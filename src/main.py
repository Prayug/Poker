import eel
from Player import Player
from Game import PokerGame
from AI import AIPlayer

eel.init('web')

player1 = Player("Player", 10000)
player2 = AIPlayer("AI", 10000)  # AI player
game = PokerGame([player1, player2])
cards_dealt = False
preflop = True

@eel.expose
def get_initial_state():
    return game.get_game_state()

@eel.expose
def deal_cards():
    global cards_dealt, preflop
    if not cards_dealt:
        game.collect_blinds()  # Collect blinds when dealing cards
        game.deal_cards()
        cards_dealt = True
        preflop = True
    return game.get_game_state()

@eel.expose
def get_best_hand():
    best_hand, hand_type = game.get_best_hand(player1)
    return {
        "best_hand": best_hand,
        "hand_type": hand_type
    }

@eel.expose
def collect_bets(action, raise_amount=None):
    if action == "check":
        game.collect_bets(action)
    elif action == "raise" and raise_amount is not None:
        game.collect_bets(action, raise_amount)
    return game.get_game_state()

@eel.expose
def deal_community_cards(number):
    game.deal_community_cards(number)
    return game.get_game_state()

@eel.expose
def showdown():
    game.showdown()
    return game.get_game_state()

@eel.expose
def reset_game():
    global cards_dealt, preflop
    game.reset_game()
    cards_dealt = False
    preflop = False
    return game.get_game_state()

@eel.expose
def fold():
    global cards_dealt, preflop
    game.fold()
    cards_dealt = False
    preflop = False
    return game.get_game_state()

eel.start('index.html', size=(1000, 600))
