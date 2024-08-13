from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import Games
import json
from . import db
from app.game_engine import create_checkers_board
from app.game_engine.computer_player import get_computer_move, checkers_notation_to_coord, coord_to_checkers_notation, make_move

game_blueprint = Blueprint('game', __name__)

def count_pieces(board):
    h_count = sum(row.count('h') for row in board)
    c_count = sum(row.count('c') for row in board)
    return h_count, c_count

def determine_turn(board):
    h_count = sum(row.count('h') + row.count('H') for row in board)
    c_count = sum(row.count('c') + row.count('C') for row in board)
    return 'h' if h_count >= c_count else 'c'

@game_blueprint.route("/game/board", methods=["GET"])
@jwt_required()
def get_board():
    current_user = get_jwt_identity()
    game = Games.query.filter_by(player_id=current_user['id']).first()

    if not game:
        initial_board_state = create_checkers_board()
        new_game = Games(player_id=current_user['id'], board_state=json.dumps(initial_board_state), moves_without_capture=0)
        db.session.add(new_game)
        db.session.commit()
        game = new_game

    board = json.loads(game.board_state)
    current_turn = determine_turn(board)
    print_board(board)
    return jsonify({
        'message': f"Hi {current_user['username']}, this is your board", 
        'board': board,
        'current_turn': current_turn,
        'moves_without_capture': game.moves_without_capture
    })

@game_blueprint.route("/game/make_human_move", methods=["PUT"])
@jwt_required()
def make_human_move():
    try:
        data = request.get_json()
        current_user = get_jwt_identity()
        game = Games.query.filter_by(player_id=current_user['id']).first()

        if not game:
            return jsonify({'message': 'Game not found'}), 404

        if game.game_over:
            return jsonify({
                'message': 'This game has already ended',
                'game_over': True,
                'winner': game.winner
            }), 400

        board = json.loads(game.board_state)

        # Human move
        src = data['src']
        dest = data['dest']
        src_row, src_col = checkers_notation_to_coord(src)
        dest_row, dest_col = checkers_notation_to_coord(dest)

        print("Initial board state:")
        print_board(board)

        # Apply human move
        move_result = perform_move(board, (src_row, src_col), (dest_row, dest_col))
        if not move_result['success']:
            return jsonify({'message': move_result['message']}), 400

        # Check if the human move was a capture
        human_capture = move_result.get('capture', False)

        print(f"Human capture: {human_capture}") 
        print("Board after human move:")
        print_board(board)

        # Update moves_without_capture
        if human_capture:
            game.moves_without_capture = 0
        else:
            game.moves_without_capture += 1

        # Save the updated board state
        game.board_state = json.dumps(board)

        # Check for game over
        h_count = sum(row.count('h') + row.count('H') for row in board)
        c_count = sum(row.count('c') + row.count('C') for row in board)
        
        if c_count == 0:
            game.game_over = True
            game.winner = 'human'
        elif game.moves_without_capture >= 40:  # Draw condition
            game.game_over = True
            game.winner = 'draw'

        db.session.commit()

        return jsonify({
            'message': 'Human move made successfully', 
            'board': board,
            'game_over': game.game_over,
            'winner': game.winner,
            'moves_without_capture': game.moves_without_capture
        })

    except Exception as e:
        print(f"Error in make_human_move: {str(e)}")
        return jsonify({'message': 'An error occurred while making the human move'}), 500

@game_blueprint.route("/game/make_computer_move", methods=["GET"])
@jwt_required()
def make_computer_move():
    try:
        current_user = get_jwt_identity()
        game = Games.query.filter_by(player_id=current_user['id']).first()

        if not game:
            return jsonify({'message': 'Game not found'}), 404

        if game.game_over:
            return jsonify({
                'message': 'This game has already ended',
                'game_over': True,
                'winner': game.winner
            }), 400

        board = json.loads(game.board_state)

        # Computer's turn
        computer_moves = []
        computer_move, checkers_notation = get_computer_move(board)
        capture_occurred = False

        if computer_move:
            print(f"Computer move: {checkers_notation}")
            try:
                board, capture_occurred = make_move(board, computer_move)
            except ValueError as e:
                print(f"Error in make_move: {str(e)}")
                return jsonify({'message': f'Error in computer move: {str(e)}'}), 400
            except Exception as e:
                print(f"Unexpected error in make_move: {str(e)}")
                return jsonify({'message': f'Unexpected error in computer move: {str(e)}'}), 500

            print(f"Computer capture: {capture_occurred}")
            print("Board after computer move:")
            print_board(board)
            computer_moves.append(checkers_notation)
        else:
            print("No valid computer move found")
            return jsonify({'message': 'No valid computer move found'}), 400

        # Update moves_without_capture
        if capture_occurred:
            game.moves_without_capture = 0
        else:
            game.moves_without_capture += 1

        # Save the updated board state
        game.board_state = json.dumps(board)

        # Check for game over
        h_count = sum(row.count('h') + row.count('H') for row in board)
        c_count = sum(row.count('c') + row.count('C') for row in board)
        
        if h_count == 0:
            game.game_over = True
            game.winner = 'computer'
        elif game.moves_without_capture >= 40:  # Draw condition
            game.game_over = True
            game.winner = 'draw'

        db.session.commit()

        return jsonify({
            'message': 'Computer move made successfully', 
            'board': board,
            'game_over': game.game_over,
            'winner': game.winner,
            'computer_moves': computer_moves,
            'moves_without_capture': game.moves_without_capture
        })

    except Exception as e:
        print(f"Error in make_computer_move: {str(e)}")
        return jsonify({'message': 'An error occurred while making the computer move'}), 500

