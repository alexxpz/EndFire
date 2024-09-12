from Game import *
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.optimizers import Adam

import random
from tqdm import tqdm


class ReplayMemory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []

    def store(self, state, action, reward, next_state, done):
        if len(self.memory) >= self.capacity:
            self.memory.pop(0)
        self.memory.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)


# Créer le modèle du réseau de neurones
def create_model(input_shape, output_shape, LR):
    optimizer = Adam(learning_rate=LR)

    model = Sequential()
    model.add(Dense(1024, input_shape=input_shape, activation='relu'))
    model.add(Dense(1024, activation='relu'))
    model.add(Dense(512, activation='relu'))
    model.add(Dense(256, activation='relu'))
    model.add(Flatten())
    model.add(Dense(output_shape, activation='linear'))
    model.compile(loss='mse', optimizer=optimizer)
    return model


def train_dqn(model, memory, batch_size, discount_factor):
    if len(memory) < batch_size:
        return

    batch = memory.sample(batch_size)
    states, actions, rewards, next_states, dones = zip(*batch)
    states = np.array(states)
    next_states = np.array(next_states)

    q_values = model.predict(states)
    next_q_values = model.predict(next_states)

    for i, (state, action, reward, next_state, done) in enumerate(batch):
        target_q = reward
        if not done:
            target_q += discount_factor * np.max(next_q_values[i])
        q_values[i, action] = target_q

    model.fit(states, q_values, verbose=0)


def choose_action(model, state, epsilon, n_actions):
    if np.random.rand() < epsilon:
        return np.random.randint(n_actions)
    else:
        q_values = model.predict(state.reshape(1, -1))
        return np.argmax(q_values[0])


direction_dict = {
    1: "Up",
    2: "Right",
    3: "Down",
    4: "Left"
}
spell_dict = {
    1: "Astral",
    2: "Double",
    3: "Attract",
    4: "Skip"
}

n_episodes = 200
batch_size = 32
memory_capacity = 100000
discount_factor = 0.99
epsilon_start = 1.0
epsilon_end = 0.01
epsilon_decay = 0.95
LR = 0.001

model = create_model((31 * 31,), 13, LR)
memory = ReplayMemory(memory_capacity)

for episode in range(n_episodes):
    game = Game()
    state = np.array(game.grid.to_numeric())
    done = False
    killed_spirits = 0

    while not done:

        health = 40
        killed_spirits = 0

        turn = 0
        is_won = False

        while not is_won and health > 0:
            current_state = game.grid.to_numeric()

            turn += 1
            game.grid.convert_glyphs()

            if turn < 7:
                game.grid.generate_glyphs()
            else:
                health -= 1

            action = 10
            double_jump_left = 2
            skip_turn = False

            while not skip_turn and health > 0:

                if action == 0:
                    skip_turn = True
                    spell_index = 12
                    memory.store(current_state, spell_index, 3, game.grid.to_numeric(), done)
                    train_dqn(model, memory, batch_size, discount_factor)
                    print("Turn skipped, no more AP")
                    continue

                spell_index = choose_action(model, state, epsilon_start, 13)
                spell, direction = one_hot_to_action(spell_index, 4, 4)

                while (spell == 2 and double_jump_left == 0) or (spell == 3 and health <= 5):
                    spell_index = choose_action(model, state, epsilon_start, 13)
                    spell, direction = one_hot_to_action(spell_index, 4, 4)

                if spell is Constants.SpellType.SKIP:
                    skip_turn = True
                    memory.store(current_state, spell_index, 0, game.grid.to_numeric(), done)
                    train_dqn(model, memory, batch_size, discount_factor)
                    print("Turn skipped voluntarily")
                    continue

                current_state = game.grid.to_numeric()
                previous_killed_spirits = killed_spirits

                if spell == Constants.SpellType.ASTRAL_JUMP:
                    health, killed_spirits = game.grid.astral_jump(direction, health, killed_spirits)
                    if health <= 0:
                        done = True
                        memory.store(current_state, spell_index, 1, game.grid.to_numeric(), done)
                        train_dqn(model, memory, batch_size, discount_factor)
                    elif killed_spirits > previous_killed_spirits:
                        memory.store(current_state, spell_index, killed_spirits * 10, game.grid.to_numeric(), done)
                        train_dqn(model, memory, batch_size, discount_factor)
                    else:
                        memory.store(current_state, spell_index, 1, game.grid.to_numeric(), done)
                        train_dqn(model, memory, batch_size, discount_factor)
                elif spell == Constants.SpellType.DOUBLE_JUMP:
                    health, killed_spirits = game.grid.double_jump(direction, health, killed_spirits)
                    double_jump_left -= 1
                    if health <= 0:
                        done = True
                        memory.store(current_state, spell_index, -10, game.grid.to_numeric(), done)
                        train_dqn(model, memory, batch_size, discount_factor)
                    elif killed_spirits > previous_killed_spirits:
                        memory.store(current_state, spell_index, killed_spirits * 8, game.grid.to_numeric(), done)
                        train_dqn(model, memory, batch_size, discount_factor)
                    else:
                        memory.store(current_state, spell_index, .5, game.grid.to_numeric(), done)
                        train_dqn(model, memory, batch_size, discount_factor)
                elif spell == Constants.SpellType.ATTRACT :
                    health = game.grid.attract(direction, health)
                    if health <= 0:
                        done = True
                        memory.store(current_state, spell_index, -100, game.grid.to_numeric(), done)
                        train_dqn(model, memory, batch_size, discount_factor)
                    else:
                        memory.store(current_state, spell_index, -1, game.grid.to_numeric(), done)
                        train_dqn(model, memory, batch_size, discount_factor)

                action -= 1

                print(spell_dict[spell])
                if spell != 4:
                    print(direction_dict[direction])
                print(f'HP left = ', health)
                print(f'AP left = ', action)
                print(f'Spirits killed = ', killed_spirits)

                is_won = game.grid.is_won()

                if is_won:
                    done = True

        done = True

        train_dqn(model, memory, batch_size, discount_factor)
    print(f'Game #', episode + 1, f'finished with', killed_spirits, f'killed spirits')
    epsilon_start = max(epsilon_end, epsilon_start * epsilon_decay)
