# poker

This project provides a framework to benchmark different poker-playing agents against each other. It supports running multiple matches between agents, visualizing results as a heatmap, and displaying a colored heatmap directly in the command line interface (CLI).

## Features

- Run **all-vs-all** agent matches to compare performance
- Supports **parallel execution** for faster benchmarking
- Output detailed results as a **heatmap image (PNG)**
- Alternatively, display a **color-coded heatmap in the CLI** using `rich`
- Symmetric benchmarking: runs only unique agent pairs, filling the heatmap symmetrically to halve runtime
- Clear interpretation: each heatmap cell shows the average chip lead of the **row agent** over the **column agent**


## Setup

### Requirements

- Python 3.8+
- Required packages (install via pip):

```bash
pip install pandas seaborn matplotlib tqdm rich
```

## Usage

Run the benchmark with default parameters:

```bash
python benchmark_heatmap.py
```

Run with more matches, rounds, and parallel workers, and save heatmap image:

```bash
python benchmark_heatmap.py --matches 10 --rounds 100 --workers 8 --output results.png
```

Run benchmark and show CLI heatmap (no image saved):

```bash
python benchmark_heatmap.py --matches 5 --rounds 50
```

| Argument    | Description                                                       | Default |
| ----------- | ----------------------------------------------------------------- | ------- |
| `--matches` | Number of matches per agent pair                                  | 10      |
| `--rounds`  | Number of hands per match                                         | 100     |
| `--workers` | Number of parallel worker threads                                 | 4       |
| `--output`  | Path to save heatmap image (PNG). If omitted, outputs CLI heatmap | None    |
| `--verbose` | Enable verbose output during matches                              | False   |

## Adding New Agents

1. **Create the agent class**  
   Add a new Python file in `agents/` with your agent implementing the required interface methods (`receive_game_start_message`, `receive_round_start_message`, etc.).

2. **Register the agent**  
   Import your agent in `agent_registry.py` and add it to the `AGENT_MAP` dictionary with a unique name, e.g.:  
   ```python
   from agents.my_custom_agent import MyCustomAgent

   AGENT_MAP["MyCustomAgent"] = MyCustomAgent
   ```


## How to interpret results

Heatmap rows represent the agent playing as Player 1.

Heatmap columns represent the agent playing as Player 2.

Each cell shows the average chips won by the row agent against the column agent.

Values are positive if the row agent outperformed the column agent, negative if underperformed.

Diagonal cells are zero (no self-play).