# import sys

# print('')
# print('')
# print('')
# print('')
# print('')
# print('')
# print('')
# print('')

# print("=================    Welcome     ============")
# print("=================    to the      ============")
# print("=================      Tic       ============")
# print("=================      Tac       ============")
# print("=================      Toe       ============")
# print("=================      Game      ============")

# print('')
# print('')
# print('')
# print('')
# print('')

# board = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
# players=['X','O']

# def print_borad():
#     print("---+---+---")
#     print(f" {board[0]} | {board[1]} | {board[2]} ")
#     print("---+---+---")
#     print(f" {board[3]} | {board[4]} | {board[5]} ")
#     print("---+---+---")
#     print(f" {board[6]} | {board[7]} | {board[8]} ")
#     print("---+---+---")






# print_borad()

# turn = 1

# for _ in range(len(board)):
#     X_choice = 0
#     if turn % 2 == 0:
#         print("Player X's Turn: ")
#         choice = int(input("Enter the position of marking..."))
#         board[choice] = 'X'

#         if board[0] == board[1] == board[2] == 'X':
#             print("Player X has won")
#             input("Press Enter to continue")
#             sys.exit()
#         elif board[0] == board[3] == board[6] == 'X':
#             print("Player X has won   ")
#             input("Press Enter to continue")
#             sys.exit()
#         elif board[0] == board[4] == board[8] == 'X':
#             print("Player X has won   ")
#             input("Press Enter to continue")
#             sys.exit()
#         elif board[2] == board[5] == board[8] == 'X':
#             print("Player X has won")
#             input("Press Enter to continue")
#             sys.exit()
#         elif board[2] == board[4] == board[6] == 'X' : 
#             print("Player X has won")
#             input("Press Enter to continue")
#             sys.exit()
#         elif board[2] == board[5] == board[8] == 'X':
#             print("Player X has won")
#             input("Press Enter to continue")
#             sys.exit()    
#         elif board[1] == board[4] == board[7] == 'X':
#             print("Player X has won")
#             input("Press Enter to continue")
#             sys.exit()
#         elif board[3] == board[4] == board[5] == 'X':
#             print("Player X has won")
#             input("Press Enter to continue")
#             sys.exit()

#     else:
#         print("Player O's Turn: ")
#         choice = int(input("Enter the position of marking..."))
#         board[choice] = 'O'
#         if board[0] == board[1] == board[2] == 'O':
#             print("Player X has won")

#         elif board[0] == board[3] == board[6] == 'O':                
#             print("Player O has won   ")
#             input("Press Enter to continue")
#             sys.exit()
#         elif board[0] == board[4] == board[8] == 'O':
#             print("Player O has won   ")
#             input("Press Enter to continue")
#             sys.exit()
#         elif board[2] == board[5] == board[8] == 'O':
#             print("Player O has won")
#             input("Press Enter to continue")
#             sys.exit()
#         elif board[2] == board[4] == board[6] == 'O':
#             print("Player O has won")
#             input("Press Enter to continue")
#             sys.exit()
#         elif board[2] == board[5] == board[8] == 'O':
#             print("Player O has won")  
#             input("Press Enter to continue")  
#             sys.exit()
#         elif board[1] == board[4] == board[7] == 'O':
#             print("Player O has won")
#             input("Press Enter to continue")
#             sys.exit()
#         elif board[3] == board[4] == board[5] == 'O':
#             print("Player O has won")
#             input("Press Enter to continue")
#             sys.exit()
#     print("\033c", end="")
#     print_borad()
#     turn += 1

import tkinter as tk
from tkinter import messagebox

class TicTacToeGUI:
    def __init__(self):
        # 1. Setup the main window
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe")
        
        # Game state variables
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        
        # 2. Build the visual grid
        self.create_board()
        
        # 3. Start the event loop (waits for clicks)
        self.window.mainloop()

    def create_board(self):
        # Create a 3x3 grid of buttons
        for row in range(3):
            for col in range(3):
                button = tk.Button(
                    self.window, 
                    text="", 
                    font=('Arial', 40), 
                    width=5, height=2,
                    # lambda passes the specific row/col to the click function
                    command=lambda r=row, c=col: self.on_click(r, c)
                )
                button.grid(row=row, column=col)
                self.buttons[row][col] = button

    def on_click(self, row, col):
        # Ignore click if the spot is already taken
        if self.board[row][col] != "":
            return

        # Update the backend board and the frontend button
        self.board[row][col] = self.current_player
        self.buttons[row][col].config(text=self.current_player)

        # Check for a win or tie after every move
        if self.check_win(self.current_player):
            messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
            self.reset_game()
        elif self.check_tie():
            messagebox.showinfo("Game Over", "It's a tie!")
            self.reset_game()
        else:
            # Switch turns
            self.current_player = "O" if self.current_player == "X" else "X"

    def check_win(self, player):
        # Check rows, columns, and diagonals
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)): return True # Rows
            if all(self.board[j][i] == player for j in range(3)): return True # Columns
        
        if all(self.board[i][i] == player for i in range(3)): return True     # Main diagonal
        if all(self.board[i][2-i] == player for i in range(3)): return True   # Anti-diagonal
        return False

    def check_tie(self):
        # Tie happens if there are no empty spaces left
        return all(self.board[r][c] != "" for r in range(3) for c in range(3))

    def reset_game(self):
        # Clear the backend board and frontend buttons
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text="")

# Run the game
if __name__ == "__main__":
    TicTacToeGUI()

