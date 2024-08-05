def create_checkers_board():
    # 8x8 board
    board = [[' ' for _ in range(8)] for _ in range(8)]
    
    # Fill the board with initial pieces (c for computer player, h for the human player)
    for row in range(8):
        if row < 3:  # First three rows for Computer piece
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = 'c'  # Computer piece
        elif row > 4:  # Last three rows for Human pieces
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = 'h'  # Human pieces

    return board

def display_board(board):
    print("   A   B   C   D   E   F   G   H")
    print(" +---+---+---+---+---+---+---+---+")
    for row_index, row in enumerate(board):
        row_str = f"{row_index + 1}|"
        for cell in row:
            row_str += f" {cell} |"
        print(row_str)
        print(" +---+---+---+---+---+---+---+---+")


# Create and print the checkers board
checkers_board = create_checkers_board()
display_board(checkers_board)
               

