from node import Node


class MCTS(object):
    def __init__(self, net, node):
        self.root = node
        self.game = None
        self.net = net
        pass

    def search(self, game):
        self.game = game
        self.root = Node()
        for i in range(64):
            print(i)
            node = self.root
            clone = game.clone()
            while node.is_not_leaf():
                node = node.select_child()
                # print(node.action)
                clone.play_action(node.action)
                clone.flip_perspective()

            policy, value = self.net.predict(clone.state)
            value = value.flatten()[0]

            valid_moves = game.get_valid_moves()

            for idx, move in enumerate(valid_moves):
                if move[4] == 0:
                    policy[0][idx] = 0

            policy_sum = sum(policy[0])

            if policy_sum > 0:
                policy[0] /= policy_sum

            node.expand_node(game=clone, policy_vector=policy[0])

            w = clone.check_game_over()

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
        self.root = self.root.children[best_n_idx]
        return self.root.action

    def update_root(self, action):
        for child in self.root.children:
            if child.action == action:
                self.root = child
                break
        pass
