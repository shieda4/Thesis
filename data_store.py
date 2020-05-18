import numpy as np


class Store(object):
    def __init__(self):
        self.player1 = []
        self.player2 = []
        self.merged = []
        pass

    def update_store(self, data, player1=False, player2=False):
        state, policy, value = data[0], data[1], data[2]
        if player1:
            self.player1.append([state, policy, value])
        if player2:
            self.player2.append([state, policy, value])

    def save_store(self, filename):
        self.merged.append(self.player1)
        self.merged.append(self.player2)
        np.save(filename + ".npy", self.merged)

    def load_store(self, filename):
        temp = np.load(filename + '.npy', allow_pickle=True)
        self.merged = temp.tolist()
        self.player1 = self.merged[0]
        self.player2 = self.merged[1]

    def get_store(self):
        self.merged.clear()
        self.merged.append(self.player1)
        self.merged.append(self.player2)
        return self.merged

    def update_values(self, player1=0, player2=0):
        for i in range(len(self.player1)):
            self.player1[i][2] = player1

        for i in range(len(self.player2)):
            self.player2[i][2] = player2

        self.merged.clear()
        self.merged.append(self.player1)
        self.merged.append(self.player2)
