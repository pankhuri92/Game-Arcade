import random

scorecard = {}
categories = ["Ones", "Twos", "Threes", "Fours", "Fives", "Sixes",
              "Three of a Kind", "Four of a Kind", "Full House",
              "Small Straight", "Large Straight", "Yahtzee", "Chance"]

def roll_dice(num_dice):
    return [random.randint(1, 6) for _ in range(num_dice)]

def display_dice(dice):
    print("Dice:", dice)

def player_turn():
    rolls_left = 3
    dice = roll_dice(5)
    display_dice(dice)

    while rolls_left > 0:
        choice = input(f"You have {rolls_left} rolls left. Press Enter to roll again, or 's' to score: ")

        if choice.lower() == 's':
            break

        dice_to_reroll = input("Enter the indices of dice to re-roll (e.g., '1 3 4'), or press Enter to re-roll all: ")

        if dice_to_reroll:
            indices = [int(index) - 1 for index in dice_to_reroll.split()]
            for index in indices:
                if 0 <= index < 5:
                    dice[index] = random.randint(1, 6)
                else:
                    print("Invalid index! Please enter a number between 1 and 5.")
                    continue  # Continue to next iteration if index is invalid

        else:
            dice = roll_dice(5)

        display_dice(dice)
        rolls_left -= 1

    category = input("Enter the category to score: ")
    if category in categories:
        score = calculate_score(category, dice)
        update_scorecard(category, score)
        display_scorecard()
    else:
        print("Invalid category. Please choose from the available categories.")

def calculate_score(category, dice):
    if category in ["Ones", "Twos", "Threes", "Fours", "Fives", "Sixes"]:
        category_value = int(category[0])  # Extract the numeric part of the category name
        return sum(d for d in dice if category_value == d)
    elif category == "Three of a Kind":
        if any(dice.count(d) >= 3 for d in dice):
            return sum(dice)
        else:
            return 0
    elif category == "Four of a Kind":
        if any(dice.count(d) >= 4 for d in dice):
            return sum(dice)
        else:
            return 0
    elif category == "Full House":
        counts = [dice.count(d) for d in set(dice)]
        if 2 in counts and 3 in counts:
            return 25
        else:
            return 0
    elif category == "Small Straight":
        sorted_dice = sorted(set(dice))
        if len(sorted_dice) >= 4 and any(sorted_dice[i] + 1 == sorted_dice[i+1] == sorted_dice[i+2] == sorted_dice[i+3] for i in range(len(sorted_dice) - 3)):
            return 30
        else:
            return 0
    elif category == "Large Straight":
        sorted_dice = sorted(set(dice))
        if len(sorted_dice) == 5 and sorted_dice[-1] - sorted_dice[0] == 4:
            return 40
        else:
            return 0
    elif category == "Yahtzee":
        if any(dice.count(d) == 5 for d in dice):
            return 50
        else:
            return 0
    elif category == "Chance":
        return sum(dice)
    else:
        print("Invalid category")
        return 0

def display_scorecard():
    print("Scorecard:")
    for category, score in scorecard.items():
        if score is not None:
            print(f"{category}: {score}")
        else:
            print(f"{category}: Not scored yet")

def update_scorecard(category, score):
    scorecard[category] = score

def initialize_game():
    global scorecard
    scorecard = {category: None for category in categories}

def check_end_game():
    return all(score is not None for score in scorecard.values())

def display_winner():
    # Implement how to display the winner of the game
    pass

def main():
    initialize_game()
    while not check_end_game():
        player_turn()

    display_winner()

if __name__ == "__main__":
    main()
