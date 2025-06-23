from pypokerengine.players import BasePokerPlayer
import random

class SuitedConnectorAgent(BasePokerPlayer):
    def declare_action(self, valid_actions, hole_card, round_state):
        suits = [card[0] for card in hole_card]
        ranks = [card[1] for card in hole_card]
        rank_values = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8,
                       '9':9, 'T':10, 'J':11, 'Q':12, 'K':13, 'A':14}
        r1, r2 = rank_values[ranks[0]], rank_values[ranks[1]]

        is_suited = suits[0] == suits[1]
        is_connected = abs(r1 - r2) == 1

        if is_suited and is_connected:
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