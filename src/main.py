import eel
from Player import Player
from Game import PokerGame
from AI import AIPlayer

eel.init('web')

player1 = Player("Alice", 10000)
player2 = AIPlayer("AI", 10000)  # AI player
game = PokerGame([player1, player2])
cards_dealt = False

@eel.expose
def get_initial_state():
    return game.get_game_state()

@eel.expose
def deal_cards():
    global cards_dealt
    if not cards_dealt:
        game.deal_cards()
        cards_dealt = True
    return game.get_game_state()

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
def play_next_round():
    global cards_dealt
    game.play_next_round()
    cards_dealt = False
    return game.get_game_state()

@eel.expose
def fold():
    global cards_dealt
    game.fold()
    cards_dealt = False
    return game.get_game_state()

eel.start('index.html', size=(1000, 600))
