from game import Game
from neural_network import Residual
import numpy as np
import time


def normalize(prediction, valid_moves):
    prediction = prediction[0]
    for i in range(280):
        if valid_moves[i][4] != 1:
            prediction[i] = 0
    prob_sum = sum(prediction)
    for i in range(len(prediction)):
        prediction[i] = prediction[i] / prob_sum
    # prediction = prediction[0] / prob_sum
    return prediction

def store_state(storage, state, value):
    list = [np.expand_dims(state, axis=0), value, 0]
    storage.append(list)
    pass



player1 = Dama()
net1 = Residual()
player2 = Dama()
net2 = Residual()
is_over = player1.check_game_over()

steps = 0
t = time.time()

storage = []

while not is_over:
    if steps % 2 == 1:
        print(player1.state)
        policy, value = net1.predict(player1.state)
        prediction = normalize(policy, player1.get_valid_moves())
        store_state(storage, player1.state, value)
        player1.play_action(player1.get_valid_moves()[np.argmax(prediction)])
        print(player1.get_valid_moves()[np.argmax(prediction)], end='\n')
        player2.state = player1.flip_perspective()
        is_over = player1.check_game_over()
        if is_over:
            print('Player2 Won')
    else:
        print(player2.state)
        policy, value = net2.predict(player2.state)
        prediction = normalize(policy, player2.get_valid_moves())
        store_state(storage, player2.state, value)
        player2.play_action(player2.get_valid_moves()[np.argmax(prediction)])
        print(player2.get_valid_moves()[np.argmax(prediction)], end='\n')
        player1.state = player2.flip_perspective()
        is_over = player2.check_game_over()
        if is_over:
            print('Player1 Won')
    steps += 1
print((time.time() - t))
