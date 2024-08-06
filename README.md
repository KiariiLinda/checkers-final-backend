# Checkers Game Back End

This is a Flask-based project for a Checkers game. It provides endpoints to manage a game of Checkers, including getting the board state, making moves, and resetting the game. The game features an AI opponent using the minimax algorithm.

## Features

- Get current board state
- Make moves (human player)
- Automatic computer moves using AI
- Game state management (win/lose/draw conditions)
- Game reset functionality

## Endpoints

### 1. Get Board State

- **URL:** `/game/board`
- **Method:** GET
- **Authentication:** JWT required
- **Description:** Retrieves the current board state for the authenticated user.

### 2. Make Move

- **URL:** `/game/make_move`
- **Method:** PUT
- **Authentication:** JWT required
- **Description:** Allows the human player to make a move and triggers the computer's move.

### 3. Reset Game

- **URL:** `/game/reset`
- **Method:** POST
- **Authentication:** JWT required
- **Description:** Resets the game to its initial state.

## Game Logic

- The game uses a standard 8x8 Checkers board.
- Human pieces are represented by 'h' (regular) and 'H' (king).
- Computer pieces are represented by 'c' (regular) and 'C' (king).
- The game handles regular moves, captures, and kinging.
- The game ends when one player has no pieces left or after 80 moves without a capture (draw).

## Computer Player (AI)

The computer player uses the minimax algorithm to determine the best move. Key components include:

- `minimax`: Implements the minimax algorithm with a specified depth.
- `get_computer_move`: Selects the best move for the computer using minimax.
- `evaluate_board`: Evaluates the current board state.
- `get_all_possible_moves`: Generates all possible moves for a given player.
- `make_move`: Applies a move to the board, handling captures and kinging.

The AI considers both regular moves and jumps, and can look several moves ahead to make strategic decisions.

## Setup and Running

Install dependencies:

    npm install

    pipenv install

Set up the backend:

    pipenv shell

    python app.py

## Acknowledgments

> [Marc Ndegwa](https://github.com/teeno-vices) - Developer
>
> [Jalen Mnene](https://github.com/Jalenzzz) - Developer
>
> [Linda Kiarii](https://github.com/KiariiLinda) - Developer
>
> [Immanuel Anyangu](https://github.com/Meshmanuu) - Developer
>
> [Luther Isaboke](https://github.com/kib4n4) - Developer
