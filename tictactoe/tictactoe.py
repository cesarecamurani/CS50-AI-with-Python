"""
Tic Tac Toe Player
"""

import math
import copy

from setuptools.namespaces import flatten

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count, o_count = 0, 0

    # Flattens the list for easier handling.
    board = list(flatten(board))
    # Counts all the Xs on the board.
    if any(elem == X for elem in board):
        x_count = board.count(X)
    # Counts all the Os on the board.
    if any(elem == O for elem in board):
        o_count = board.count(O)
    # If there are more Xs than Os returns O, otherwise returns X.
    return O if x_count > o_count else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Returns None if the board is in a terminal state.
    if terminal(board):
        return None
    # Initializes the possible actions to an empty set.
    possible_actions = set()

    length = len(board)
    # Checks every cell and adds it to the list of possible actions if empty.
    for i in range(length):
        for j in range(length):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Deep-copies the original board.
    latest_board = copy.deepcopy(board)
    # Raises an Exception if the action is not allowed.
    if action not in actions(latest_board):
        raise Exception('This action is not valid')
    # Assigns the cell to the right player.
    latest_board[action[0]][action[1]] = player(board)

    return latest_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    players = [X, O]
    """
    Checks the winning conditions list for each player and 
    if a player meets one of them it returns the player, otherwise returns None.
    """
    for plr in players:
        winning_conditions = [
            all(elem == plr for elem in board[0]),
            all(elem == plr for elem in board[1]),
            all(elem == plr for elem in board[2]),
            all(elem == plr for elem in [board[0][0], board[1][0], board[2][0]]),
            all(elem == plr for elem in [board[0][1], board[1][1], board[2][1]]),
            all(elem == plr for elem in [board[0][2], board[1][2], board[2][2]]),
            all(elem == plr for elem in [board[0][0], board[1][1], board[2][2]]),
            all(elem == plr for elem in [board[0][2], board[1][1], board[2][0]])
        ]

        if any(condition for condition in winning_conditions):
            return plr

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Returns True if there's a winner.
    if winner(board) is not None:
        return True
    # Flattens the list for easier checking.
    board = list(flatten(board))
    # Returns True if there are no more EMPTY cells on the board.
    if all(elem != EMPTY for elem in board):
        return True
    # Returns False as default.
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1

    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    # Initiates the best_move variable as an empty tuple.
    best_move = ()
    possible_actions = actions(board)

    if x_player(board):
        # Sets the initial value to minus infinity (worst possible value for max player).
        best_value = -math.inf
        """
        For every possible action it founds the opponent minimum value and if it's higher than
        the initial (best) value it sets to it, setting the best move to the corresponding action.
        """
        for action in possible_actions:
            opponent_min_value = min_value(result(board, action))

            if opponent_min_value > best_value:
                best_value = opponent_min_value
                best_move = action

    elif o_player(board):
        # Sets the initial value to infinity (worst possible value for min player).
        best_value = math.inf
        """
        For every possible action it founds the opponent maximum value and if it's lower than
        the initial (best) value it sets to it, setting the best move to the corresponding action.
        """
        for action in possible_actions:
            opponent_max_value = max_value(result(board, action))

            if opponent_max_value < best_value:
                best_value = opponent_max_value
                best_move = action

    return best_move


def max_value(board):
    # Returns the result of the utility function if the game is over.
    if terminal(board):
        return utility(board)
    # Sets the initial value to minus infinity (worst possible value for max player).
    value = -math.inf
    """
    For every possible action on the board it finds the maximum value between 
    the initial value (in the first interaction) and the result of calling the min_value function on the 
    outcome of result(board, action), re-assigning the initial value to the highest value between the 2.
    """
    for action in actions(board):
        value = max(value, min_value(result(board, action)))
    # Returns the value
    return value


def min_value(board):
    # Returns the result of the utility function if the game is over.
    if terminal(board):
        return utility(board)
    # Sets the initial value to infinity (worst possible value for min player).
    value = math.inf
    """
    For every possible action on the board it finds the minimum value between 
    the initial value (in the first interaction) and the result of calling the max_value function on the 
    outcome of result(board, action), re-assigning the initial value to the lowest value between the 2.
    """
    for action in actions(board):
        value = min(value, max_value(result(board, action)))
    # Returns the value.
    return value


# Returns player X turn.
def x_player(board):
    return player(board) == X


# Returns player O turn.
def o_player(board):
    return player(board) == O
