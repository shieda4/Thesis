from game import Game
from node import Node
from neural_network import Residual
from tree_search import MCTS
from termcolor import colored
from human import Human


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
human = Human()
game = Game()
print('Game has started !')
print_board(game.state)
step = 1

while game.check_game_over() == 0:
    clone = game.clone()
    # Player 1
    if step % 2 != 0:
        predicted_action, temp_children, temp_moves = tree_search_1.search(game.clone())
        game.play_action(predicted_action)
        print('Computer moved:', end='\t')
        print('(' + predicted_action[0] + ',' + predicted_action[1] + ') -> (' + predicted_action[2] + ',' +
              predicted_action[3] + ')')
        if clone.if_attack_move(predicted_action):
            while game.attack_move_available(game.remove_except_current(predicted_action)):
                predicted_action, temp_children, temp_moves = tree_search_1.search(game.clone(), chain_move=True,
                                                                                   action=predicted_action)
                game.play_action(predicted_action)
                print('Computer moved:', end='\t')
                print('(' + predicted_action[0] + ',' + predicted_action[1] + ') -> (' + predicted_action[2] + ',' +
                      predicted_action[3] + ')')

    # Player 2
    else:
        print_board(game.state)
        selected_move = human.get_move(game, chain=False)
        game.play_action(selected_move)
        print('Human moved:', end="\t")
        print('(' + selected_move[0] + ',' + selected_move[1] + ') -> (' + selected_move[2] + ',' +
              selected_move[3] + ')')
        if clone.if_attack_move(selected_move):
            while game.attack_move_available(
                    game.remove_non_attacks(game.remove_except_current(selected_move))):
                selected_move = human.get_move(game, chain=True, prev_move=selected_move)
                game.play_action(selected_move)
                print('Human moved:', end="\t")
                print('(' + selected_move[0] + ',' + selected_move[1] + ') -> (' + selected_move[2] + ',' +
                      selected_move[3] + ')')
    game.flip_perspective()
    step += 1
    if step > 120:
        break
        draw = True
if draw:
    print('It is a Draw !')
elif step % 2 == 0:
    print('Computer Won')
else:
    print('Human Won')