@game_blueprint.route("/game/possible_moves", methods=["GET"])
@jwt_required()
def get_possible_moves():
    current_user = get_jwt_identity()
    game = Games.query.filter_by(player_id=current_user['id']).first()

    if not game:
        return jsonify({'message': 'Game not found'}), 404

    board = json.loads(game.board_state)
    possible_moves = get_possible_human_moves(board)

    return jsonify({
        'possible_moves': possible_moves
    })

def get_possible_human_moves(board):
    possible_moves = []
    for row in range(8):
        for col in range(8):
            if board[row][col].lower() == 'h':
                piece_moves = get_piece_moves(board, row, col)
                if piece_moves:
                    from_pos = coord_to_checkers_notation(row, col)
                    for to_pos in piece_moves:
                        possible_moves.append({
                            'from': from_pos,
                            'to': coord_to_checkers_notation(to_pos[0], to_pos[1])
                        })
    return possible_moves

def get_piece_moves(board, row, col):
    moves = []
    piece = board[row][col]
    is_king = piece.isupper()
    directions = [(-1, -1), (-1, 1)] if not is_king else [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    
    # Check for normal moves
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 8 and 0 <= new_col < 8 and board[new_row][new_col] == ' ':
            moves.append((new_row, new_col))
    
    # Check for capture moves
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 8 and 0 <= new_col < 8 and board[new_row][new_col].lower() == 'c':
            jump_row, jump_col = new_row + dr, new_col + dc
            if 0 <= jump_row < 8 and 0 <= jump_col < 8 and board[jump_row][jump_col] == ' ':
                moves.append((jump_row, jump_col))
    
    return moves

@game_blueprint.route("/game/reset", methods=["POST"])
@jwt_required()
def reset_game():
    current_user = get_jwt_identity()
    game = Games.query.filter_by(player_id=current_user['id']).first()

    if not game:
        return jsonify({'message': 'No game found to reset'}), 404

    # Create a fresh board to compare with
    initial_board_state = create_checkers_board()

    # Check if the current board is already in the initial state
    if (game.board_state == json.dumps(initial_board_state) and
        game.moves_without_capture == 0 and
        not game.game_over and
        game.winner is None):
        print("Reset attempted, but board was already in initial state.")
        return jsonify({'message': 'Board was already reset'}), 400

    # If not in initial state, reset the game
    game.board_state = json.dumps(initial_board_state)
    game.moves_without_capture = 0
    game.game_over = False
    game.winner = None

    db.session.commit()

    print("Game has been reset!")
    print("Fresh board state:")
    print_board(initial_board_state)

    return jsonify({
        'message': 'Game has been reset',
        'board': initial_board_state,
        'current_turn': 'h',
        'moves_without_capture': 0,
        'game_over': False
    })

def print_board(board):
    print("   A   B   C   D   E   F   G   H")
    print(" +---+---+---+---+---+---+---+---+")
    for i, row in enumerate(board):
        print(f"{i+1}|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print(f"\n +---+---+---+---+---+---+---+---+")

def perform_move(board, src, dest):
    src_row, src_col = src
    dest_row, dest_col = dest

    # Check if the source position contains a human piece
    if board[src_row][src_col].lower() != 'h':
        return {'success': False, 'message': 'You can only move your own pieces'}

    is_king = board[src_row][src_col].isupper()

    # Check if the destination is empty
    if board[dest_row][dest_col] != ' ':
        return {'success': False, 'message': 'The destination square is not empty'}

    # Check if the move is diagonal
    if abs(src_row - dest_row) != abs(src_col - dest_col):
        return {'success': False, 'message': 'Moves must be diagonal'}

    # Check if the move is forward (for non-king pieces)
    if not is_king and dest_row >= src_row:
        return {'success': False, 'message': 'Regular pieces can only move forward'}

    # Check if the move is a single step or a valid capture
    if abs(src_row - dest_row) > 2:
        return {'success': False, 'message': 'Invalid move distance'}

    # Check for capture move
    capture = False
    if abs(src_row - dest_row) == 2:
        captured_row = (src_row + dest_row) // 2
        captured_col = (src_col + dest_col) // 2
        if board[captured_row][captured_col].lower() != 'c':
            return {'success': False, 'message': 'Invalid capture move'}
        capture = True

    # Move is valid, update the board
    piece = board[src_row][src_col]
    board[dest_row][dest_col] = piece
    board[src_row][src_col] = ' '

    # Handle captures
    if capture:
        board[captured_row][captured_col] = ' '

    # Promote to king if reached the opposite end
    if piece.lower() == 'h' and dest_row == 0:
        board[dest_row][dest_col] = piece.upper()

    return {'success': True, 'capture': capture}
