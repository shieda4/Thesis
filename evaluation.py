from game import Game
from node import Node
from neural_network import Residual
from tree_search import MCTS
from data_store import Store


# Starting 1 Self-play -> Training Iteration
net1 = Residual()
net1.load_model('models/model2')
net2 = Residual()
net2.load_model('models/model1')
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
        print('P1 Non Chain -> ', end='\t')
        print(predicted_action)
        if clone.if_attack_move(predicted_action):
            while game.attack_move_available(game.remove_except_current(predicted_action)):
                predicted_action, temp_children, temp_moves = tree_search_1.search(game.clone(), chain_move=True, action=predicted_action)
                game.play_action(predicted_action)
                print('P1 Chain -> ', end='\t')
                print(predicted_action)

    # Player 2
    else:
        predicted_action, temp_children, temp_moves = tree_search_2.search(game.clone())
        game.play_action(predicted_action)
        print('P2 Non Chain -> ', end='\t')
        print(predicted_action)
        if clone.if_attack_move(predicted_action):
            while game.attack_move_available(game.remove_except_current(predicted_action)):
                predicted_action, temp_children, temp_moves = tree_search_2.search(game.clone(), chain_move=True, action=predicted_action)
                game.play_action(predicted_action)
                print('P2 Chain -> ', end='\t')
                print(predicted_action)
    game.flip_perspective()
    step += 1
    if step > 200:
        break
        draw = True
print(game.state)
if draw:
    print('Draw')
if step % 2 == 0:
    print('Player 1 won')
else:
    print('Player 2 won')
