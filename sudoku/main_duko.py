import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk

# Solved Sudoku board using backtracking
def solve_sudoku(board):
    empty = find_empty(board)
    if not empty:
        return True
    row, col = empty

    for num in range(1, 10):
        if is_valid(board, num, (row, col)):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0
    return False

# Check if a number is valid in a given position
def is_valid(board, num, pos):
    row, col = pos
    if num in board[row]:
        return False
    if num in [board[i][col] for i in range(9)]:
        return False
    box_x, box_y = col // 3, row // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num:
                return False
    return True

# Find the next empty cell
def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

# Create a partially filled Sudoku board
def generate_puzzle():
    board = [[0 for _ in range(9)] for _ in range(9)]
    for _ in range(15):
        row, col = random.randint(0, 8), random.randint(0, 8)
        num = random.randint(1, 9)
        if is_valid(board, num, (row, col)):
            board[row][col] = num
    solve_sudoku(board)
    for _ in range(45):
        row, col = random.randint(0, 8), random.randint(0, 8)
        board[row][col] = 0
    return board

# Main Game Class
class HarryPotterSudoku:
    def __init__(self, root):
        self.root = root
        self.root.title("Harry Potter Sudoku")
        self.board = generate_puzzle()
        self.original_board = [row[:] for row in self.board]
        self.house_color = "#7F0909"  # Default Gryffindor color
        self.create_ui()

    def create_ui(self):
        # Load and display background image
        bg_image = Image.open("sudoku/hogwarts_background.jpg")
        bg_image = bg_image.resize((600, 700), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        self.bg_label = tk.Label(self.root, image=bg_photo)
        self.bg_label.image = bg_photo
        self.bg_label.place(relwidth=1, relheight=1)

        # House selection dropdown
        self.house_var = tk.StringVar()
        self.house_var.set("Gryffindor")
        house_menu = tk.OptionMenu(
            self.root, 
            self.house_var, 
            "Gryffindor", "Slytherin", "Ravenclaw", "Hufflepuff",
            command=self.change_house_color
        )
        house_menu.config(font=("Arial", 12), bg="#EEE117", fg="black")
        house_menu.pack(pady=10)

        # Sudoku grid
        self.grid_frame = tk.Frame(self.root, bg=self.house_color)
        self.grid_frame.pack(pady=20)

        self.cells = []
        for i in range(9):
            row = []
            for j in range(9):
                bg_color = "#FFD700" if (i // 3 + j // 3) % 2 == 0 else "#FFF8DC"
                fg_color = "#000000" if self.original_board[i][j] != 0 else "#0000FF"  # Pre-filled black, input blue
                cell = tk.Entry(
                    self.grid_frame,
                    width=2,
                    font=("Arial", 18),
                    justify="center",
                    bg=bg_color,
                    fg=fg_color
                )
                cell.grid(row=i, column=j, padx=5, pady=5)
                if self.original_board[i][j] != 0:
                    cell.insert(0, str(self.original_board[i][j]))
                    cell.config(state="disabled", fg="#000000")  # Black for pre-filled cells
                else:
                    cell.bind("<FocusOut>", self.on_focus_out)  # Trigger to change text color on entry
                row.append(cell)
            self.cells.append(row)

        # Controls
        self.control_frame = tk.Frame(self.root, bg=self.house_color)
        self.control_frame.pack(pady=10)

        tk.Button(
            self.control_frame, text="Check", command=self.check_solution,
            bg="#00A651", fg="purple", font=("Arial", 12)
        ).pack(side="left", padx=10)

        tk.Button(
            self.control_frame, text="Hint", command=self.give_hint,
            bg="#FFC107", fg="black", font=("Arial", 12)
        ).pack(side="left", padx=10)

        tk.Button(
            self.control_frame, text="Reset", command=self.reset_board,
            bg="#D32F2F", fg="purple", font=("Arial", 12)
        ).pack(side="left", padx=10)

    def check_solution(self):
        for i in range(9):
            for j in range(9):
                val = self.cells[i][j].get()
                if not val.isdigit() or not is_valid(self.board, int(val), (i, j)):
                    messagebox.showerror("Error", f"Invalid entry at ({i+1}, {j+1})!")
                    return
                self.board[i][j] = int(val)

        if solve_sudoku(self.board):
            messagebox.showinfo("Success", "Congratulations! You've completed the puzzle!")
        else:
            messagebox.showerror("Error", "The solution is incorrect!")

    def reset_board(self):
        for i in range(9):
            for j in range(9):
                self.cells[i][j].config(state="normal")
                self.cells[i][j].delete(0, "end")
                if self.original_board[i][j] != 0:
                    self.cells[i][j].insert(0, str(self.original_board[i][j]))
                    self.cells[i][j].config(state="disabled")

    def give_hint(self):
        empty_cells = [
            (i, j)
            for i in range(9)
            for j in range(9)
            if self.original_board[i][j] == 0
        ]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.cells[i][j].insert(0, str(self.board[i][j]))
            self.cells[i][j].config(state="disabled")
        else:
            messagebox.showinfo("Hint", "No more hints available!")

    def on_focus_out(self, event):
        """Change user-entered numbers to black for visibility."""
        if event.widget.get().isdigit():
            event.widget.config(fg="#000000")  # Black for user-entered text

    def change_house_color(self, selected_house):
        house_colors = {
            "Gryffindor": "#7F0909",
            "Slytherin": "#2A623D",
            "Ravenclaw": "#222F5B",
            "Hufflepuff": "#EEE117"
        }
        self.house_color = house_colors[selected_house]
        self.grid_frame.config(bg=self.house_color)
        self.control_frame.config(bg=self.house_color)


if __name__ == "__main__":
    root = tk.Tk()
    game = HarryPotterSudoku(root)
    root.mainloop()
