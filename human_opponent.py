from game import Game
from node import Node
from neural_network import Residual
from tree_search import MCTS
from termcolor import colored
import pdb


def list_moves(all_moves):
    idx = []
    for i, move in enumerate(all_moves):
        if move[4] == 1:
            print(i, end=' -> ')
            print(move)
            idx.append(i)
    return idx


def print_board(board):
    for i in range(8):
        for j in range(8):
            if board[i][j] in set([-1, -2]):
                print(colored('(' + str(i) + ',' + str(j) + ')' + str(board[i][j]), 'red'), end='\t')
            elif board[i][j] in set([1, 2]):
                print(colored('(' + str(i) + ',' + str(j) + ')' + str(board[i][j]), 'green'), end='\t')
            else:
                print(colored('(' + str(i) + ',' + str(j) + ')' + str(board[i][j]), 'white'), end='\t')
        print('')
    pass


net = Residual()
net.load_model('models/model11')
tree_search_1 = MCTS(net, Node())

game = Game()

step = 1

while game.check_game_over() == 0:
    clone = game.clone()
    # Player 1
    if step % 2 != 0:
        predicted_action, temp_children, temp_moves = tree_search_1.search(game.clone())
        game.play_action(predicted_action)
        print('Computer moved ', end='\t')
        print(predicted_action)
        if clone.if_attack_move(predicted_action):
            while game.attack_move_available(game.remove_except_current(predicted_action)):
                predicted_action, temp_children, temp_moves = tree_search_1.search(game.clone(), chain_move=True,
                                                                                   action=predicted_action)
                game.play_action(predicted_action)
                print('Computer moved ', end='\t')
                print(predicted_action)

    # Player 2
    else:
        valid_moves = game.remove_reverse_moves()
        if game.attack_move_available(valid_moves):
            valid_moves = game.remove_non_attacks(valid_moves)
        print_board(game.state)
        idxs = list_moves(valid_moves)
        selected_move = None
        while not selected_move in set(idxs):
            selected_move = int(input())
            if selected_move in set(idxs):
                game.play_action(valid_moves[selected_move])
                break
            else:
                print('Invalid selection')
        if clone.if_attack_move(valid_moves[selected_move]):
            while game.attack_move_available(game.remove_non_attacks(game.remove_except_current(valid_moves[selected_move]))):
                valid_moves = game.remove_non_attacks(game.remove_except_current(valid_moves[selected_move]))
                print_board(game.state)
                idxs = list_moves(valid_moves)
                selected_move = None
                while not selected_move in set(idxs):
                    selected_move = input(int())
                    if selected_move in set(idxs):
                        game.play_action(valid_moves[selected_move])
                        break
                    else:
                        print('Invalid selection')
    game.flip_perspective()
    step += 1
    if step > 120:
        break
        draw = True
