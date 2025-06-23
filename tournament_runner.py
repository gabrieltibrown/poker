import argparse
from collections import defaultdict
from agents.agent_registry import AGENT_MAP
from poker_utils import run_match

def main():
    parser = argparse.ArgumentParser(description="Poker Bot Tournament Runner")
    parser.add_argument('--agent1', type=str, required=True, help="Name of first agent (e.g. MyFirstAgent)")
    parser.add_argument('--agent2', type=str, required=True, help="Name of second agent (e.g. RandomAgent)")
    parser.add_argument('--rounds', type=int, default=100, help="Number of hands per match")
    parser.add_argument('--matches', type=int, default=10, help="Number of repeated matches")
    parser.add_argument('--verbose', action='store_true', help="Print detailed output")
    args = parser.parse_args()

    if args.agent1 not in AGENT_MAP or args.agent2 not in AGENT_MAP:
        print(f"Error: Unknown agent name. Available agents: {', '.join(AGENT_MAP.keys())}")
        return

    Agent1Class = AGENT_MAP[args.agent1]
    Agent2Class = AGENT_MAP[args.agent2]

    scores = defaultdict(int)

    print(f"\n🃏 Running {args.matches} matches of {args.rounds} hands each\n")

    for match_num in range(1, args.matches + 1):
        print(f"Match {match_num}... ", end="", flush=True)

        a1 = Agent1Class()
        a2 = Agent2Class()
        diff1, diff2 = run_match(a1, a2, num_rounds=args.rounds, verbose=args.verbose)

        scores[args.agent1] += diff1
        scores[args.agent2] += diff2

        print(f"Result: {args.agent1} {diff1:+} | {args.agent2} {diff2:+}")

    print("\n🏆 Final Results:")
    for agent, score in sorted(scores.items(), key=lambda x: -x[1]):
        print(f"{agent}: {score:+}")

if __name__ == "__main__":
    main()
