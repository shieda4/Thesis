from game import Game
from node import Node
from neural_network import Residual
from tree_search import MCTS


game = Game()
net = Residual()
tree_search_1 = MCTS(net, Node())
tree_search_2 = MCTS(net, Node())

predicted_action = tree_search_1.search(game.clone())
game.play_action(predicted_action)
game.flip_perspective()
predicted_action = tree_search_2.search(game.clone())
game.play_action(predicted_action)
game.flip_perspective()

step = 1
while game.check_game_over() == 0:
    # Player 1
    if step % 2 != 0:
        tree_search_1.update_root(predicted_action)
        predicted_action = tree_search_1.search(game.clone())
    # Player 2
    else:
        tree_search_2.update_root(predicted_action)
        predicted_action = tree_search_2.search(game.clone())
    game.play_action(predicted_action)
    game.flip_perspective()
    print(game.state, end="\n")
    step += 1
