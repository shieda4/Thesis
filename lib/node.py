import math
from copy import deepcopy


class Node(object):

    def __init__(self, parent=None, action=None, policy=0.0, child_policy=[]):
        # Node Visit Count
        self.W = 0.0  # Node Value
        self.Q = math.inf  # Mean Node Value (W / N)
        self.policy = policy  # Self Policy (Probability of reaching current node)
        self.action = action  # Action from parent node leading to current state
        self.N = 0
        self.children = []  # A list of child Nodes
        self.child_policy = child_policy  # A policy distribution over the children nodes
        self.parent = parent  # Parent node of the current node

    # Identifies if a node is a leaf or not
    def is_not_leaf(self):
        if len(self.children) > 0:
            return True
        return False

    # Selects a child for expansion based on the PUCT value
    def select_child(self):
        exploration_constant = 1
        best_uct = 0
        best_uct_idx = 0

        for idx, child in enumerate(self.children):
            uct = child.Q + child.policy * exploration_constant * (math.sqrt(self.N) / (1 + child.N))
            if uct > best_uct:
                best_uct = uct
                best_uct_idx = idx

        return self.children[best_uct_idx]

    # Expands a node based on the policy and value returned by the Neural Network
    def expand_node(self, valid_moves, policy_vector):
        self.child_policy = deepcopy(policy_vector)

        for idx, move in enumerate(valid_moves):
            if move[4] != 0:
                action = deepcopy(move)
                self.add_child_node(parent=self, action=action, policy=policy_vector[idx])

    # Adds a child node to the parent node
    def add_child_node(self, parent, action, policy=0.0):

        child_node = Node(parent=parent, action=action, policy=policy)
        self.children.append(child_node)
        return child_node

    # Update values based on the Neural Network results values up the tree
    def back_prop(self, w, v):
        self.N += 1
        self.W += w + v
        self.Q = self.W / self.N
