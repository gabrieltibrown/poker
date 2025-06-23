import argparse
from collections import defaultdict
from agents.agent_registry import AGENT_MAP
from poker_utils import run_match

def main():
    parser = argparse.ArgumentParser(description="Poker Bot Benchmark Runner")
    parser.add_argument('--agent', type=str, required=True, help="Agent to benchmark against all others")
    parser.add_argument('--rounds', type=int, default=100, help="Hands per match")
    parser.add_argument('--matches', type=int, default=10, help="Matches per opponent")
    parser.add_argument('--verbose', action='store_true', help="Verbose output")
    args = parser.parse_args()

    if args.agent not in AGENT_MAP:
        print(f"Unknown agent: {args.agent}")
        print("Available agents:", ", ".join(AGENT_MAP.keys()))
        return

    tested_agent_cls = AGENT_MAP[args.agent]
    opponents = [name for name in AGENT_MAP if name != args.agent]
    results = defaultdict(float)

    print(f"\nBenchmarking {args.agent} against {len(opponents)} opponents:\n" + ", ".join(opponents) + "\n")

    for opponent_name in opponents:
        opponent_cls = AGENT_MAP[opponent_name]
        total_score = 0
        for _ in range(args.matches):
            a1 = tested_agent_cls()
            a2 = opponent_cls()
            diff1, diff2 = run_match(a1, a2, num_rounds=args.rounds, verbose=args.verbose)
            total_score += diff1
            if args.verbose:
                print(f"Match vs {opponent_name}: {args.agent} {diff1:+} | {opponent_name} {diff2:+}")
        avg_score = total_score / args.matches
        results[opponent_name] = avg_score

    print(f"\nAverage Results for {args.agent} (positive = agent won chips):")
    for opponent_name, avg in sorted(results.items(), key=lambda x: -x[1]):
        print(f"{args.agent} vs {opponent_name}: {avg:+.2f}")

if __name__ == "__main__":
    main()
