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
from data_store import Store

# Creating Initial Network Model
net = Residual()
net.save_model('models/model0')
del net

# Starting 1 Self-play -> Training Iteration
iteration = 0
while iteration < 10:
    net = Residual()
    net.load_model('models/model' + iteration)
    tree_search_1 = MCTS(net, Node())
    tree_search_2 = MCTS(net, Node())
    store = Store()
    game = Game()

    # Starting 1 Self-play Game
    step = 1
    draw = False
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
        if step > 200:
            break
            draw = True
    print(game.state, end="\n")

    # Saving training data
    if not draw:
        if step % 2 == 0:
            store.update_values(player1=1, player2=0)
        else:
            store.update_values(player1=0, player2=1)
    else:
        store.update_values(player1=0, player2=0)
    store.save_store('store' + iteration)

    # Network Training
    net.fit_model(store.merged)
    net.save_model('models/model' + (iteration + 1))

# Final
