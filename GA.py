import copy

import numpy as np
from Game import *
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.optimizers import Adam
from tqdm import tqdm

from operator import attrgetter
import random


class GeneticAlgorithm:
    def __init__(self, population_size, mutation_rate, n_generations, input_shape, output_shape, LR):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.n_generations = n_generations
        self.input_shape = input_shape
        self.output_shape = output_shape
        self.LR = LR

    def create_model(self):
        optimizer = Adam(learning_rate=self.LR)

        model = Sequential()
        model.add(Dense(128, input_shape=self.input_shape, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Flatten())
        model.add(Dense(self.output_shape, activation='linear'))
        model.compile(loss='mse', optimizer=optimizer)
        return model

    def initialize_population(self):
        return [self.create_model() for _ in range(self.population_size)]

    def mutate(self, model):
        for layer in model.layers:
            weights = layer.get_weights()
            for i in range(len(weights)):
                mutation_mask = np.random.uniform(0, 1, weights[i].shape) < self.mutation_rate
                mutation_values = np.random.standard_normal(weights[i].shape)
                weights[i] += mutation_mask * mutation_values
            layer.set_weights(weights)

    def crossover(self, parent1, parent2):
        child = self.create_model()

        for i, layer in enumerate(child.layers):
            parent1_weights = parent1.layers[i].get_weights()
            parent2_weights = parent2.layers[i].get_weights()

            child_weights = []
            for j in range(len(parent1_weights)):
                child_weights.append((parent1_weights[j] + parent2_weights[j]) / 2)

            layer.set_weights(child_weights)

        return child

    def fitness(self, model, game):
        health = 40
        killed_spirits = 0

        turn = 0
        is_won = False

        while not is_won and health > 0:
            turn += 1
            game.grid.convert_glyphs()

            if turn < 7:
                game.grid.generate_glyphs()
            else:
                health -= 1

            action = 10
            double_jump_left = 2
            skip_turn = False

            while action > 0 and not skip_turn:

                if action == 0:
                    skip_turn = True
                    continue

                spell, direction = one_hot_to_action(np.argmax(model.predict(np.array(game.grid.to_numeric()).reshape(1,-1))[0]), 4, 4)

                if spell is Constants.SpellType.SKIP:
                    skip_turn = True
                    continue

                if spell == Constants.SpellType.ASTRAL_JUMP:
                    health, killed_spirits = game.grid.astral_jump(direction, health, killed_spirits)
                elif spell == Constants.SpellType.DOUBLE_JUMP:
                    health, killed_spirits = game.grid.double_jump(direction, health, killed_spirits)
                    double_jump_left -= 1
                elif spell == Constants.SpellType.ATTRACT:
                    health = game.grid.attract(direction, health)

                action -= 1

                if health <= 0:
                    return killed_spirits + 1

                is_won = game.grid.is_won()

                if is_won:
                    return killed_spirits + 1

        return killed_spirits + 1

    def run(self):
        population = self.initialize_population()
        print("Population generated")
        best_model = None

        for generation in tqdm(range(self.n_generations)):
            game = Game()
            print("Game generated")

            fitness_scores = []
            for model in population:
                fitness_score = self.fitness(model, copy.deepcopy(game))
                fitness_scores.append(fitness_score)
            print(fitness_scores)
            best_model = population[np.argmax(fitness_scores)]
            print("Best model generated")

            new_population = [best_model]
            for _ in range(self.population_size - 1):
                parent1 = random.choices(population, weights=fitness_scores)[0]
                parent2 = random.choices(population, weights=fitness_scores)[0]

                child = self.crossover(parent1, parent2)
                self.mutate(child)
                new_population.append(child)

            population = new_population
            print(f'Generation {generation + 1}: Best killed spirits: {max(fitness_scores) - 1}')

        return best_model


population_size = 100
mutation_rate = 0.1
n_generations = 10
input_shape = (31 * 31,)
output_shape = 13
LR = 0.001

ga = GeneticAlgorithm(population_size, mutation_rate, n_generations, input_shape, output_shape, LR)

print("Algorithm generated")

best_candidate = ga.run()
print(best_candidate.summary())


# while not done:
#     action = np.argmax(best_candidate.predict(state.reshape(1, -1))[0])
#     state, killed_spirits, done = test_game.step(action)
#
# print(f'Testing the best model: Killed spirits: {killed_spirits}')