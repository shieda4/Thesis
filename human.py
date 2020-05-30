from termcolor import colored


def list_moves(all_moves):
    idx = []
    for i, move in enumerate(all_moves):
        if move[4] == 1:
            print(i, end=' -> ')
            print(move)
            idx.append(i)
    return idx


class Human:
    def __init__(self):
        pass

    def get_move(self, game, chain=False, prev_move=None):
        if chain is False:
            valid_moves = game.remove_reverse_moves()
            if game.attack_move_available(valid_moves):
                valid_moves = game.remove_non_attacks(valid_moves)
        else:
            valid_moves = game.remove_non_attacks(game.remove_except_current(prev_move))
        indexes = list_moves(valid_moves)
        selected_move = None
        while not selected_move in set(indexes):
            selected_move = int(input('Select move index: '))
            if selected_move in set(indexes):
                return valid_moves[selected_move]
            else:
                print('Invalid selection')
