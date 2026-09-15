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





print("\033c", end="")

print_borad()

turn = 1

for _ in range(len(board)):
    mark = 0
    if turn % 2 == 0:
        print("Player X's Turn: ")
        print("Enter the position of marking...")
    else:
        print("Player O's Turn: ")
        print("Enter the position of marking...")

    turn += 1
