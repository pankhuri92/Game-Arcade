import pygame
import sys
import random
from gameplay import Game
from gameplay import Player
from strategy import computer_bid

# Initialize Pygame
pygame.init()

# Set up the screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the title of the window
pygame.display.set_caption("Diamonds")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load card images
card_images = {}
for i in range(2, 15):
    card_path = f"images/{i}_of_diamonds.png"  # Adjust the path as needed
    card_images[i] = pygame.transform.scale(pygame.image.load(card_path), (72, 96))  # Adjust size as needed

# Load card images for player's hand (other than diamonds)
player_hand_images = {}
suit = random.choice(["hearts","clubs","spades"])
for i in range(2, 15):
    card_path = f"images/{i}_of_{suit}.png"  # Adjust the path as needed
    player_hand_images[i] = pygame.transform.scale(pygame.image.load(card_path), (72, 96))  # Adjust size as needed

# Fonts
font = pygame.font.Font(None, 36)

def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def start_screen():
    screen.fill(WHITE)
    draw_text("Diamonds", BLACK, screen_width // 2, screen_height // 2 - 100)
    pygame.draw.rect(screen, BLACK, (screen_width // 2 - 100, screen_height // 2, 200, 50))
    draw_text("Start Game", WHITE, screen_width // 2, screen_height // 2 + 25)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if screen_width // 2 - 100 <= x <= screen_width // 2 + 100 and \
                   screen_height // 2 <= y <= screen_height // 2 + 50:
                    return

def end_screen(player_score, computer_score):
    while True:
        screen.fill(WHITE)
        
        # Display player and computer scores
        draw_text(f"Your Score: {player_score}", BLACK, screen_width // 2, screen_height // 2 - 60)
        draw_text(f"Computer Score: {computer_score}", BLACK, screen_width // 2, screen_height // 2 + 20)
        
        # Determine the winner
        if player_score > computer_score:
            draw_text("You Win!", BLACK, screen_width // 2, screen_height // 2 - 100)
        elif computer_score > player_score:
            draw_text("Computer Wins!", BLACK, screen_width // 2, screen_height // 2 - 100)
        else:
            draw_text("It's a Tie!", BLACK, screen_width // 2, screen_height // 2 - 100)
        
        # Draw 'Play Again' button
        pygame.draw.rect(screen, BLACK, (screen_width // 2 - 100, screen_height // 2 + 100, 200, 50))
        draw_text("Play Again", WHITE, screen_width // 2, screen_height // 2 + 125)
        
        # Draw 'Exit' button
        pygame.draw.rect(screen, BLACK, (screen_width // 2 - 100, screen_height // 2 + 200, 200, 50))
        draw_text("Exit", WHITE, screen_width // 2, screen_height // 2 + 225)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if screen_width // 2 - 100 <= x <= screen_width // 2 + 100:
                    if screen_height // 2 + 100 <= y <= screen_height // 2 + 150:
                        # Play Again button clicked
                        return True
                    elif screen_height // 2 + 200 <= y <= screen_height // 2 + 250:
                        # Exit button clicked
                        pygame.quit()
                        sys.exit()

def initialize_game():
    player_name = "Player"
    game = Game(player_name)
    return game

def player_bid(player):
    selected_card = None
    while True:
        screen.fill(WHITE)
        draw_text("Your Hand:", BLACK, screen_width // 2, screen_height // 2 - 200)
        
        # Draw player's hand
        card_width = 72
        card_height = 96
        card_spacing = 20  # Adjust spacing as needed
        row_spacing = 30  # Adjust spacing between rows as needed
        cards_per_row = 7  # Adjust number of cards per row as needed
        for i, card in enumerate(player.hand, start=1):
            row = 0 if i <= cards_per_row else 1
            col = (i - 1) % cards_per_row
            x = col * (card_width + card_spacing) + card_spacing // 2
            y = row * (card_height + row_spacing) + screen_height // 2 - (1.5 * card_height)
            card_image = player_hand_images[card]
            screen.blit(card_image, (x, y))
            
            # Check if the card is clicked
            card_rect = pygame.Rect(x, y, card_width, card_height)
            if card_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, (255, 0, 0), card_rect, 2)
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for i, card in enumerate(player.hand, start=1):
                    row = 0 if i <= cards_per_row else 1
                    col = (i - 1) % cards_per_row
                    card_x = col * (card_width + card_spacing) + card_spacing // 2
                    card_y = row * (card_height + row_spacing) + screen_height // 2 - (1.5 * card_height)
                    card_rect = pygame.Rect(card_x, card_y, card_width, card_height)
                    if card_rect.collidepoint(x, y):
                        selected_card = card
                        break
                if selected_card:
                    try:
                        return player.make_bid(selected_card)
                    except ValueError as e:
                        print(e)
                        selected_card = None

def game_loop():
    start_screen()
    
    while True:
        game = initialize_game()
        diamonds = game.diamonds
        computer_hand = game.computer.hand
        player_hand = game.player.hand
        computer_score, player_score = 0, 0
        opponent_bids = []

        for rounds_played, diamond_card in enumerate(diamonds, start=1):
            screen.fill(WHITE)
            
            # Display round number
            draw_text(f"Round {rounds_played}", BLACK, screen_width - 80, 30)
            
            # Display diamond card
            card_image = card_images[diamond_card]
            screen.blit(card_image, (screen_width // 2 - 36, screen_height // 2 - 48))
            
            # Display player and computer bids
            if opponent_bids:
                draw_text(f"Player Bid: {opponent_bids[-1]}", BLACK, screen_width // 2 - 150, 50)
                draw_text(f"Computer Bid: {computer_bid_value}", BLACK, screen_width // 2 + 150, 50)
            
            # Display scores
            draw_text(f"Your Score: {player_score}", BLACK, screen_width - 150, screen_height - 100)
            draw_text(f"Computer Score: {computer_score}", BLACK, screen_width - 150, screen_height - 50)
            
            pygame.display.flip()
            pygame.time.wait(2000)  # Delay for 2 seconds (you can adjust as needed)
            
            player_bid_value = player_bid(game.player)
            computer_bid_value = computer_bid(computer_hand, diamond_card, rounds_played, opponent_bids, computer_score, player_score)
            opponent_bids.append(player_bid_value)
            
            player_points, computer_points = game.score_round(diamond_card, player_bid_value, computer_bid_value)
            player_score += player_points
            computer_score += computer_points

            print(f"Round Score - You: {player_points}, Computer: {computer_points}")
            print(f"Total Score - You: {player_score}, Computer: {computer_score}\n")

        if not end_screen(player_score, computer_score):
            break

game_loop()
