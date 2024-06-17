import eel
# from src.Player import Player
# from src.Game import PokerGame
# from src.Card import Card
from Player import Player
from Game import PokerGame

# Initialize Eel
eel.init('web')

# Initialize the game
player1 = Player("Alice", 10000)
player2 = Player("Bob", 10000)
game = PokerGame([player1, player2])

@eel.expose
def deal_cards():
    print("hello")
    game.deal_cards()
    return get_game_state()

@eel.expose
def collect_bets():
    game.collect_bets()
    return get_game_state()

@eel.expose
def deal_community_cards(number):
    game.deal_community_cards(number)
    return get_game_state()

@eel.expose
def showdown():
    game.showdown()
    return get_game_state()

@eel.expose
def play_next_round():
    game.play_round()
    return get_game_state()

def get_game_state():
    return {
        "player1": {
            "name": game.players[0].name,
            "chips": game.players[0].chips,
            "hand": [str(card) for card in game.players[0].hand]
        },
        "player2": {
            "name": game.players[1].name,
            "chips": game.players[1].chips,
            "hand": [str(card) for card in game.players[1].hand]
        },
        "community_cards": [str(card) for card in game.community_cards],
        "log": ["Game state updated"]
    }

if __name__ == "__main__":
    eel.start('index.html', size=(800, 600))