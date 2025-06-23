from pypokerengine.players import BasePokerPlayer
import random

class PairPlayer(BasePokerPlayer):
    def declare_action(self, valid_actions, hole_card, round_state):
        ranks = [card[1] for card in hole_card]
        if ranks[0] == ranks[1]:
            return 'raise', [a for a in valid_actions if a['action'] == 'raise'][0]['amount']['min']
        return 'call', 0

    def receive_game_start_message(self, game_info):
        pass
    def receive_round_start_message(self, round_count, hole_card, seats):
        pass
    def receive_street_start_message(self, street, round_state):
        pass
    def receive_game_update_message(self, action, new_game_state):
        pass
    def receive_round_result_message(self, winners, hand_info, round_state):
        pass