def get_tree_policy(children, all_moves):
    policy = [0] * 280
    actions = []
    visit_count = []
    for child in children:
        actions.append(child.action)
        visit_count.append(child.N)

    for i, action in enumerate(actions):
        idx = all_moves.index(action)
        policy[idx] = visit_count[i] / sum(visit_count)
    return policy


from game import Game
from node import Node
from neural_network import Residual
from tree_search import MCTS
import time
from data_store import Store

net = Residual()
net2 = Residual()
tree_search_1 = MCTS(net, Node())
tree_search_2 = MCTS(net2, Node())
store = Store()
game = Game()
t = time.time()
step = 1
while game.check_game_over() == 0:
    clone = game.clone()
    # Player 1
    if step % 2 != 0:
        predicted_action, temp_children, temp_moves = tree_search_1.search(game.clone())
        temp_policy = get_tree_policy(temp_children, temp_moves)
        store.update_store([game.clone().state, temp_policy, 0], player1=True)
        game.play_action(predicted_action)
        print('P1 Non Chain -> ', end='\t')
        print(predicted_action)
        if clone.if_attack_move(predicted_action):
            while game.attack_move_available(game.remove_except_current(predicted_action)):
                predicted_action, temp_children, temp_moves = tree_search_1.search(game.clone(), chain_move=True,
                                                                                   action=predicted_action)
                temp_policy = get_tree_policy(temp_children, temp_moves)
                store.update_store([game.clone().state, temp_policy, 0], player1=True)
                game.play_action(predicted_action)
                print('P1 Chain -> ', end='\t')
                print(predicted_action)

    # Player 2
    else:
        predicted_action, temp_children, temp_moves = tree_search_2.search(game.clone())
        temp_policy = get_tree_policy(temp_children, temp_moves)
        store.update_store([game.clone().state, temp_policy, 0], player2=True)
        game.play_action(predicted_action)
        print('P2 Non Chain -> ', end='\t')
        print(predicted_action)
        if clone.if_attack_move(predicted_action):
            while game.attack_move_available(game.remove_except_current(predicted_action)):
                predicted_action, temp_children, temp_moves = tree_search_2.search(game.clone(), chain_move=True,
                                                                                   action=predicted_action)
                temp_policy = get_tree_policy(temp_children, temp_moves)
                store.update_store([game.clone().state, temp_policy, 0], player2=True)
                game.play_action(predicted_action)
                print('P2 Chain -> ', end='\t')
                print(predicted_action)
    print(game.state, end="\n")
    game.flip_perspective()
    step += 1
t = time.time() - t
print(game.state, end="\n")
if step % 2 == 0:
    store.update_values(player1=1, player2=0)
else:
    store.update_values(player1=0, player2=1)
store.save_store('store')
