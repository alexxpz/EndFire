def action_to_one_hot(action, direction, n_actions, n_directions):
    one_hot_vector = np.zeros((n_actions - 1) * n_directions + 1, dtype=int)
    if direction is None:
        one_hot_vector[len(one_hot_vector) - 1] = 1
    else:  # Si l'action a une direction associée
        one_hot_vector[(action - 1) * n_actions + direction - 1] = 1
    return one_hot_vector

def initial_population():
    training_data = []
    for i in range(n_games):
        game = Game()
        killed_spirits, grid_list, spell_list = game.start_game()
        if killed_spirits > score_requirement:
            one_hot_spell_list = [action_to_one_hot(action, direction, 4, 4) for action, direction in spell_list]
            training_data.append([grid_list, one_hot_spell_list, killed_spirits])
    return training_data

model = create_model((31 * 31,), 13)
training_data = initial_population()

X = np.array([grid for game_data in training_data for grid in game_data[0]])
y = np.array([one_hot_action for game_data in training_data for one_hot_action in game_data[1]])

model.fit(X, y, epochs=100, batch_size=32)


