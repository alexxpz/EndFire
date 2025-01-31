from Game import *
import tensorflow as tf
import numpy as np
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression

LR = 1e-3
score_requirement = -1
n_games = 10


def initial_population():
    n_success = 0
    total_killed_spirits = 0
    training_data = []
    for i in range(n_games):
        game = Game()
        killed_spirits, grid_list, spell_list = game.start_game()
        total_killed_spirits += killed_spirits
        if killed_spirits > score_requirement:
            training_data.append([grid_list, spell_list, killed_spirits])
            n_success += 1
    average_killed_spirits = total_killed_spirits / n_games

    print(n_success)
    print(average_killed_spirits)
    return training_data


training_set = initial_population()

grids = []
actions = []
scores = []

for episode in training_set:
    game_grids = episode[0]
    game_actions = episode[1]
    game_scores = episode[2]

    # Ajouter les états, actions
    grids.extend(game_grids)
    actions.extend(game_actions)
    scores.extend([game_scores] * len(game_grids))


# Création du training set et validation set

train_percentage = 0.8
train_test_separator_index = round(train_percentage*len(grids))

print(train_test_separator_index)

grids_train = grids[0:train_test_separator_index]
actions_train = actions[0:train_test_separator_index]

grids_dev = grids[train_test_separator_index:len(grids)]
actions_dev = actions[train_test_separator_index:len(actions)]


