/**
 * AI Tic-Tac-Toe Game in C
 * ---------------------------------------------------------
 * Structured, improved, and enhanced using Gemini 2.5 Pro
 *
 * Description:
 * This program implements a Tic-Tac-Toe game where the human
 * player ('X') plays against an unbeatable AI ('O').
 *
 * The AI uses the Minimax algorithm — a classic AI decision-making
 * method — to determine the optimal move by simulating all possible
 * game outcomes.
 *
 * Features:
 * - Structured modular design
 * - Recursive minimax decision logic
 * - Clean board visualization
 * - Input validation for human moves
 *
 * ---------------------------------------------------------
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
 * @brief Checks if the board is completely filled.
 * @return true if no empty cells remain, false otherwise.
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
 * @brief Checks whether a given player ('X' or 'O') has won.
 * @param player - The symbol of the player to check.
 * @return true if the player has a winning line, false otherwise.
 */
bool checkWinner(char player) {
    // Rows
    for (int i = 0; i < 3; i++) {
        if (board[i][0] == player && board[i][1] == player && board[i][2] == player)
            return true;
    }
    // Columns
    for (int i = 0; i < 3; i++) {
        if (board[0][i] == player && board[1][i] == player && board[2][i] == player)
            return true;
    }
    // Diagonals
    if (board[0][0] == player && board[1][1] == player && board[2][2] == player)
        return true;
    if (board[0][2] == player && board[1][1] == player && board[2][0] == player)
        return true;

    return false;
}

/**
 * @brief Minimax algorithm implementation.
 * Evaluates all possible game states recursively to determine
 * the optimal score for AI ('O') or Player ('X').
 *
 * @param isMaximizingPlayer - true if AI's turn, false if Player's turn.
 * @return +10 for AI win, -10 for Player win, 0 for draw.
 */
int minimax(bool isMaximizingPlayer) {
    // Terminal conditions
    if (checkWinner(PLAYER_O)) return 10;
    if (checkWinner(PLAYER_X)) return -10;
    if (isBoardFull()) return 0;

    // Maximizer (AI's move)
    if (isMaximizingPlayer) {
        int bestScore = INT_MIN;
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if (board[i][j] == EMPTY_SPACE) {
                    board[i][j] = PLAYER_O;
                    int score = minimax(false);
                    board[i][j] = EMPTY_SPACE;
                    if (score > bestScore) bestScore = score;
                }
            }
        }
        return bestScore;
    }
    // Minimizer (Player's move)
    else {
        int bestScore = INT_MAX;
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if (board[i][j] == EMPTY_SPACE) {
                    board[i][j] = PLAYER_X;
                    int score = minimax(true);
                    board[i][j] = EMPTY_SPACE;
                    if (score < bestScore) bestScore = score;
                }
            }
        }
        return bestScore;
    }
}

/**
 * @brief Determines the best possible move for the AI using minimax.
 * @return A struct Move containing the best (row, col).
 */
struct Move findBestMove() {
    int bestScore = INT_MIN;
    struct Move bestMove = {-1, -1};

    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            if (board[i][j] == EMPTY_SPACE) {
                board[i][j] = PLAYER_O;
                int moveScore = minimax(false);
                board[i][j] = EMPTY_SPACE;

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
 * @brief Gets the human player's move and validates it.
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
            printf("Invalid move. Please try again.\n");
        }
    }
}

/**
 * @brief The main game loop controlling the turns and outcomes.
 */
int main() {
    printf("=====================================\n");
    printf("      AI Tic-Tac-Toe in C (Minimax)\n");
    printf("=====================================\n");
    printf("You are 'X' | AI is 'O'\n\n");

    initializeBoard();
    printBoard();

    while (true) {
        // Player's turn
        getPlayerMove();
        printBoard();
        if (checkWinner(PLAYER_X)) {
            printf("🎉 Congratulations! You win!\n");
            break;
        }
        if (isBoardFull()) {
            printf("🤝 It's a draw!\n");
            break;
        }

        // AI's turn
        printf("AI is thinking...\n");
        struct Move aiMove = findBestMove();
        board[aiMove.row][aiMove.col] = PLAYER_O;

        printf("AI played at (%d, %d):\n", aiMove.row, aiMove.col);
        printBoard();

        if (checkWinner(PLAYER_O)) {
            printf("💻 AI wins! Better luck next time.\n");
            break;
        }
        if (isBoardFull()) {
            printf("🤝 It's a draw!\n");
            break;
        }
    }

    return 0;
}

/* -------------------------------------------------------------------
   📚 References & Acknowledgements
   -------------------------------------------------------------------
   1. Donald E. Knuth, "The Art of Computer Programming, Vol. 1–4."
      (For recursive algorithmic structure principles)
   2. S. Russell, P. Norvig, "Artificial Intelligence: A Modern Approach"
      (3rd Edition, Pearson, 2016)
   3. Tic-Tac-Toe Minimax concept explained in:
      GeeksforGeeks: https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-1-introduction/
   4. Stack Overflow & Cprogramming.com community references for
      practical C code structuring and debugging approaches.
   5. Enhancements and structured documentation support by
      Gemini 2.5 Pro & ChatGPT (OpenAI GPT-5).
   ------------------------------------------------------------------- */
