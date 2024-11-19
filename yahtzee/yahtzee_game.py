import tkinter as tk
import random
from tkinter import messagebox  

categories = ["Ones", "Twos", "Threes", "Fours", "Fives", "Sixes",
              "Three of a Kind", "Four of a Kind", "Full House",
              "Small Straight", "Large Straight", "Yahtzee", "Chance"]
scorecard = {category: None for category in categories}  
dice = [1, 1, 1, 1, 1]
rolls_left = 3
selected_category = None
potential_scores = {}

dice_color = "#F7E5EC"
held_dice_color = "#E8C3C9"
table_bg = "#D3E3E6"
highlight_color = "#90EE90"  
bg_color = "#4682B4"

root = tk.Tk()
root.title("Yahtzee")
root.configure(bg=bg_color)

def calculate_score(category):
    if category in ["Ones", "Twos", "Threes", "Fours", "Fives", "Sixes"]:
        category_value = categories.index(category) + 1
        return sum(d for d in dice if d == category_value)
    elif category == "Three of a Kind":
        return sum(dice) if any(dice.count(d) >= 3 for d in set(dice)) else 0
    elif category == "Four of a Kind":
        return sum(dice) if any(dice.count(d) >= 4 for d in set(dice)) else 0
    elif category == "Full House":
        counts = [dice.count(d) for d in set(dice)]
        return 25 if 2 in counts and 3 in counts else 0
    elif category == "Small Straight":
        unique_dice = sorted(set(dice))
        return 30 if len(unique_dice) >= 4 and any(
            unique_dice[i:i+4] == list(range(unique_dice[i], unique_dice[i]+4))
            for i in range(len(unique_dice) - 3)
        ) else 0
    elif category == "Large Straight":
        unique_dice = sorted(set(dice))
        return 40 if unique_dice == list(range(1, 6)) or unique_dice == list(range(2, 7)) else 0
    elif category == "Yahtzee":
        return 50 if any(dice.count(d) == 5 for d in set(dice)) else 0
    elif category == "Chance":
        return sum(dice)
    else:
        return 0

def calculate_potential_scores():
    global potential_scores
    potential_scores = {category: (calculate_score(category) if scorecard[category] is None else None) for category in categories}
    update_scorecard_table()

def update_scorecard_table():
    for i, category in enumerate(categories):
        score = potential_scores.get(category, "N/A") if scorecard[category] is None else scorecard[category]
        score_label = score_labels[i]
        score_label.config(text=str(score))
        # Highlight selected categories
        if scorecard[category] is not None:
            score_labels[i].config(bg=highlight_color)

def roll_dice():
    global rolls_left
    if rolls_left > 0:
        for i in range(5):
            if not dice_selected[i]:
                dice[i] = random.randint(1, 6)
        rolls_left -= 1
        update_dice_display()
        calculate_potential_scores()
        rolls_label.config(text=f"Rolls Left: {rolls_left}")
    check_game_end()

def select_category(category_index):
    global selected_category, rolls_left
    category = categories[category_index]
    if scorecard[category] is None:  # Only allow unscored categories
        scorecard[category] = potential_scores[category] if potential_scores[category] is not None else 0
        selected_category = category_index
        rolls_left = 3  # Reset rolls
        update_scorecard_table()
        reset_dice()
        check_game_end()

def toggle_dice(index):
    dice_selected[index] = not dice_selected[index]
    update_dice_display()

def reset_dice():
    global dice
    dice = [1, 1, 1, 1, 1]
    for i in range(5):
        dice_selected[i] = False
    update_dice_display()

def restart_game():
    global scorecard, rolls_left
    scorecard = {category: None for category in categories}
    rolls_left = 3
    reset_dice()
    update_scorecard_table()
    rolls_label.config(text=f"Rolls Left: {rolls_left}")
    check_game_end()

def check_game_end():
    if all(score is not None for score in scorecard.values()):
        total_score = sum(scorecard.values())
        messagebox.showinfo("Game Over", f"Game Over! Your total score is: {total_score}")
        restart_game()  

def update_dice_display():
    for i, die in enumerate(dice):
        color = held_dice_color if dice_selected[i] else dice_color
        dice_labels[i].config(text=str(die), bg=color)

# UI Setup
main_frame = tk.Frame(root, bg=bg_color, padx=20, pady=20)
main_frame.pack()

title_label = tk.Label(main_frame, text="Yahtzee", font=("Arial", 24, "bold"), bg=bg_color, fg="white")
title_label.pack()

board_frame = tk.Frame(main_frame, bg=bg_color, pady=20)
board_frame.pack()

# Scorecard table
table_frame = tk.Frame(board_frame, bg=bg_color)
table_frame.grid(row=0, column=0)

categories_label = tk.Label(table_frame, text="Category", font=("Arial", 14, "bold"), bg=table_bg, borderwidth=1, relief="solid", width=25)
categories_label.grid(row=0, column=0, sticky="nsew")

score_label_header = tk.Label(table_frame, text="Score", font=("Arial", 14, "bold"), bg=table_bg, borderwidth=1, relief="solid", width=10)
score_label_header.grid(row=0, column=1, sticky="nsew")

score_labels = []
for i, category in enumerate(categories):
    category_label = tk.Label(table_frame, text=category, font=("Arial", 12), bg=table_bg, borderwidth=1, relief="solid", width=25)
    category_label.grid(row=i + 1, column=0, sticky="nsew")
    score_label = tk.Label(table_frame, text="0", font=("Arial", 12), bg=table_bg, borderwidth=1, relief="solid", width=10)
    score_label.grid(row=i + 1, column=1, sticky="nsew")
    score_label.bind("<Button-1>", lambda e, idx=i: select_category(idx))
    score_labels.append(score_label)

dice_frame = tk.Frame(board_frame, bg=bg_color)
dice_frame.grid(row=1, column=0, pady=20)

dice_labels = []
dice_selected = [False] * 5
for i in range(5):
    label = tk.Label(dice_frame, text="1", font=("Arial", 18, "bold"), bg=dice_color, width=4, height=2, relief="raised")
    label.grid(row=0, column=i, padx=5)
    label.bind("<Button-1>", lambda e, idx=i: toggle_dice(idx))
    dice_labels.append(label)

rolls_label = tk.Label(board_frame, text=f"Rolls Left: {rolls_left}", font=("Arial", 14), bg=bg_color, fg="white")
rolls_label.grid(row=2, column=0, pady=10)

roll_button = tk.Button(board_frame, text="ROLL", font=("Arial", 14, "bold"), command=roll_dice, bg="white", width=10)
roll_button.grid(row=3, column=0, pady=10)

restart_button = tk.Button(main_frame, text="Restart Game", font=("Arial", 12), command=restart_game, bg="white")
restart_button.pack(pady=10)

restart_game()
root.mainloop()
