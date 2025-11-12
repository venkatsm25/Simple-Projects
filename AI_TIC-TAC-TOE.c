/**
 * AI Tic-Tac-Toe Game in C
 *
 * This program implements a Tic-Tac-Toe game where the human player
 * plays against an unbeatable AI.
 *
 * The AI uses the minimax algorithm to determine the best possible move.
 *
 * Player = 'X'
 * AI = 'O'
 */

#include <stdio.h>
#include <stdbool.h> // For bool, true, false
#include <limits.h>  // For INT_MIN and INT_MAX

// Define player symbols
#define PLAYER_X 'X'
#define PLAYER_O 'O'
#define EMPTY_SPACE ' '

// The 3x3 game board
char board[3][3];

// Structure to hold a move (row and column)
struct Move {
    int row;
    int col;
};

/**
 * @brief Initializes the game board to be empty.
 */
void initializeBoard() {
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            board[i][j] = EMPTY_SPACE;
        }
    }
}

/**
 * @brief Prints the current state of the game board.
 */
void printBoard() {
    printf("\n");
    printf(" %c | %c | %c \n", board[0][0], board[0][1], board[0][2]);
    printf("---|---|---\n");
    printf(" %c | %c | %c \n", board[1][0], board[1][1], board[1][2]);
    printf("---|---|---\n");
    printf(" %c | %c | %c \n", board[2][0], board[2][1], board[2][2]);
    printf("\n");
}

/**
 * @brief Checks if there are any moves left on the board.
 * @return true if the board is full, false otherwise.
 */
bool isBoardFull() {
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            if (board[i][j] == EMPTY_SPACE) {
                return false;
            }
        }
    }
    return true;
}

/**
 * @brief Checks if a specific player has won the game.
 * @param player The player ('X' or 'O') to check for a win.
 * @return true if the player has won, false otherwise.
 */
bool checkWinner(char player) {
    // Check rows
    for (int i = 0; i < 3; i++) {
        if (board[i][0] == player && board[i][1] == player && board[i][2] == player) {
            return true;
        }
    }
    // Check columns
    for (int i = 0; i < 3; i++) {
        if (board[0][i] == player && board[1][i] == player && board[2][i] == player) {
            return true;
        }
    }
    // Check diagonals
    if (board[0][0] == player && board[1][1] == player && board[2][2] == player) {
        return true;
    }
    if (board[0][2] == player && board[1][1] == player && board[2][0] == player) {
        return true;
    }
    return false;
}

/**
 * @brief The core minimax algorithm.
 * It considers all possible ways the game can go and returns a "score"
 * for the current board state.
 *
 * @param isMaximizingPlayer true if it's the AI's turn (maximizing score),
 * false if it's the Player's turn (minimizing score).
 * @return A score: +10 for AI win, -10 for Player win, 0 for draw.
 */
int minimax(bool isMaximizingPlayer) {
    // Check for terminal states (win/lose/draw)
    if (checkWinner(PLAYER_O)) {
        return 10; // AI wins
    }
    if (checkWinner(PLAYER_X)) {
        return -10; // Player wins
    }
    if (isBoardFull()) {
        return 0; // Draw
    }

    // AI's turn (Maximizer)
    if (isMaximizingPlayer) {
        int bestScore = INT_MIN; // Initialize with a very low score

        // Iterate through all empty cells
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if (board[i][j] == EMPTY_SPACE) {
                    // Make the move
                    board[i][j] = PLAYER_O;
                    // Recursively call minimax for the opponent's turn
                    int score = minimax(false); // Now it's the minimizer's (Player's) turn
                    // Undo the move
                    board[i][j] = EMPTY_SPACE;
                    // Find the maximum score
                    if (score > bestScore) {
                        bestScore = score;
                    }
                }
            }
        }
        return bestScore;
    }
    // Player's turn (Minimizer)
    else {
        int bestScore = INT_MAX; // Initialize with a very high score

        // Iterate through all empty cells
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if (board[i][j] == EMPTY_SPACE) {
                    // Make the move
                    board[i][j] = PLAYER_X;
                    // Recursively call minimax for the opponent's turn
                    int score = minimax(true); // Now it's the maximizer's (AI's) turn
                    // Undo the move
                    board[i][j] = EMPTY_SPACE;
                    // Find the minimum score
                    if (score < bestScore) {
                        bestScore = score;
                    }
                }
            }
        }
        return bestScore;
    }
}

/**
 * @brief Finds the best possible move for the AI.
 * It iterates through all possible moves, calls minimax() for each,
 * and chooses the move that gives the highest (best) score.
 *
 * @return A Move struct with the optimal row and column.
 */
struct Move findBestMove() {
    int bestScore = INT_MIN;
    struct Move bestMove;
    bestMove.row = -1;
    bestMove.col = -1;

    // Iterate through all empty cells
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            if (board[i][j] == EMPTY_SPACE) {
                // Make the move
                board[i][j] = PLAYER_O;
                
                // Calculate the score for this move
                // We call minimax for the minimizing player (Human)
                int moveScore = minimax(false); 

                // Undo the move
                board[i][j] = EMPTY_SPACE;

                // If this move's score is better than the best score found so far
                if (moveScore > bestScore) {
                    bestScore = moveScore;
                    bestMove.row = i;
                    bestMove.col = j;
                }
            }
        }
    }
    return bestMove;
}

/**
 * @brief Gets and validates the human player's move.
 */
void getPlayerMove() {
    int row, col;
    while (true) {
        printf("Enter your move (row and column, 0-2): ");
        scanf("%d %d", &row, &col);

        if (row >= 0 && row < 3 && col >= 0 && col < 3 && board[row][col] == EMPTY_SPACE) {
            board[row][col] = PLAYER_X;
            break;
        } else {
            printf("Invalid move. The cell is already taken or out of bounds.\n");
        }
    }
}

/**
 * @brief The main game loop.
 */
int main() {
    printf("Welcome to AI Tic-Tac-Toe!\n");
    printf("You are 'X' and the AI is 'O'.\n");
    
    initializeBoard();
    printBoard();

    while (true) {
        // --- Player's Turn ---
        getPlayerMove();
        printBoard();

        if (checkWinner(PLAYER_X)) {
            printf("Congratulations! You win!\n");
            break;
        }
        if (isBoardFull()) {
            printf("It's a draw!\n");
            break;
        }

        // --- AI's Turn ---
        printf("AI is thinking...\n");
        struct Move aiMove = findBestMove();
        board[aiMove.row][aiMove.col] = PLAYER_O;
        
        printf("AI played at (%d, %d):\n", aiMove.row, aiMove.col);
        printBoard();

        if (checkWinner(PLAYER_O)) {
            printf("AI wins! Better luck next time.\n");
            break;
        }
        if (isBoardFull()) {
            printf("It's a draw!\n");
            break;
        }
    }

    return 0;
}