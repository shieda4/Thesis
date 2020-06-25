from game import Game
from node import Node
from neural_network import Residual
from tree_search import MCTS
import time


# Starting 1 Self-play -> Training Iteration
iteration = 6
while iteration in range(7):
    print('Game ' + str(iteration))
    net1 = Residual()
    net2 = Residual()
    net1.load_model('models/model' + str(iteration))
    net2.load_model('models/model' + str(iteration + 1))
    tree_search_1 = MCTS(net1, Node())
    tree_search_2 = MCTS(net2, Node())
    game = Game()

    # Starting 1 Self-play Game
    step = 1
    draw = False
    while game.check_game_over() == 0:
        clone = game.clone()
        # Player 1
        if step % 2 != 0:
            predicted_action, temp_children, temp_moves = tree_search_1.search(game.clone())
            game.play_action(predicted_action)
            # print('P1 Non Chain -> ', end='\t')
            # print(predicted_action)
            if clone.if_attack_move(predicted_action):
                while game.attack_move_available(game.remove_except_current(predicted_action)):
                    predicted_action, temp_children, temp_moves = tree_search_1.search(game.clone(), chain_move=True, action=predicted_action)
                    game.play_action(predicted_action)
                    # print('P1 Chain -> ', end='\t')
                    # print(predicted_action)

        # Player 2
        else:
            predicted_action, temp_children, temp_moves = tree_search_2.search(game.clone())
            game.play_action(predicted_action)
            # print('P2 Non Chain -> ', end='\t')
            # print(predicted_action)
            if clone.if_attack_move(predicted_action):
                while game.attack_move_available(game.remove_except_current(predicted_action)):
                    predicted_action, temp_children, temp_moves = tree_search_2.search(game.clone(), chain_move=True, action=predicted_action)
                    game.play_action(predicted_action)
                    # print('P2 Chain -> ', end='\t')
                    # print(predicted_action)
        game.flip_perspective()
        step += 1
        if step > 200:
            break
            draw = True
    # print(game.state)
    if draw:
        print('Player ' + str(iteration) + ' vs ' + 'Player ' + str(iteration + 1) + ': ', end='\t')
        print('Draw')
    if step % 2 == 0:
        print('Player ' + str(iteration) + ' vs ' + 'Player ' + str(iteration + 1) + ': ', end='\t')
        print('Player ' + str(iteration) + ' Won')
    else:
        print('Player ' + str(iteration) + ' vs ' + 'Player ' + str(iteration + 1) + ': ', end='\t')
        print('Player ', str(iteration + 1) + ' Won')
    iteration += 1
