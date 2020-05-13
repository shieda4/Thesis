from game import Game
from node import Node
from neural_network import Residual
from tree_search import MCTS
import time

net = Residual()
net2 = Residual()
tree_search_1 = MCTS(net, Node())
tree_search_2 = MCTS(net2, Node())

game = Game()
t = time.time()
step = 1
while game.check_game_over() == 0:
    clone = game.clone()
    # Player 1
    if step % 2 != 0:
        predicted_action = tree_search_1.search(game.clone())
        game.play_action(predicted_action)
        print('P1 Non Chain -> ', end='\t')
        print(predicted_action)
        if clone.if_attack_move(predicted_action):
            while game.attack_move_available(game.remove_except_current(predicted_action)):
                predicted_action = tree_search_1.search(game.clone(), chain_move=True, action=predicted_action)
                game.play_action(predicted_action)
                print('P1 Chain -> ', end='\t')
                print(predicted_action)

    # Player 2
    else:
        predicted_action = tree_search_2.search(game.clone())
        game.play_action(predicted_action)
        print('P2 Non Chain -> ', end='\t')
        print(predicted_action)
        if clone.if_attack_move(predicted_action):
            while game.attack_move_available(game.remove_except_current(predicted_action)):
                predicted_action = tree_search_2.search(game.clone(), chain_move=True, action=predicted_action)
                game.play_action(predicted_action)
                print('P2 Chain -> ', end='\t')
                print(predicted_action)
    print(game.state, end="\n")
    game.flip_perspective()
    step += 1
t = time.time() - t
print(game.state, end="\n")
