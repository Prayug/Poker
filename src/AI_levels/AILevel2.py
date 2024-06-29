from Player import Player
from Card import Value, Suit

class AIPlayerLevel2(Player):
    def __init__(self, name, chips):
        super().__init__(name, chips)

    def evaluate_hand_strength(self):
        """ Evaluate the hand strength based on the initial two cards. """
        if len(self.hand) != 2:
            return 0 

        card1, card2 = self.hand
        rank1, rank2 = card1.rank.value, card2.rank.value
        suit1, suit2 = card1.suit, card2.suit

        score = 0

        if rank1 == rank2:
            score += rank1 * 20  # Higher rank pairs get significantly higher scores

        # Evaluate suitedness
        if suit1 == suit2:
            score += 10  # Suited cards get a higher bonus

        # Evaluate connectedness
        rank_diff = abs(rank1 - rank2)
        if rank_diff == 1:
            score += 8  # Suited connectors get a high bonus
        elif rank_diff == 2:
            score += 5  # Near connectors get a moderate bonus

        # Evaluate high cards
        if rank1 >= Value.TEN.value:
            score += rank1  # Higher rank cards get higher scores
        if rank2 >= Value.TEN.value:
            score += rank2  # Higher rank cards get higher scores

        # Evaluate potential for flush draws
        if suit1 == suit2 and max(rank1, rank2) >= Value.TEN.value:
            score += 5  # Additional bonus for high suited cards

        # Evaluate potential for straight draws
        if rank_diff <= 4:
            score += 2  # Small bonus for potential straight draws

        return score

    def make_decision(self, highest_bet):
        """ Make decision based on hand strength and call if EV is positive. """
        hand_strength = self.evaluate_hand_strength()

        # Call if hand strength is above a certain threshold
        call_threshold = 20  # This threshold can be adjusted based on desired aggressiveness
        if hand_strength >= call_threshold:
            return "Call"
        return "Fold"  # AI folds if the hand strength is below the threshold
