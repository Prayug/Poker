# possible additional ideas
# GUI stuff
# Multiplayer
# AI players
import eel
from itertools import combinations
import sys
import os
import pygame
from typing import List, Tuple
from Deck import Deck  
from Card import Card, Suit, Value 
from AI import AIPlayer

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Player import Player

class PokerGame:
    def __init__(self, players):
        self.deck = Deck()  
        self.players = players
        self.community_cards = []
        self.pot = 0
        self.highest_bet = 0
        self.ai_player = next((p for p in players if isinstance(p, AIPlayer)), None)

    def get_game_state(self):
        def get_card_image_path(card):
            rank = card.rank.value
            suit = card.suit.value
            return f"cards/{rank}{suit}.png"

        return {
            "player1": {
                "name": self.players[0].name,
                "chips": self.players[0].chips,
                "hand": [get_card_image_path(card) for card in self.players[0].hand]
            },
            "player2": {
                "name": self.players[1].name,
                "chips": self.players[1].chips,
                "hand": [get_card_image_path(card) for card in self.players[1].hand]
            },
            "community_cards": [get_card_image_path(card) for card in self.community_cards],
            "log": ["Game state updated"]
        }

    def advance_game_stage(self):
        if not self.flop_dealt:
            self.deal_community_cards(3)
            self.flop_dealt = True
        elif not self.turn_dealt:
            self.deal_community_cards(1)
            self.turn_dealt = True
        elif not self.river_dealt:
            self.deal_community_cards(1)
            self.river_dealt = True
        else:
            self.showdown()

    def reset_game(self):
        self.deck = Deck()
        self.community_cards = []
        self.pot = 0
        self.highest_bet = 0
        self.flop_dealt = False
        self.turn_dealt = False
        self.river_dealt = False
        for player in self.players:
            player.reset_hand()
        self.log = []

    def deal_cards(self):
        for player in self.players:
            player.setCards(self.deck.deal())
        for player in self.players:
            player.setCards(self.deck.deal())

    def deal_community_cards(self, number):
        if number == 3 and not self.flop_dealt:
            self.community_cards.extend(self.deck.deal() for _ in range(3))
            self.flop_dealt = True
        elif number == 1 and not self.turn_dealt and self.flop_dealt:
            self.community_cards.append(self.deck.deal())
            self.turn_dealt = True
        elif number == 1 and not self.river_dealt and self.turn_dealt:
            self.community_cards.append(self.deck.deal())
            self.river_dealt = True

    def collect_bets(self, player_action, raise_amount=None):
        active_players = [p for p in self.players if not p.fold]
        
        if player_action == "check":
            # Both players check
            self.players[0].check()
            self.players[1].check()
            self.advance_game_stage()  # Automatically advance to the next stage
        elif player_action == "raise" and raise_amount is not None:
            raise_amount = int(raise_amount)
            self.player_raise(self.players[0], raise_amount)
            self.ai_call(self.players[1])
        
        if self.showdown_needed():
            self.showdown()
        
        return self.get_game_state()

    def play_round(self):
        self.reset_game()
        self.deal_cards()
    
    def showdown(self):
        # Simple winner determination placeholder
        print("\nShowdown!")
        player1_best_hand, player1_hand_type = self.evaluate_hand(self.players[0].hand + self.community_cards)
        player2_best_hand, player2_hand_type = self.evaluate_hand(self.players[1].hand + self.community_cards)

        print(f"\n{self.players[0].name}'s best hand: {player1_best_hand} ({player1_hand_type})")
        print(f"{self.players[1].name}'s best hand: {player2_best_hand} ({player2_hand_type})")

        if player1_best_hand > player2_best_hand:
            print(f"\n{self.players[0].name} wins the pot of {self.pot} chips!\n")
            self.players[0].chips += self.pot
        elif player2_best_hand > player1_best_hand:
            print(f"\n{self.players[1].name} wins the pot of {self.pot} chips!\n")
            self.players[1].chips += self.pot
        else:
            print("\nIt's a tie!")
            split_pot = self.pot // 2
            self.players[0].chips += split_pot
            self.players[1].chips += split_pot

    def evaluate_hand(self, cards: List[Card]) -> Tuple[Tuple[int, List[int]], str]:
        best_rank = (-1, [])
        best_hand_type = "High Card"
        
        for combo in combinations(cards, 5):
            rank, hand_type = self.rank_hand(combo)
            if rank > best_rank:
                best_rank = rank
                best_hand_type = hand_type
        return best_rank, best_hand_type

    def rank_hand(self, hand: List[Card]) -> Tuple[Tuple[int, List[int]], str]:
        values = sorted([card.rank.value for card in hand], reverse=True)
        suits = [card.suit for card in hand]
        
        is_flush = len(set(suits)) == 1
        is_straight = all(values[i] - values[i+1] == 1 for i in range(len(values) - 1))
        value_counts = {v: values.count(v) for v in values}
        counts = sorted(value_counts.values(), reverse=True)
        ranks_by_count = sorted(value_counts, key=lambda k: (value_counts[k], k), reverse=True)

        if is_straight and is_flush and values[0] == Value.ACE.value:
            return (10, values), "Royal Flush"
        if is_straight and is_flush:
            return (9, values), "Straight Flush"
        if counts == [4, 1]:
            return (8, ranks_by_count), "Four of a Kind"
        if counts == [3, 2]:
            return (7, ranks_by_count), "Full House"
        if is_flush:
            return (6, values), "Flush"
        if is_straight:
            return (5, values), "Straight"
        if counts == [3, 1, 1]:
            return (4, ranks_by_count), "Three of a Kind"
        if counts == [2, 2, 1]:
            return (3, ranks_by_count), "Two Pair"
        if counts == [2, 1, 1, 1]:
            return (2, ranks_by_count), "One Pair"
        return (1, values), "High Card"
    
    def player_raise(self, player, raise_amount):
        raise_amount = player.raise_bet(raise_amount, self.highest_bet)
        self.pot += raise_amount
        self.highest_bet = player.current_bet
        return raise_amount

    def ai_call(self, ai_player):
        call_amount = ai_player.call(self.highest_bet)
        self.pot += call_amount
        return call_amount

    def both_check(self):
        if not self.flop_dealt:
            self.deal_community_cards(3)
        elif not self.turn_dealt:
            self.deal_community_cards(1)
        elif not self.river_dealt:
            self.deal_community_cards(1)
        else:
            self.showdown()

def main():
    # pygame.init()
    # screen = pygame.display.set_mode((800, 600)) 
    # pygame.display.set_caption('My Pygame Window')
    
    # running = True
    # while running:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             running = False
        
    #     screen.fill((0, 128, 255)) 
    #     pygame.display.flip()
    
    # pygame.quit()
    # sys.exit()
    player1 = Player("Alice", 10000)
    player2 = Player("Bob", 10000)
    game = PokerGame([player1, player2])
    game.play_round()   

    # Done Step 1: Shuffle deck (optional: blinds)
    # Done Step 2: Deal cards
    # Step 3: Collect bets
    # Step 4: Show flop
    # Step 5: Collect bets
    # Step 6: Show turn
    # Step 7: Collect bets
    # Step 8: Show river
    # Step 9: Collect bets
    # Step 10: Showdown
    # Step 11: Award chips
    # Step 12: Repeat

    # while isGame:
    #     game = PokerGame([player1, player2])
    #     game.play_round()
    #     print(player1.hand)
    #     print(player2.hand)

if __name__ == "__main__":
    main()