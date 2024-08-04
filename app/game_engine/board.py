def create_board():
    # 8x8 board
  board = [[' ' for _ in range(8)] for _ in range(8)]
  # Fill the board with initial pieces (● for computer player,  ○for the human player)
  for row in range(8):
    if row < 3:  # First three rows for Computer piece
        for col in range(8):
            if (row + col) % 2 == 1:
                board[row][col] = '●'  # Computer piece
    elif row > 4:  # Last three rows for Human pieces
        for col in range(8):
            if (row + col) % 2 == 1:
                board[row][col] = '○'  # Human pieces
  return board

#Create and print the checkers board            
def display_board(board):
    print("    A   B   C   D   E   F   G   H")
    print("  +---+---+---+---+---+---+---+---+")
    for idx, row in enumerate(board):
        print(f"{idx+1} | {' | '.join(row)} | {idx+1}")
        print("  +---+---+---+---+---+---+---+---+")
    print("    A   B   C   D   E   F   G   H")   
   
checkers_board = create_board()
display_board(checkers_board)                 

