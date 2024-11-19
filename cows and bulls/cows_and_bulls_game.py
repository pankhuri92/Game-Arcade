import tkinter as tk
from tkinter import messagebox
import random

def load_words(file_path):
    """Load and return a list of 4-letter words from the provided file."""
    return [line.strip() for line in open(file_path)]

def filter_words(words, guess, cows, bulls):
    """Filter words based on cows and bulls feedback."""
    def match_cows_bulls(word):
        common = sum(min(guess.count(c), word.count(c)) for c in set(guess))
        match = sum(g == w for g, w in zip(guess, word))
        return match == bulls and (common - match) == cows

    return [word for word in words if match_cows_bulls(word)]

class CowsAndBullsGame:
    def __init__(self, master, file_path):
        self.master = master
        self.master.title("Cows and Bulls")
        self.master.configure(bg="#DCD3E2")  # Background color: Titan White
        self.words = load_words(file_path)
        self.best_starts = ['acre', 'pain', 'riot', 'mile', 'quit']
        self.current_guess = None
        self.attempts = 0

        # Centering the content
        self.frame = tk.Frame(master, bg="#DCD3E2", padx=20, pady=20)
        self.frame.pack(expand=True)  # Expands to center content

        # GUI Components
        self.instructions = tk.Label(
            self.frame,
            text="Think of a 4-letter word. I'll try to guess it!",
            font=("Helvetica", 16, "bold"),
            bg="#DCD3E2",
            fg="#333333"
        )
        self.instructions.pack(pady=10)

        self.guess_label = tk.Label(
            self.frame,
            text="My guess will appear here.",
            font=("Helvetica", 18, "bold"),
            bg="#DCD3E2",
            fg="#333333"
        )
        self.guess_label.pack(pady=10)

        self.bulls_label = tk.Label(self.frame, text="Enter Bulls (Correct letter & position):", bg="#DCD3E2", fg="#333333")
        self.bulls_label.pack()

        self.bulls_entry = tk.Entry(self.frame)
        self.bulls_entry.pack()

        self.cows_label = tk.Label(self.frame, text="Enter Cows (Correct letter, wrong position):", bg="#DCD3E2", fg="#333333")
        self.cows_label.pack()

        self.cows_entry = tk.Entry(self.frame)
        self.cows_entry.pack()

        self.submit_button = tk.Button(
            self.frame,
            text="Submit",
            command=self.submit_feedback,
            bg="#6D5271",  # Fedora color
            fg="white",
            font=("Helvetica", 12, "bold")
        )
        self.submit_button.pack(pady=10)

        self.new_game_button = tk.Button(
            self.frame,
            text="New Game",
            command=self.new_game,
            bg="#6D5271",  # Fedora color
            fg="white",
            font=("Helvetica", 12, "bold")
        )
        self.new_game_button.pack(pady=5)

        self.result_label = tk.Label(self.frame, text="", font=("Helvetica", 12, "italic"), bg="#DCD3E2", fg="#333333")
        self.result_label.pack(pady=10)

        # Start the game
        self.new_game()

    def make_guess(self):
        """Make a guess and display it."""
        if self.best_starts:
            self.current_guess = self.best_starts.pop(0)
        else:
            self.current_guess = random.choice(self.words) if self.words else None

        if self.current_guess:
            self.guess_label.config(text=f"My guess: {self.current_guess}")
        else:
            self.result_label.config(text="No more possible words. Let's restart!", fg="red")

    def submit_feedback(self):
        """Process user feedback and make the next guess."""
        try:
            bulls = int(self.bulls_entry.get())
            cows = int(self.cows_entry.get())

            if bulls == 4:
                messagebox.showinfo("Game Over", f"I guessed the word '{self.current_guess}' in {self.attempts + 1} tries!")
                self.new_game()
                return

            self.words = filter_words(self.words, self.current_guess, cows, bulls)
            self.attempts += 1
            self.bulls_entry.delete(0, tk.END)
            self.cows_entry.delete(0, tk.END)

            if not self.words:
                messagebox.showerror("Error", "No more possible words. Let's restart!")
                self.new_game()
            else:
                self.make_guess()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid integers for Bulls and Cows.")

    def new_game(self):
        """Reset the game."""
        self.words = load_words("four_letter_words.txt")
        self.best_starts = ['acre', 'pain', 'riot', 'mile', 'quit']
        self.current_guess = None
        self.attempts = 0
        self.result_label.config(text="")
        self.bulls_entry.delete(0, tk.END)
        self.cows_entry.delete(0, tk.END)
        self.make_guess()

# Create the GUI application
if __name__ == "__main__":
    root = tk.Tk()
    app = CowsAndBullsGame(root, "four_letter_words.txt")
    root.mainloop()
