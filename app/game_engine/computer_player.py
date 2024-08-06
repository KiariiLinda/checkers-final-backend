import copy

def coord_to_checkers_notation(row, col):
    return f"{chr(col + ord('A'))}{row + 1}"

def checkers_notation_to_coord(notation):
    col = ord(notation[0].upper()) - ord('A')
    row = int(notation[1]) - 1
    return row, col

def minimax(board, depth, maximizing_player):
    if depth == 0 or game_over(board):
        return evaluate_board(board), None

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in get_all_possible_moves(board, 'c'):
            new_board = make_move(board, move)
            eval, _ = minimax(new_board, depth - 1, False)
            if eval > max_eval:
                max_eval = eval
                best_move = move
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for move in get_all_possible_moves(board, 'h'):
            new_board = make_move(board, move)
            eval, _ = minimax(new_board, depth - 1, True)
            if eval < min_eval:
                min_eval = eval
                best_move = move
        return min_eval, best_move  

def get_computer_move(board):
    print("Getting computer move for board:")
    print_board(board)
    possible_moves = get_all_possible_moves(board, 'c')
    print("Possible moves for computer:")
    for move in possible_moves:
        src, dest = move
        print(f"{coord_to_checkers_notation(*src)} to {coord_to_checkers_notation(*dest)}", end=", ")
    print()

    if possible_moves:
        _, best_move = minimax(board, depth=3, maximizing_player=True)
        src, dest = best_move
        
        # Convert to checkers notation
        checkers_notation = f"{coord_to_checkers_notation(*src)} to {coord_to_checkers_notation(*dest)}"
        print(f"Computer chose move: {checkers_notation}")
        return best_move, checkers_notation
    else:
        print("No valid moves found for computer")
        return None, None

def evaluate_board(board):
    c_count = sum(row.count('c') for row in board)
    h_count = sum(row.count('h') for row in board)
    return c_count - h_count

def game_over(board):
    return get_all_possible_moves(board, 'c') == [] and get_all_possible_moves(board, 'h') == []

def get_all_possible_moves(board, player):
    moves = []
    for row in range(8):
        for col in range(8):
            if board[row][col].lower() == player:  # Check for both 'c' and 'C' for computer
                is_king = board[row][col].isupper()  # Assume king pieces are uppercase
                   
                # Define move directions based on player and piece type
                if player == 'c':
                    directions = [(1, -1), (1, 1)] if not is_king else [(-1, -1), (-1, 1), (1, -1), (1, 1)]
                else:  # player == 'h'
                    directions = [(-1, -1), (-1, 1)] if not is_king else [(-1, -1), (-1, 1), (1, -1), (1, 1)]

                for dr, dc in directions:
                    new_row, new_col = row + dr, col + dc
                    if 0 <= new_row < 8 and 0 <= new_col < 8 and board[new_row][new_col] == ' ':
                        moves.append(((row, col), (new_row, new_col)))
                    
                    # Check for jumps
                    jump_row, jump_col = row + 2*dr, col + 2*dc
                    if (0 <= jump_row < 8 and 0 <= jump_col < 8 and
                        board[jump_row][jump_col] == ' ' and
                        board[new_row][new_col] != ' ' and
                        board[new_row][new_col] != player):
                        moves.append(((row, col), (jump_row, jump_col)))
    return moves

def get_possible_moves(board, row, col):
    moves = []
    directions = [(1, -1), (1, 1)] if board[row][col] == 'c' else [(-1, -1), (-1, 1)]
    
    for dx, dy in directions:
        new_row, new_col = row + dx, col + dy
        if 0 <= new_row < 8 and 0 <= new_col < 8 and board[new_row][new_col] == ' ':
            moves.append(((row, col), (new_row, new_col)))
        
        # Check for captures
        jump_row, jump_col = new_row + dx, new_col + dy
        if (0 <= jump_row < 8 and 0 <= jump_col < 8 and
            board[new_row][new_col] != ' ' and
            board[new_row][new_col] != board[row][col] and
            board[jump_row][jump_col] == ' '):
            moves.append(((row, col), (jump_row, jump_col)))
    
    return moves

def make_move(board, move):
    new_board = copy.deepcopy(board)
    start, end = move
    start_row, start_col = start
    end_row, end_col = end

    # Move the piece
    piece = new_board[start_row][start_col]
    new_board[end_row][end_col] = piece
    new_board[start_row][start_col] = ' '

    # Handle captures
    if abs(start_row - end_row) == 2:
        mid_row = (start_row + end_row) // 2
        mid_col = (start_col + end_col) // 2
        new_board[mid_row][mid_col] = ' '  # Remove the captured piece

    # Promote to king if reached the opposite end
    if (piece == 'c' and end_row == 7) or (piece == 'h' and end_row == 0):
        new_board[end_row][end_col] = piece.upper()

    return new_board

def print_board(board):
    print("   A   B   C   D   E   F   G   H")
    print(" +---+---+---+---+---+---+---+---+")
    for row_index, row in enumerate(board):
        row_str = f"{row_index + 1}|"
        for cell in row:
            row_str += f" {cell} |"
        print(row_str)
        print(" +---+---+---+---+---+---+---+---+")