import sys

print('')
print('')
print('')
print('')
print('')
print('')
print('')
print('')

print("=================    Welcome     ============")
print("=================    to the      ============")
print("=================      Tic       ============")
print("=================      Tac       ============")
print("=================      Toe       ============")
print("=================      Game      ============")

print('')
print('')
print('')
print('')
print('')

board = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
players=['X','O']

def print_borad():
    print("---+---+---")
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print("---+---+---")






print_borad()

turn = 1

for _ in range(len(board)):
    X_choice = 0
    if turn % 2 == 0:
        print("Player X's Turn: ")
        choice = int(input("Enter the position of marking..."))
        board[choice] = 'X'

        if board[0] == board[1] == board[2] == 'X':
            print("Player X has won")
            input("Press Enter to continue")
            sys.exit()
        elif board[0] == board[3] == board[6] == 'X':
            print("Player X has won   ")
            input("Press Enter to continue")
            sys.exit()
        elif board[0] == board[4] == board[8] == 'X':
            print("Player X has won   ")
            input("Press Enter to continue")
            sys.exit()
        elif board[2] == board[5] == board[8] == 'X':
            print("Player X has won")
            input("Press Enter to continue")
            sys.exit()
        elif board[2] == board[4] == board[6] == 'X' : 
            print("Player X has won")
            input("Press Enter to continue")
            sys.exit()
        elif board[2] == board[5] == board[8] == 'X':
            print("Player X has won")
            input("Press Enter to continue")
            sys.exit()    
        elif board[1] == board[4] == board[7] == 'X':
            print("Player X has won")
            input("Press Enter to continue")
            sys.exit()
        elif board[3] == board[4] == board[5] == 'X':
            print("Player X has won")
            input("Press Enter to continue")
            sys.exit()

    else:
        print("Player O's Turn: ")
        choice = int(input("Enter the position of marking..."))
        board[choice] = 'O'
        if board[0] == board[1] == board[2] == 'O':
            print("Player X has won")

        elif board[0] == board[3] == board[6] == 'O':                
            print("Player O has won   ")
            input("Press Enter to continue")
            sys.exit()
        elif board[0] == board[4] == board[8] == 'O':
            print("Player O has won   ")
            input("Press Enter to continue")
            sys.exit()
        elif board[2] == board[5] == board[8] == 'O':
            print("Player O has won")
            input("Press Enter to continue")
            sys.exit()
        elif board[2] == board[4] == board[6] == 'O':
            print("Player O has won")
            input("Press Enter to continue")
            sys.exit()
        elif board[2] == board[5] == board[8] == 'O':
            print("Player O has won")  
            input("Press Enter to continue")  
            sys.exit()
        elif board[1] == board[4] == board[7] == 'O':
            print("Player O has won")
            input("Press Enter to continue")
            sys.exit()
        elif board[3] == board[4] == board[5] == 'O':
            print("Player O has won")
            input("Press Enter to continue")
            sys.exit()
    print("\033c", end="")
    print_borad()
    turn += 1



