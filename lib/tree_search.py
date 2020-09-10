from lib.node import Node
import numpy as np


def _add_dirichlet_noise(policy):
    dirichlet_input = [0.5 for x in range(280)]
    dirichlet_list = np.random.dirichlet(dirichlet_input)
    noisy_policy = []
    for i, pol in enumerate(policy):
        noisy_policy.append((1 - 0.25) * pol + 0.25 * dirichlet_list[i])

    return noisy_policy


class MCTS(object):
    def __init__(self, net, node):
        self.root = node
        self.game = None
        self.net = net
        pass

    def search(self, game, chain_move=False, action=None):
        self.game = game
        self.root = Node()
        root_expansion = True

        # 128 MCTS Iterations
        for i in range(128):
            node = self.root
            clone = game.clone()
            # Search for a Leaf node
            while node.is_not_leaf():
                node = node.select_child()
                clone.play_action(node.action)
                clone.flip_perspective()

            # Get the policy and Value from the Neural Network
            policy, value = self.net.predict(clone.state)
            policy = _add_dirichlet_noise(policy)
            value = value.flatten()[0]

            # Finalize the list of valid moves based on the current position
            if not chain_move or not root_expansion:
                valid_moves = clone.remove_reverse_moves()
                if clone.attack_move_available(valid_moves):
                    valid_moves = clone.remove_non_attacks(valid_moves)
            else:
                valid_moves = clone.remove_except_current(action)
                valid_moves = clone.remove_non_attacks(valid_moves)
            root_expansion = False

            # Normalize the Policy
            # Zero out invalid moves
            # Make all probabilities sum up to 1
            for idx, move in enumerate(valid_moves):
                if move[4] == 0:
                    policy[0][idx] = 0
            policy_sum = sum(policy[0])
            if policy_sum > 0:
                policy[0] /= policy_sum

            # Expand Node Based on the policy
            node.expand_node(valid_moves, policy_vector=policy[0])

            # Checks if game is over
            w = clone.check_game_over()

            # Back Propagate values up the tree
            while node is not None:
                w = -w
                value = -value
                node.back_prop(w, value)
                node = node.parent

        best_n = 0
        best_n_idx = 0

        for idx, child in enumerate(self.root.children):
            if child.N > best_n:
                best_n = child.N
                best_n_idx = idx

        # Return the estimated best action
        return self.root.children[best_n_idx].action, self.root.children, game.get_valid_moves()
