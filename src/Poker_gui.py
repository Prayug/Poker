import pygame
import sys
import os
from Deck import Deck
from Player import Player
from Game import PokerGame

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BG_COLOR = (0, 128, 0)  # Green color for the poker table
WHITE = (255, 255, 255)
FONT_SIZE = 20

# Card images directory
CARDS_DIR = os.path.join(os.path.dirname(__file__), 'cards')

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Poker Game')

# Load card images
card_images = {}
missing_card_image = pygame.Surface((50, 75))  # Placeholder image for missing cards
missing_card_image.fill((255, 0, 0))  # Fill placeholder with red color

for suit in ["♠", "♥", "♦", "♣"]:
    for value in range(2, 15):
        card_filename = os.path.join(CARDS_DIR, f"{value}{suit}.png")
        try:
            card_images[(suit, value)] = pygame.image.load(card_filename)
        except FileNotFoundError:
            card_images[(suit, value)] = missing_card_image

# Font setup
font = pygame.font.Font(None, FONT_SIZE)

def draw_text(text, x, y, color=WHITE):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_card(card, x, y):
    card_img = card_images.get((card.suit.value, card.rank.value), missing_card_image)
    screen.blit(card_img, (x, y))

def draw_player(player, x, y):
    draw_text(f"{player.name}: {player.chips} chips", x, y)
    for i, card in enumerate(player.hand):
        draw_card(card, x + i * 40, y + 20)

def draw_pot(pot, x, y):
    draw_text(f"Pot: {pot} chips", x, y)

def draw_community_cards(cards, x, y):
    for i, card in enumerate(cards):
        draw_card(card, x + i * 40, y)

def main():
    player1 = Player("Alice", 10000)
    player2 = Player("Bob", 10000)
    game = PokerGame([player1, player2])

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BG_COLOR)

        game.play_round()  # Run a single round

        # Draw players
        draw_player(player1, 50, 50)
        draw_player(player2, 50, 200)

        # Draw pot
        draw_pot(game.pot, SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2)

        # Draw community cards
        draw_community_cards(game.community_cards, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50)

        pygame.display.flip()
        clock.tick(30)  # Limit to 30 FPS

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
