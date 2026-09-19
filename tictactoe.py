"""A two-player tic-tac-toe game with a Tkinter GUI."""

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


class TicTacToeGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe")
        self.window.resizable(False, False)

        self.current_player = "X"
        self.board = [" "] * 9
        self.buttons = [None] * 9
        self.game_over = False

        self.create_widgets()
        self.window.mainloop()

    def create_widgets(self):
        # Header label showing current player's turn
        self.label = tk.Label(
            self.window,
            text="Player X's turn",
            font=("Arial", 18),
        )
        self.label.grid(row=0, column=0, columnspan=3, pady=(10, 5))

        # 3x3 grid of buttons using position indices 0-8
        for i in range(9):
            row, col = divmod(i, 3)
            button = tk.Button(
                self.window,
                text=" ",
                font=("Arial", 36),
                width=4,
                height=1,
                bg="#f0f0f0",
                activebackground="#e0e0e0",
                command=lambda idx=i: self.on_click(idx),
            )
            button.grid(row=row + 1, column=col, padx=2, pady=2)
            self.buttons[i] = button

        # Reset button
        reset_button = tk.Button(
            self.window,
            text="Reset",
            font=("Arial", 14),
            command=self.reset_game,
        )
        reset_button.grid(row=4, column=0, columnspan=3, pady=(10, 10))

    def on_click(self, index):
        if self.game_over or self.board[index] != " ":
            return

        self.board[index] = self.current_player
        self.buttons[index].config(
            text=self.current_player,
            fg="#008000" if self.current_player == "X" else "#0000FF",
            disabledforeground="#008000" if self.current_player == "X" else "#0000FF",
        )
        self.buttons[index].config(state=tk.DISABLED)

        if self.check_winner(self.current_player):
            self.highlight_winner()
            self.label.config(text=f"Player {self.current_player} wins!")
            messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
            self.game_over = True
        elif self.check_tie():
            self.label.config(text="It's a tie!")
            messagebox.showinfo("Game Over", "It's a tie!")
            self.game_over = True
        else:
            self.current_player = "O" if self.current_player == "X" else "X"
            self.label.config(text=f"Player {self.current_player}'s turn")

    def check_winner(self, player):
        return any(
            all(self.board[i] == player for i in line) for line in WINNING_LINES
        )

    def check_tie(self):
        return all(cell != " " for cell in self.board)

    def highlight_winner(self):
        """Highlight the winning line in yellow."""
        for line in WINNING_LINES:
            if all(self.board[i] == self.current_player for i in line):
                for i in line:
                    self.buttons[i].config(bg="#FFD700")
                break

    def reset_game(self):
        self.current_player = "X"
        self.board = [" "] * 9
        self.game_over = False
        self.label.config(text="Player X's turn")
        for i in range(9):
            self.buttons[i].config(
                text=" ",
                state=tk.NORMAL,
                bg="#f0f0f0",
                disabledforeground="black",
            )


if __name__ == "__main__":
    TicTacToeGUI()
