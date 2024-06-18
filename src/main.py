import eel
from Player import Player
from Game import PokerGame

eel.init('web')

player1 = Player("Alice", 10000)
player2 = Player("Bob", 10000)
game = PokerGame([player1, player2])
cards_dealt = False

@eel.expose
def deal_cards():
    global cards_dealt
    if not cards_dealt:
        game.deal_cards()
        cards_dealt = True
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
    global cards_dealt
    game.reset_game()
    cards_dealt = False
    return get_game_state()

def get_game_state():
    def get_card_image_path(card):
        rank = card.rank.value
        suit = card.suit.value
        return f"cards/{rank}{suit}.png"

    return {
        "player1": {
            "name": game.players[0].name,
            "chips": game.players[0].chips,
            "hand": [get_card_image_path(card) for card in game.players[0].hand]
        },
        "player2": {
            "name": game.players[1].name,
            "chips": game.players[1].chips,
            "hand": [get_card_image_path(card) for card in game.players[1].hand]
        },
        "community_cards": [get_card_image_path(card) for card in game.community_cards],
        "log": ["Game state updated"]
    }

@eel.expose
def get_initial_state():
    return get_game_state()

if __name__ == "__main__":
    eel.start('index.html', size=(800, 600))
