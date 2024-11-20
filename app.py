import tkinter as tk
import subprocess

# Functions to start games
def start_yahtzee():
    subprocess.run(["python", "yahtzee/yahtzee_game.py"])  # Replace with your Yahtzee game file path

def start_cows_and_bulls():
    subprocess.run(["python", "cows and bulls/cows_and_bulls_game.py"])  # Replace with your Cows and Bulls game file path

def start_diamonds():
    subprocess.run(["python", "diamonds/diamonds_game.py"])  # Replace with your Diamonds game file path

def start_sudoku():
    subprocess.run(["python", "sudoku/main_duko.py"])  # Replace with your Sudoku game file path

# Create main menu window
root = tk.Tk()
root.title("Game Arcade")
root.geometry("400x600")
root.configure(bg="#B2D9C4")

# Title
title_label = tk.Label(root, text="Game Arcade", font=("Arial", 24, "bold"), bg="#B2D9C4", fg="black")
title_label.pack(pady=20)

# Game boxes
box_font = ("Arial", 16, "bold")
box_width = 20
box_height = 2
box_pad = 20

yahtzee_button = tk.Button(root, text="Yahtzee", font=box_font, bg="#247D7F", fg="white", width=box_width, height=box_height, command=start_yahtzee)
yahtzee_button.pack(pady=box_pad)

cows_and_bulls_button = tk.Button(root, text="Cows and Bulls", font=box_font, bg="#247D7F", fg="white", width=box_width, height=box_height, command=start_cows_and_bulls)
cows_and_bulls_button.pack(pady=box_pad)

diamonds_button = tk.Button(root, text="Diamonds", font=box_font, bg="#247D7F", fg="white", width=box_width, height=box_height, command=start_diamonds)
diamonds_button.pack(pady=box_pad)

sudoku_button = tk.Button(root, text="Sudoku", font=box_font, bg="#247D7F", fg="white", width=box_width, height=box_height, command=start_sudoku)
sudoku_button.pack(pady=box_pad)

# Run main loop
root.mainloop()
