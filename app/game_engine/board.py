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
            
def display_board(board):
    print("  A B C D E F G H")
    print(" +-----------------+")
    for i in range(8):
        print(f"{i + 1}|", ' '.join(board[i]), "|")  # Adjusted to print rows 1-8 in order
        print(" +-----------------+")

checkers_board = create_board()
display_board(checkers_board)                 

