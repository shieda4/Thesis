import numpy as np
from copy import deepcopy


def is_even(x):
    return x % 2 == 0
    pass


def is_piece(x, y):
    return (is_even(x) and (not is_even(y))) or ((not is_even(x)) and is_even(y))
    pass


def is_capture_move(move):
    if move[0] - move[2] == 1:
        return False
    return True
    pass


class Game(object):
    def __init__(self):
        self.row = self.column = 8
        self.action_size = 280
        self.state = np.array([[0, -1, 0, -1, 0, -1, 0, -1],
                               [-1, 0, -1, 0, -1, 0, -1, 0],
                               [0, -1, 0, -1, 0, -1, 0, -1],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [1, 0, 1, 0, 1, 0, 1, 0],
                               [0, 1, 0, 1, 0, 1, 0, 1],
                               [1, 0, 1, 0, 1, 0, 1, 0]])
        # self.state = np.array([[0, 0, 0, 0, 0, 0, 0, -1],
        #                        [0, 0, 0, 0, 0, 0, 0, 0],
        #                        [0, 2, 0, 0, 0, 0, 0, -1],
        #                        [0, 0, 0, 0, 0, 0, 0, 0],
        #                        [0, 0, 0, 0, 0, 0, 0, 0],
        #                        [-2, 0, 0, 0, 0, 0, 0, 0],
        #                        [0, 0, 0, 0, 0, 0, 0, 1],
        #                        [0, 0, 0, 0, 0, 0, 1, 0]])

        pass

    def clone(self):
        return deepcopy(self)

    def play_action(self, action):
        x, y, x1, y1 = action[0:4]

        # For Normal Piece
        if self.state[x][y] == 1:
            # Non Capture Moves
            if (x - x1) == 1:
                self.state[x][y] = 0
                if x1 == 0:
                    self.state[x1][y1] = 2
                else:
                    self.state[x1][y1] = 1
            # Capture Moves
            else:
                x_mid = int((x + x1) / 2)
                y_mid = int((y + y1) / 2)
                self.state[x][y] = 0
                self.state[x_mid][y_mid] = 0
                if x1 == 0:
                    self.state[x1][y1] = 2
                else:
                    self.state[x1][y1] = 1

        # For King Piece
        else:
            if abs(x - x1) == 1:
                self.state[x][y] = 0
                self.state[x1][y1] = 2
            else:
                # Up
                if (x - x1) > 0:
                    # Left
                    if y - y1 > 0:
                        self.state[x1 + 1][y1 + 1] = 0
                        self.state[x1][y1] = 2
                        self.state[x][y] = 0
                    # Right
                    else:
                        self.state[x1 + 1][y1 - 1] = 0
                        self.state[x1][y1] = 2
                        self.state[x][y] = 0
                # Down
                else:
                    # Left
                    if y - y1 > 0:
                        self.state[x1 - 1][y1 + 1] = 0
                        self.state[x1][y1] = 2
                        self.state[x][y] = 0
                    # Right
                    else:
                        self.state[x1 - 1][y1 - 1] = 0
                        self.state[x1][y1] = 2
                        self.state[x][y] = 0

    def get_all_moves(self):
        all_moves = []
        for i in range(self.row):
            for j in range(self.column):
                if is_piece(i, j):

                    x, y = i, j
                    while x > 0 and y > 0:
                        x = x - 1
                        y = y - 1
                        all_moves.append([i, j, x, y, 0])

                    x, y = i, j
                    while x > 0 and y < self.column - 1:
                        x = x - 1
                        y = y + 1
                        all_moves.append([i, j, x, y, 0])

                    x, y = i, j
                    while x < self.column - 1 and y > 0:
                        x = x + 1
                        y = y - 1
                        all_moves.append([i, j, x, y, 0])

                    x, y = i, j
                    while x < self.column - 1 and y < self.column - 1:
                        x = x + 1
                        y = y + 1
                        all_moves.append([i, j, x, y, 0])
        return all_moves

    def get_valid_moves(self):
        all_moves = self.get_all_moves()
        for move in all_moves:
            x, y, x1, y1, valid = deepcopy(move)

            # Normal Piece
            if self.state[x][y] == 1:
                # 1 Forward Diagonal
                if x - x1 == 1:
                    # If able to perform action
                    if self.state[x1][y1] == 0:
                        move[4] = 1

                # Diagonal Attack Move
                elif abs(x - x1) == 2:
                    x_mid = int((x + x1) / 2)
                    y_mid = int((y + y1) / 2)

                    # If able to perform action
                    if (self.state[x1][y1] == 0) and (
                            (self.state[x_mid][y_mid] == -1) or (self.state[x_mid][y_mid] == -2)):
                        move[4] = 1

                # Invalid Moves
                else:
                    pass

            # King Piece
            elif self.state[x][y] == 2:
                if self.state[x1][y1] == 0:
                    # Forward Movement
                    if x - x1 > 0:
                        # Left Movement
                        if y - y1 > 0:
                            # Direction: Upper Left
                            x_move, y_move = -1, -1
                            x_temp, y_temp = deepcopy(x) + x_move, deepcopy(y) + y_move
                            count = 0
                            while (x_temp != x1) and (y_temp != y1):
                                count += self.state[x_temp][y_temp]
                                x_temp += x_move
                                y_temp += y_move

                            # Non Capture Moves
                            if count == 0:
                                move[4] = 1
                            # Capture of a normal piece
                            elif count == -1:
                                if self.state[x1 + (-x_move)][y1 + (-y_move)] == -1:
                                    move[4] = 1
                            # Capture of a king piece
                            elif count == -2:
                                if self.state[x1 + (-x_move)][y1 + (-y_move)] == -2:
                                    move[4] = 1
                            pass
                        # Right Movement
                        elif y - y1 < 0:
                            # Direction: Upper Right
                            x_move, y_move = -1, +1
                            x_temp, y_temp = deepcopy(x) + x_move, deepcopy(y) + y_move
                            count = 0
                            while (x_temp != x1) and (y_temp != y1):
                                count += self.state[x_temp][y_temp]
                                x_temp += x_move
                                y_temp += y_move

                            # Non Capture Moves
                            if count == 0:
                                move[4] = 1
                            # Capture of a normal piece
                            elif count == -1:
                                if self.state[x1 + (-x_move)][y1 + (-y_move)] == -1:
                                    move[4] = 1
                            # Capture of a king piece
                            elif count == -2:
                                if self.state[x1 + (-x_move)][y1 + (-y_move)] == -2:
                                    move[4] = 1
                            pass

                    # Backward Movement
                    elif x - x1 < 0:
                        # Left Movement
                        if y - y1 > 0:
                            # Direction: lower Left
                            x_move, y_move = +1, -1
                            x_temp, y_temp = deepcopy(x) + x_move, deepcopy(y) + y_move
                            count = 0
                            while (x_temp != x1) and (y_temp != y1):
                                count += self.state[x_temp][y_temp]
                                x_temp += x_move
                                y_temp += y_move

                            # Non Capture Moves
                            if count == 0:
                                move[4] = 1
                            # Capture of a normal piece
                            elif count == -1:
                                if self.state[x1 + (-x_move)][y1 + (-y_move)] == -1:
                                    move[4] = 1
                            # Capture of a king piece
                            elif count == -2:
                                if self.state[x1 + (-x_move)][y1 + (-y_move)] == -2:
                                    move[4] = 1
                            pass
                        # Right Movement
                        elif y - y1 < 0:
                            # Direction: lower Right
                            x_move, y_move = +1, +1
                            x_temp, y_temp = deepcopy(x) + x_move, deepcopy(y) + y_move
                            count = 0
                            while (x_temp != x1) and (y_temp != y1):
                                count += self.state[x_temp][y_temp]
                                x_temp += x_move
                                y_temp += y_move

                            # Non Capture Moves
                            if count == 0:
                                move[4] = 1
                            # Capture of a normal piece
                            elif count == -1:
                                if self.state[x1 + (-x_move)][y1 + (-y_move)] == -1:
                                    move[4] = 1
                            # Capture of a king piece
                            elif count == -2:
                                if self.state[x1 + (-x_move)][y1 + (-y_move)] == -2:
                                    move[4] = 1
                            pass
                        pass
                    # Invalid Move
                    else:
                        pass

            # Empty Square
            else:
                pass

        return all_moves

    def check_game_over(self):
        all_moves = self.get_valid_moves()
        enemy_clone = self.clone()
        enemy_clone.flip_perspective()
        enemy_all_moves = enemy_clone.get_valid_moves()
        move_available = False
        enemy_move_available = False
        for move in all_moves:
            if move[4] == 1:
                move_available = True
                break
        for move in enemy_all_moves:
            if move[4] == 1:
                enemy_move_available = True
                break
        if move_available and enemy_move_available:
            return 0
        elif (not move_available) and (not enemy_move_available):
            return 0
        elif (not move_available) and enemy_move_available:
            return -1
        else:
            return 1

    def flip_perspective(self):
        black = deepcopy(self.state)
        for i in range(self.row):
            for j in range(int(self.column / 2)):
                temp = black[i][j]
                black[i][j] = black[i][self.column - 1 - j]
                black[i][self.column - 1 - j] = temp

        for i in range(int(self.row / 2)):
            for j in range(self.column):
                temp = black[i][j]
                black[i][j] = black[self.row - 1 - i][j]
                black[self.row - 1 - i][j] = temp

        black = black * -1
        self.state = black

    def remove_non_attacks(self, all_moves):
        for move in all_moves:
            # For Valid Moves
            if move[4] == 1:
                if True:
                    # For Normal Pieces
                    if self.state[move[0]][move[1]] == 1:
                        if abs(move[0] - move[2]) != 2:
                            move[4] = 0
                    # For King Pieces
                    else:
                        # if abs(move[0] - move[2]) > 1:
                        # Up
                        if move[0] - move[2] > 0:
                            # Left
                            if move[1] - move[3] > 0:
                                if self.state[move[2] + 1][move[3] + 1] not in set([-1, -2]):
                                    move[4] = 0
                            # Right
                            else:
                                if self.state[move[2] + 1][move[3] - 1] not in set([-1, -2]):
                                    move[4] = 0
                        # Down
                        else:
                            # Left
                            if move[1] - move[3] > 0:
                                if self.state[move[2] - 1][move[3] + 1] not in set([-1, -2]):
                                    move[4] = 0
                            # Right
                            else:
                                if self.state[move[2] - 1][move[3] - 1] not in set([-1, -2]):
                                    move[4] = 0
        return all_moves

    def attack_move_available(self, all_moves):
        attack_move_available = False
        for move in all_moves:
            # For Valid Moves
            if move[4] == 1:
                if True:
                    # For Normal Pieces
                    if self.state[move[0]][move[1]] == 1:
                        if abs(move[0] - move[2]) == 2:
                            attack_move_available = True
                            break
                    # For King Pieces
                    else:
                        if abs(move[0] - move[2]) > 1:
                            # Up
                            if move[0] - move[2] > 0:
                                # Left
                                if move[1] - move[3] > 0:
                                    if self.state[move[2] + 1][move[3] + 1] in set([-1, -2]):
                                        attack_move_available = True
                                        break
                                # Right
                                else:
                                    if self.state[move[2] + 1][move[3] - 1] in set([-1, -2]):
                                        attack_move_available = True
                                        break
                            # Down
                            else:
                                # Left
                                if move[1] - move[3] > 0:
                                    if self.state[move[2] - 1][move[3] + 1] in set([-1, -2]):
                                        attack_move_available = True
                                        break
                                # Right
                                else:
                                    if self.state[move[2] - 1][move[3] - 1] in set([-1, -2]):
                                        attack_move_available = True
                                        break
        return attack_move_available

    def if_attack_move(self, move):
        # For Normal Pieces
        if self.state[move[0]][move[1]] == 1:
            if abs(move[0] - move[2]) == 2:
                return True
        # For King Pieces
        else:
            if abs(move[0] - move[2]) > 1:
                # Up
                if move[0] - move[2] > 0:
                    # Left
                    if move[1] - move[3] > 0:
                        if self.state[move[2] + 1][move[3] + 1] in set([-1, -2]):
                            return True
                    # Right
                    else:
                        if self.state[move[2] + 1][move[3] - 1] in set([-1, -2]):
                            return True
                # Down
                else:
                    # Left
                    if move[1] - move[3] > 0:
                        if self.state[move[2] - 1][move[3] + 1] in set([-1, -2]):
                            return True
                    # Right
                    else:
                        if self.state[move[2] - 1][move[3] - 1] in set([-1, -2]):
                            return True
        return False

    def remove_reverse_moves(self):
        all_moves = self.get_valid_moves()
        for move in all_moves:
            if self.state[move[0]][move[1]] == 1:
                if (move[0] - move[2]) < 0:
                    move[4] = 0
        return all_moves

    def remove_except_current(self, action):
        all_moves = self.get_valid_moves()
        x, y = action[2:4]
        for move in all_moves:
            if move[0] != x and move[1] != y:
                move[4] = 0
        return all_moves
