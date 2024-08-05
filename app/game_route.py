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
        new_game = Games(player_id=current_user['id'], board_state=json.dumps(initial_board_state))
        db.session.add(new_game)
        db.session.commit()
        game = new_game

    board = json.loads(game.board_state)
    current_turn = determine_turn(board)
    print_board(board)
    return jsonify({
        'message': f"Hi {current_user['username']}, this is your board", 
        'board': board,
        'current_turn': current_turn
    })

@game_blueprint.route("/game/make_move", methods=["PUT"])
@jwt_required()
def make_move_route():  # Renamed to avoid conflict with imported make_move
    try:
        data = request.get_json()
        current_user = get_jwt_identity()
        game = Games.query.filter_by(player_id=current_user['id']).first()

        if not game:
            return jsonify({'message': 'Game not found'}), 404

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

        print("Board after human move:")
        print_board(board)

        # Computer's turn
        computer_moves = []
        computer_move, checkers_notation = get_computer_move(board)
        if computer_move:
            print(f"Computer move: {checkers_notation}")
            board = make_move(board, computer_move)
            print("Board after computer move:")
            print_board(board)
            computer_moves.append(checkers_notation)
        else:
            print("No valid computer move found")

        # Save the updated board state
        game.board_state = json.dumps(board)
        db.session.commit()

        # Check for game over
        h_count = sum(row.count('h') + row.count('H') for row in board)
        c_count = sum(row.count('c') + row.count('C') for row in board)
        if h_count == 0 or c_count == 0:
            game.human_won = (h_count > 0)
            db.session.commit()

        return jsonify({
            'message': 'Moves made successfully', 
            'board': board,
            'game_over': game.human_won is not None,
            'computer_moves': computer_moves
        })

    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        print(f"Error in make_move: {str(e)}")
        print(f"Traceback:\n{error_traceback}")
        return jsonify({
            'message': 'An error occurred while making the move',
            'error': str(e),
            'traceback': error_traceback
        }), 500

   
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

    # If it's a capture move, check if there's an opponent's piece to capture
    if abs(src_row - dest_row) == 2:
        captured_row = (src_row + dest_row) // 2
        captured_col = (src_col + dest_col) // 2
        if board[captured_row][captured_col].lower() != 'c':
            return {'success': False, 'message': 'Invalid capture move'}

    # Move is valid, update the board
    piece = board[src_row][src_col]
    board[dest_row][dest_col] = piece
    board[src_row][src_col] = ' '

    # Handle captures
    if abs(src_row - dest_row) == 2:
        captured_row = (src_row + dest_row) // 2
        captured_col = (src_col + dest_col) // 2
        board[captured_row][captured_col] = ' '

    # Promote to king if reached the opposite end
    if piece.lower() == 'h' and dest_row == 0:
        board[dest_row][dest_col] = piece.upper()

    return {'success': True}



def print_board(board):
    print("   A   B   C   D   E   F   G   H")
    print(" +---+---+---+---+---+---+---+---+")
    for row_index, row in enumerate(board):
        row_str = f"{row_index + 1}|"
        for cell in row:
            row_str += f" {cell} |"
        print(row_str)
        print(" +---+---+---+---+---+---+---+---+")
