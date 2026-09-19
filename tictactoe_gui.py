"""A two-player tic-tac-toe game with a Tkinter GUI.

This is the GUI version, using the same logic as the CLI version in tic_tac_toe/tic_tac_toe.py.
"""

import tkinter as tk
from tkinter import messagebox

WINNING_LINES = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)


def check_winner(board):
    """Return 'X', 'O', or None to indicate the winner (or ongoing game)."""
    for player in ("X", "O"):
        for line in WINNING_LINES:
            if all(board[i] == player for i in line):
                return player
    return None


def check_tie(board):
    """Return True if the board is full with no winner."""
    return all(cell != " " for cell in board)


class TicTacToeGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.window.resizable(False, False)

        # Game state
        self.board = [" "] * 9
        self.buttons = [None] * 9
        self.current_player = "X"
        self.game_over = False

        self.create_widgets()

    def create_widgets(self):
        # Status label
        self.status_label = tk.Label(
            self.window,
            text=f"Player {self.current_player}'s turn",
            font=("Helvetica", 16, "bold"),
        )
        self.status_label.grid(row=0, column=0, columnspan=3, pady=(10, 5), padx=10)

        # 3x3 grid of buttons
        for i in range(9):
            row, col = divmod(i, 3)
            button = tk.Button(
                self.window,
                text=" ",
                font=("Helvetica", 36, "bold"),
                width=4,
                height=1,
                relief=tk.RAISED,
                bd=3,
                command=lambda idx=i: self.on_click(idx),
            )
            # Use padding to evenly space buttons
            grid_row = row + 1
            button.grid(row=grid_row, column=col, padx=3, pady=3)
            self.buttons[i] = button

        # Control buttons
        reset_btn = tk.Button(
            self.window,
            text="Reset",
            font=("Helvetica", 12, "bold"),
            command=self.reset_game,
            width=10,
            height=1,
        )
        reset_btn.grid(row=4, column=0, columnspan=3, pady=(10, 5))

        # Apply padding to rows 1-3 to center the grid
        for r in range(1, 4):
            self.window.grid_rowconfigure(r, weight=1)

    def on_click(self, index):
        if self.game_over or self.board[index] != " ":
            return

        # Record the move
        self.board[index] = self.current_player
        self.buttons[index].config(
            text=self.current_player,
            state=tk.DISABLED,
            fg="#2E7D32" if self.current_player == "X" else "#1565C0",
        )

        # Check for winner
        winner = check_winner(self.board)
        if winner:
            self.highlight_winning_line(winner)
            self.status_label.config(
                text=f"Player {winner} wins! Click Reset to play again.",
                fg="#2E7D32" if winner == "X" else "#1565C0",
            )
            messagebox.showinfo("Game Over", f"Player {winner} wins!")
            self.game_over = True
            return

        # Check for tie
        if check_tie(self.board):
            self.status_label.config(text="It's a tie! Click Reset to play again.")
            messagebox.showinfo("Game Over", "It's a tie!")
            self.game_over = True
            return

        # Switch player
        self.current_player = "O" if self.current_player == "X" else "X"
        self.status_label.config(f"Player {self.current_player}'s turn")

    def highlight_winning_line(self, winner):
        """Highlight the winning combination in light blue."""
        for line in WINNING_LINES:
            if all(self.board[i] == winner for i in line):
                for i in line:
                    self.buttons[i].config(bg="#BBDEFB")
                break

    def reset_game(self):
        self.board = [" "] * 9
        self.current_player = "X"
        self.game_over = False

        for i, button in enumerate(self.buttons):
            button.config(
                text=" ",
                state=tk.NORMAL,
                bg="SystemButtonFace",
                fg="black",
            )

        self.status_label.config(
            text=f"Player {self.current_player}'s turn",
            fg="black",
        )

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = TicTacToeGUI()
    app.run()