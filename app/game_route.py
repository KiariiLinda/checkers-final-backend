from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from.models import Games
import json
from. import db
from .game_engine import create_board

game_blueprint = Blueprint('game',  __name__)

@game_blueprint.route("/game/board", methods=["GET"])
@jwt_required()
def get_board():
    current_user = get_jwt_identity()
    print(f"Current user: {current_user}")
    print(f"Current user ID: {current_user['id']}")
    game = Games.query.filter_by(player_id=current_user['id']).first()
    print(f"Game query result: {game}")
    if not game:
        print('No game found. Creating a new game.')
        initial_board_state = create_board()  # Call the imported function
        new_game = Games(player_id=current_user['id'], board_state=json.dumps(initial_board_state))
        db.session.add(new_game)
        db.session.commit()
        game = new_game  # Now game will reference the newly created game
    print(f"Game found for user {current_user['id']}")
    board = json.loads(game.board_state)
    print_board(board)
    return jsonify({'message': f"Hi {current_user['username']}, this is your board", 'board': board})
    
@game_blueprint.route("/game/make_move", methods=["PUT"])
@jwt_required()
def make_move():
    try:
        data = request.get_json()
        current_user = get_jwt_identity()
        game = Games.query.filter_by(player_id=current_user['id']).first()

        if not game:
            return jsonify({'message': 'Game not found'}), 404

        board = json.loads(game.board_state)  # Use the correct attribute name

        # Extract move details from request data
        src = data['src'].upper()   # e.g., "C3"
        dest = data['dest'].upper()   # e.g., "B4"

        # Convert board coordinates from "C3" to row/col
        src_row = int(src[1]) - 1  # Assuming 1-indexed input (C3 -> 2)
        src_col = ord(src[0].upper()) - ord('A')  # Convert column letter to index (C=2)
        dest_row = int(dest[1]) - 1  # Assuming 1-indexed input (B4 -> 3)
        dest_col = ord(dest[0].upper()) - ord('A')  # Convert column letter to index (B=1)

        # Validate the piece type
        piece_type = board[src_row][src_col]
        if piece_type not in ['●', '○']:  # Adjust based on your piece representation
            return jsonify({'message': 'Invalid piece selected'}), 400

        # Check if it's the current player's turn
        if (game.current_user == 'Human' and piece_type != '○') or (game.current_user == 'Computer' and piece_type != '●'):
            return jsonify({'message': 'Not your piece.'}), 400

        # Check if the move is valid for the piece
        if(piece_type == '○' and dest_row >= src_row) or (piece_type == '●' and dest_row <= src_row):
            return jsonify({'message': 'Invalid move. Piece can only move forward.'}), 400
          # Check if the move is diagonal
        if abs(dest_row - src_row) != abs(dest_col - src_col):
            return jsonify({'message': 'Invalid move. Piece can only move diagonally.'}), 400

        # Check if the destination is occupied by an opponent's piece
        dest_piece_type = board[dest_row][dest_col]
        if dest_piece_type and ((game.current_user == 'Human' and dest_piece_type == '●') or (game.current_user == 'Computer' and dest_piece_type == '○')):
            return jsonify({'message': 'Invalid move. Destination is occupied by an opponent\'s piece.'}), 400
        
        captured_piece = None
        capturing_player = None

        # Check if the move is a capture move
        if abs(dest_row - src_row) == 2 and abs(dest_col - src_col) == 2:
            mid_row = (src_row + dest_row) // 2
            mid_col = (src_col + dest_col) // 2
            mid_piece_type = board[mid_row][mid_col]
            if not mid_piece_type or ((game.current_user == 'Human' and mid_piece_type != '●') or (game.current_user == 'Computer' and mid_piece_type != '○')):
                return jsonify({'message': 'Invalid move. Capture move is not valid.'}), 400

            # Perform the capture move
            captured_piece = mid_piece_type
            capturing_player = game.current_user
            board[mid_row][mid_col] = ' '  # Clear the captured piece
            board[dest_row][dest_col] = piece_type
            board[src_row][src_col] = ' '  # Clear the source position
        else:
             # Check if the destination is empty
            if board[dest_row][dest_col] != ' ':
                return jsonify({'message': 'Invalid move. Destination is not empty.'}), 400

            # Perform the regular move on the board
            board[dest_row][dest_col] = piece_type
            board[src_row][src_col] = ' '  # Clear the source position

        # Update game state
        game.board_state = json.dumps(board)

        # Alternate turns
        game.current_user = 'Computer' if game.current_user == 'Human' else 'Human'

        db.session.add(game)
        db.session.commit()

        print_board(board)

        response_message = 'Move made successfully'
        if captured_piece:
            response_message += f'. {capturing_player} captured piece: {captured_piece}'

        return jsonify({'message': response_message, 'board': board})
    except Exception as e:
        return jsonify({'message': str(e)}), 500
        
    
    
def print_board(board):
    print("    A   B   C   D   E   F   G   H")
    print("  +---+---+---+---+---+---+---+---+")
    for idx, row in enumerate(board):
        print(f"{idx+1} | {' | '.join(row)} | {idx+1}")
        print("  +---+---+---+---+---+---+---+---+")
    print("    A   B   C   D   E   F   G   H")   
    


         









    
    
   
    

       



