# possible additional ideas
# GUI stuff
# Multiplayer
# AI players

from itertools import combinations
import sys
import os
import pygame
from typing import List, Tuple
from Deck import Deck  
from Card import Card, Suit, Value 

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Player import Player

class PokerGame:

    def __init__(self, players):
        self.deck = Deck()  
        self.players = players
        self.community_cards = []
        self.pot = 0
        self.highest_bet = 0

    def deal_cards(self):
        for player in self.players:
            player.setCards(self.deck.deal())
        for player in self.players:
            player.setCards(self.deck.deal())

    def deal_community_cards(self, number):
        for _ in range(number):
            self.community_cards.append(self.deck.deal())

    def collect_bets(self):
        print("\nCollecting bets...\n")
        active_players = [p for p in self.players if not p.fold]
        self.highest_bet = 0

        for player in active_players:
            player.current_bet = 0

        first_bet = True
        while True:
            all_acted = True
            for player in active_players:
                if player.fold:
                    continue

                if player.current_bet == self.highest_bet and not first_bet:
                    continue

                print(f"{player.name}, you have {player.chips} chips.")
                action = input(f"{player.name}, your action (check/call/raise/fold/all-in): ").lower()
                if action == "fold":
                    player.fold_hand()
                    active_players = [p for p in self.players if not p.fold]
                    if len(active_players) == 1:
                        winner = active_players[0]
                        print(f"\n{winner.name} wins the pot of {self.pot} chips!\n")
                        winner.chips += self.pot
                        return True
                elif action == "check":
                    if self.highest_bet == 0:
                        player.check()
                    else:
                        print("You can't check, there's a bet to call.")
                        all_acted = False
                        continue
                elif action == "call":
                    if player.current_bet < self.highest_bet:
                        bet_amount = player.call(self.highest_bet)
                        self.pot += bet_amount
                        print(f"{player.name} calls with {bet_amount}. Current bet: {player.current_bet}, Pot: {self.pot}")
                    else:
                        print("You have already matched the highest bet.")
                elif action == "raise":
                    raise_amount = int(input("Enter raise amount: "))
                    if raise_amount < self.highest_bet * 2:
                        print("You must raise at least 2 times the last raise.")
                        all_acted = False
                        continue

                    if raise_amount <= player.chips:
                        bet_amount = player.call(raise_amount)
                        self.pot += bet_amount
                        self.highest_bet = player.current_bet
                        print(f"{player.name} raises to {raise_amount}. Current bet: {player.current_bet}, Pot: {self.pot}")
                        all_acted = False
                    else:
                        print("You don't have enough chips to raise that amount.")
                        all_acted = False
                        continue
                elif action == "all-in":
                    bet_amount = player.all_in()
                    self.pot += bet_amount
                    if player.current_bet > self.highest_bet:
                        self.highest_bet = player.current_bet
                    print(f"{player.name} goes all-in with {bet_amount}. Current bet: {player.current_bet}, Pot: {self.pot}")
                    all_acted = False

                print(f"{player.name} has bet {player.current_bet} in this round.")

            if all_acted:
                break
            first_bet = False

        return False

    def play_round(self):
        self.deck = Deck()  # Reset and shuffle the deck
        self.community_cards = []
        self.pot = 0
        self.highest_bet = 0

        self.deal_cards()
        for player in self.players:
            print(f"\n{player.name} hand: {player.hand}")

        if self.collect_bets():
            return

        self.deal_community_cards(3)  # Flop
        print(f"\nFlop: {self.community_cards}\n")

        if self.collect_bets():
            return

        self.deal_community_cards(1)  # Turn
        print(f"\nTurn: {self.community_cards}\n")

        if self.collect_bets():
            return

        self.deal_community_cards(1)  # River
        print(f"\nRiver: {self.community_cards}\n")

        if self.collect_bets():
            return

        self.showdown()
    
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