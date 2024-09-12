from Game import *
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers import Adam


# Créer le modèle du réseau de neurones
def create_model(input_shape, output_shape):
    model = Sequential()
    model.add(Dense(128, input_shape=input_shape, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Flatten())
    model.add(Dense(output_shape, activation='linear'))
    model.compile(loss='mse', optimizer=Adam(lr=0.001))
    return model


# Convertir les actions en un vecteur one-hot
def action_to_one_hot(action, direction, n_actions, n_directions):
    action_vector = np.zeros(n_actions + n_directions)
    action_vector[action] = 1
    if direction is not None:
        action_vector[n_actions + direction] = 1
    return action_vector


# Convertir les actions one-hot en index
def one_hot_to_action(action_vector, n_actions, n_directions):
    action = np.argmax(action_vector[:n_actions])
    direction = np.argmax(action_vector[n_actions:])
    if direction == 0:
        direction = None
    return action, direction


class GameEnvironment:
    def __init__(self):
        self.game = None
        self.state_size = 31 * 31
        self.action_size = 13
        self.n_actions = 4
        self.n_directions = 4

    def reset(self):
        self.game = Game()
        self.game.start_game()
        state = np.array(self.game.grid.to_numeric())
        return state

    def step(self, action, direction):
        state, killed_spirits, done = self.game.perform_action(action, direction)
        state = np.array(state)
        reward = killed_spirits
        return state, reward, done

    def perform_action(self, action, direction):
        return
        # Ajoutez ici le code pour exécuter l'action et la direction
        # correspondantes dans le jeu et renvoyer le nouvel état, les esprits
        # tués et si le jeu est terminé ou non.


# Classe Agent
class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.model = create_model((state_size,), action_size)

    def act(self, state, epsilon):
        if np.random.rand() <= epsilon:
            return np.random.randint(self.action_size)
        act_values = self.model.predict(state.reshape(1, -1))
        return np.argmax(act_values[0])

    def train(self, state, action, reward, next_state, done):
        target = reward
        if not done:
            target = (reward + 0.99 * np.amax(self.model.predict(next_state.reshape(1, -1))[0]))
        target_f = self.model.predict(state.reshape(1, -1))
        target_f[0][action] = target
        self.model.fit(state.reshape(1, -1), target_f, epochs=1, verbose=0)


# Entraînement de l'agent
def train_agent(agent, env, n_episodes, epsilon_decay):
    for episode in range(n_episodes):
        state = env.reset()
        done = False
        score = 0
        while not done:
            action_index = agent.act(state, epsilon)
            action, direction = one_hot_to_action(action_index, env.n_actions, env.n_directions)
            next_state, reward, done = env.step(action, direction)
            agent.train(state, action_index, reward, next_state, done)
            state = next_state
            score += reward
        epsilon_decay *= epsilon
        print(f"Episode {episode}/{n_episodes} - Score: {score}")


# Initialisation de l'environnement et de l'agent
state_size = 31 * 31
action_size = 13
env = GameEnvironment()
agent = DQNAgent(state_size, action_size)

# Entraînement de l'agent
n_episodes = 1000
epsilon = 1.0
epsilon_decay = 0.995
train_agent(agent, env, n_episodes, epsilon)
