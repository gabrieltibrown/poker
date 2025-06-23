from pypokerengine.api.game import setup_config, start_poker

def run_match(agent1, agent2, num_rounds=100, initial_stack=1000, verbose=False):
    config = setup_config(max_round=num_rounds, initial_stack=initial_stack, small_blind_amount=5)
    config.register_player(name="Player1", algorithm=agent1)
    config.register_player(name="Player2", algorithm=agent2)
    game_result = start_poker(config, verbose=0)

    final_stacks = {p['name']: p['stack'] for p in game_result['players']}
    diff1 = final_stacks["Player1"] - initial_stack
    diff2 = final_stacks["Player2"] - initial_stack

    if verbose:
        print(f"Final Stacks: {final_stacks}")

    return diff1, diff2