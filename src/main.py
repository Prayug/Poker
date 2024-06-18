import eel
from Player import Player
from Game import PokerGame
from AI import AIPlayer

eel.init('web')

player1 = Player("You", 10000)
player2 = AIPlayer("AI", 10000)  #AI player
game = PokerGame([player1, player2])
cards_dealt = False

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
        game.players[0].check()
        game.players[1].check()
    elif action == "raise" and raise_amount is not None:
        raise_amount = int(raise_amount)
        game.player_raise(game.players[0], raise_amount)
        game.ai_call(game.players[1])
    
    game.advance_game_stage()

    if game.showdown_needed():
        game.showdown()
    
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
    game.reset_game()
    cards_dealt = False
    return game.get_game_state()

# @eel.expose
# def get_initial_state():
#     state = get_game_state()
#     state["highest_bet"] = game.highest_bet
#     return state


if __name__ == "__main__":
    eel.start('index.html', size=(800, 600))
