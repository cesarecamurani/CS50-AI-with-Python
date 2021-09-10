import tictactoe as ttt
import pdb

X = "X"
O = "O"
N = 'N'
EMPTY = None

# board = ttt.initial_state()
board = [[EMPTY, X, O], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]

player = ttt.player(board)
pdb.set_trace()

ttt_board = [[O, X, N],
             [O, N, X],
             [X, O, N]]

winner = ttt.winner(board)

terminal = ttt.terminal(board)

actions = ttt.actions(board)

result = ttt.result(board, (0, 2))

# max_value = ttt.max_value(board)
#
# min_value = ttt.min_value(board)

# minimax = ttt.minimax(board)
