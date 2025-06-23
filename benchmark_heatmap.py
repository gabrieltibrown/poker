import argparse
import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from rich.console import Console
from rich.table import Table
import numpy as np

from agents.agent_registry import AGENT_MAP
from poker_utils import run_match

console = Console()

def run_single_match(agent1_name, agent2_name, matches, rounds, verbose):
    agent1_cls = AGENT_MAP[agent1_name]
    agent2_cls = AGENT_MAP[agent2_name]
    total_score = 0
    for _ in range(matches):
        a1 = agent1_cls()
        a2 = agent2_cls()
        diff1, diff2 = run_match(a1, a2, num_rounds=rounds, verbose=verbose)
        total_score += diff1
    avg_score = total_score / matches
    if verbose:
        print(f"{agent1_name} vs {agent2_name}: {avg_score:+.2f}")
    return (agent1_name, agent2_name, avg_score)

def run_all_vs_all_parallel(matches, rounds, verbose, max_workers=4):
    agents = list(AGENT_MAP.keys())
    results_matrix = pd.DataFrame(index=agents, columns=agents, dtype=float)

    pairs = []
    n = len(agents)
    for i in range(n):
        for j in range(i+1, n):  # only i < j to avoid duplicate pairs and self-play
            pairs.append((agents[i], agents[j]))

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(run_single_match, a1, a2, matches, rounds, verbose): (a1, a2) for a1, a2 in pairs}

        for future in tqdm(as_completed(futures), total=len(futures), desc="Benchmarking"):
            agent1_name, agent2_name, avg_score = future.result()
            results_matrix.at[agent1_name, agent2_name] = avg_score
            results_matrix.at[agent2_name, agent1_name] = -avg_score  # symmetric

    # Diagonal zero
    for agent in agents:
        results_matrix.at[agent, agent] = 0

    return results_matrix

def print_heatmap_cli(df):
    data = df.fillna(0).values
    min_val, max_val = np.min(data), np.max(data)
    range_val = max_val - min_val if max_val != min_val else 1

    def value_to_color(val):
        norm = (val - min_val) / range_val
        if norm < 0.5:
            r = 255
            g = int(2 * norm * 255)
            b = 0
        else:
            r = int(255 - 2 * (norm - 0.5) * 255)
            g = 255
            b = 0
        return f"rgb({r},{g},{b})"

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Agent \\ Opponent", style="bold")
    for col in df.columns:
        table.add_column(col)

    for idx, row in df.iterrows():
        row_colors = [value_to_color(val) for val in row]
        row_cells = [f"[{color}]{val:.1f}[/{color}]" for val, color in zip(row, row_colors)]
        table.add_row(idx, *row_cells)

    console.print(table)

def plot_heatmap(results_matrix, output_file=None):
    print("plotting heatmap")
    plt.figure(figsize=(10,8))
    sns.set(font_scale=1.1)
    ax = sns.heatmap(results_matrix, annot=True, fmt=".1f", cmap="coolwarm", center=0,
                     cbar_kws={'label': 'Avg Chips Won'})
    ax.set_title("Poker Agent vs Agent Benchmark (Avg Chips Won)")
    plt.ylabel("Agent 1")
    plt.xlabel("Agent 2")
    plt.tight_layout()
    print("saving output file")
    if output_file:
        plt.savefig(output_file)
        print(f"Heatmap saved to {output_file}")
    else:
        print("no output file")

def main():
    parser = argparse.ArgumentParser(description="Poker Agent All-vs-All Benchmark Heatmap with Parallelization")
    parser.add_argument('--matches', type=int, default=10, help="Matches per agent pair")
    parser.add_argument('--rounds', type=int, default=100, help="Hands per match")
    parser.add_argument('--verbose', action='store_true', help="Verbose output")
    parser.add_argument('--output', type=str, default=None, help="File path to save heatmap image")
    parser.add_argument('--workers', type=int, default=4, help="Number of parallel workers")
    args = parser.parse_args()

    results = run_all_vs_all_parallel(args.matches, args.rounds, args.verbose, max_workers=args.workers)
    if args.output:
        plot_heatmap(results, output_file=args.output)
    else:
        print_heatmap_cli(results)

if __name__ == "__main__":
    main()
