"""

    ACIT 1515 - Lab 4

    For Lab 4 you will be implementing and debugging a command-line version of Connect 4, a game consisting of a
    vertically suspended board where players take turns dropping a colored token into columns with the aim of forming
    a vertical, horizontal, or diagonal line of four of their tokens.

    See https://en.wikipedia.org/wiki/Connect_Four for more info

    ---

    For this implementation, the board will be square (6 rows by 6 columns by default) and the colored tokens will be
    represented by the following strings: • for an empty space o for a user token x for the computer opponent token

    Below is an example empty board:

    •   •   •   •   •   •  

    •   •   •   •   •   •  

    •   •   •   •   •   •  

    •   •   •   •   •   •  

    •   •   •   •   •   •  

    •   •   •   •   •   •
        
    And an example of a board where the user has won by forming a diagonal line of four tokens:

    •   •   •   •   •   •

    •   •   •   •   •   •  

    •   •   •   o   •   •  

    •   •   o   x   •   •  

    •   o   o   x   •   •  

    o   x   x   x   o   •   


    PART 1
    ---------------------------------------------------------------------------
    
    The main function in this script will be responsible for repeatedly asking the player to choose a position (
    alternating as the 'user' then the 'computer'), validating the position, updating the board if the position is
    valid, and then printing the board to the command-line.
    
    IMPORTANT: just like the vertical, physical version of the game, the player should not be allowed to choose a
    position with an empty space below it, i.e. the following game board would be considered invalid:

        0   1   2   3   4   5

    0   •   •   •   •   •   •

    1   •   •   •   •   •   •  

    2   •   •   •   o   •   •      <-- this position (column 3, row 2) has an empty space below it

    3   •   •   o   •   •   •  

    4   •   o   o   x   x   •  

    5   o   x   x   x   o   • 

    Implementation details are provided below in the respective functions


    PART 2
    ---------------------------------------------------------------------------

    Once the program functions correctly, you must refactor the code as necessary to accept any size of board.

    The size (ROWS) value must be supplied as a command-line argument when the script is invoked, e.g.
        py lab4.py --rows 7

    ---
    
    RULES for this submission:

    You CAN:
        - add parameters to functions if necessary
        - move repetitive code into a new function
        - modify the code in the main() function as needed
        - import any necessary modules (from the standard library only!)

    You MUST: - only use the print_board function to output the board (i.e. print(board) is not allowed except for
    debugging purposes) - remove any hard-coded values (e.g. use the ROWS, EMPTY, USER, and COMPUTER variables) - use
    the prompt() function we previously defined to handle error checking and valid input

"""

import sys
from tools import prompt

# Rows can be made smaller or larger by passing a --rows argument to the script
ROWS = 6
EMPTY = "• "
USER = "o "
COMPUTER = "x "


# The board is a list of lists, where each inner list represents a row
def valid_move(board, position):
    col = position % ROWS
    row = position // ROWS
    if board[row][col] != EMPTY:
        return False, "Position already occupied!"
    elif row < ROWS - 1 and board[row + 1][col] == EMPTY:
        return False, "Position has an empty space below it!"
    else:
        return True, ""


def update_board(board, position, symbol):
    row = position // ROWS
    col = position % ROWS
    board[row][col] = symbol


def print_board(board):
    for row in board:
        print("  ".join(row))
        # Blank line
        print()


def check_win(board, symbol):
    # Check horizontal, vertical, and diagonals
    for i in range(ROWS):
        for j in range(ROWS - 3):
            if board[i][j] == board[i][j + 1] == board[i][j + 2] == board[i][j + 3] == symbol:  # Horizontal
                return True
    for i in range(ROWS - 3):
        for j in range(ROWS):
            if board[i][j] == board[i + 1][j] == board[i + 2][j] == board[i + 3][j] == symbol:  # Vertical
                return True
    for i in range(ROWS - 3):
        for j in range(ROWS - 3):
            if board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] == board[i + 3][
                j + 3] == symbol:  # Diagonal from top-left to bottom-right
                return True
            if board[i][j + 3] == board[i + 1][j + 2] == board[i + 2][j + 1] == board[i + 3][
                j] == symbol:  # Diagonal from bottom-left to top-right
                return True
    return False


def check_state(board, symbol):
    if check_win(board, symbol):
        if symbol == USER:
            print("Game Over! User wins.")
        else:
            print("Game Over! Computer wins.")
        return False

    # Check for full board
    for row in board:
        if EMPTY in row:
            return True
    print("Game Over! Board is full.")
    return False


def main():
    # Initialize the board to whatever size is specified by the ROWS variable, set every position to EMPTY
    board = [[EMPTY for _ in range(ROWS)] for _ in range(ROWS)]

    # Show the user the empty board
    print_board(board)

    game_over = False

    # The user will always go first
    current_player = USER

    # Continue the game until the board is full or someone wins
    while not game_over:
        if current_player == USER:
            move = prompt(f"User's turn (0-{ROWS * ROWS - 1}):", range(ROWS * ROWS), int)
        else:
            move = prompt(f"Computer's turn (0-{ROWS * ROWS - 1}):", range(ROWS * ROWS), int)

        valid, msg = valid_move(board, move)
        if not valid:
            print(msg)
            print_board(board)
        else:
            update_board(board, move, current_player)
            print_board(board)

            # Check game state here after the move
            game_over = not check_state(board, current_player)

            # Only switch players if the game is not over
            if not game_over:
                current_player = COMPUTER if current_player == USER else USER


if __name__ == "__main__":
    # Check for command-line arguments
    if "--rows" in sys.argv:
        # Get the index of the --rows argument
        index = sys.argv.index("--rows") + 1
        # Check if the index is within the bounds of the list
        if index < len(sys.argv):
            ROWS = int(sys.argv[index])
    main()
