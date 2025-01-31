from Grid import *
from Constants import *
import random
import copy


def ask_spell(double_jump_left):
    print("Spell : ")
    user_input = input().strip()

    while ((
                   user_input != "astral" and user_input != "double" and user_input != "attract" and user_input != "skip") or (
                   user_input == "double" and double_jump_left == 0)):
        user_input = input().strip()

    if user_input == "astral":
        return Constants.SpellType.ASTRAL_JUMP
    elif user_input == "double":
        return Constants.SpellType.DOUBLE_JUMP
    elif user_input == "attract":
        return Constants.SpellType.ATTRACT
    else:
        return Constants.SpellType.SKIP


def ask_direction():
    print("Direction : ")
    user_input = input().strip()

    while user_input not in ["up", "right", "down", "left"]:
        user_input = input().strip()

    if user_input == "up":
        return Constants.Direction.UP
    elif user_input == "right":
        return Constants.Direction.RIGHT
    elif user_input == "down":
        return Constants.Direction.DOWN
    elif user_input == "left":
        return Constants.Direction.LEFT

    return Constants.Direction.UP


def get_random_spell(double_jump_left):
    random_spell = random.choice([Constants.SpellType.ASTRAL_JUMP,
                                  Constants.SpellType.DOUBLE_JUMP,
                                  Constants.SpellType.ATTRACT,
                                  Constants.SpellType.SKIP])
    if double_jump_left == 0:
        random_spell = random.choice([Constants.SpellType.ASTRAL_JUMP,
                                      Constants.SpellType.ATTRACT,
                                      Constants.SpellType.SKIP])

    return random_spell


def get_random_direction():
    random_direction = random.choice([Constants.Direction.UP,
                                      Constants.Direction.DOWN,
                                      Constants.Direction.LEFT,
                                      Constants.Direction.RIGHT])

    return random_direction

def one_hot_to_action(spell_index, n_actions, n_directions):
    direction = None
    if spell_index == 12:
        action = 4
    else:
        action = int(np.ceil((spell_index + 1) / n_actions))
        direction = (spell_index % 4) + 1

    return action, direction

class Game:
    def __init__(self):
        self.grid = Grid()
        self.grid.initialize()
        self.grid.generate_player(16, 15)

    def start_manual_game(self):
        health = 40
        killed_spirits = 0

        turn = 0
        is_won = False

        while not is_won and health > 0:
            turn += 1
            print("======")
            print(f'TURN', turn)
            print("======")
            self.grid.convert_glyphs()

            if turn < 7:
                self.grid.generate_glyphs()
            else:
                health -= 1

            action = 10
            double_jump_left = 2
            skip_turn = False

            while action > 0 and not skip_turn:
                print(self.grid)
                print(f'HP = ', health)
                print(f'AP = ', action)
                print(f'KILLED SPIRITS = ', killed_spirits)
                spell = ask_spell(double_jump_left)

                if spell is Constants.SpellType.SKIP:
                    skip_turn = True
                    continue

                direction = ask_direction()

                if spell == Constants.SpellType.ASTRAL_JUMP:
                    health, killed_spirits = self.grid.astral_jump(direction, health, killed_spirits)
                elif spell == Constants.SpellType.DOUBLE_JUMP:
                    health, killed_spirits = self.grid.double_jump(direction, health, killed_spirits)
                    double_jump_left -= 1
                elif spell == Constants.SpellType.ATTRACT:
                    health = self.grid.attract(direction, health)

                action -= 1

                if health == 0:
                    print("Lose")
                    return killed_spirits

                is_won = self.grid.is_won()

                if is_won:
                    print("Win")
                    return killed_spirits

    def start_game(self):
        grid_list = list()
        spell_list = list()

        health = 40
        killed_spirits = 0

        turn = 0
        is_won = False

        while not is_won and health > 0:
            turn += 1
            self.grid.convert_glyphs()

            if turn < 7:
                self.grid.generate_glyphs()
            else:
                health -= 1

            action = 10
            double_jump_left = 2
            skip_turn = False

            while action > 0 and not skip_turn:
                spell = get_random_spell(double_jump_left)

                if spell is Constants.SpellType.SKIP:
                    skip_turn = True
                    spell_list.append([spell, None])
                    grid_list.append(self.grid.to_numeric())
                    continue

                direction = get_random_direction()

                if spell == Constants.SpellType.ASTRAL_JUMP:
                    health, killed_spirits = self.grid.astral_jump(direction, health, killed_spirits)
                elif spell == Constants.SpellType.DOUBLE_JUMP:
                    health, killed_spirits = self.grid.double_jump(direction, health, killed_spirits)
                    double_jump_left -= 1
                elif spell == Constants.SpellType.ATTRACT:
                    health = self.grid.attract(direction, health)

                spell_list.append([spell, direction])
                grid_list.append(self.grid.to_numeric())
                action -= 1

                if health <= 0:
                    return killed_spirits, grid_list, spell_list

                is_won = self.grid.is_won()

                if is_won:
                    return killed_spirits, grid_list, spell_list

        return killed_spirits, grid_list, spell_list

    def start_game_with_model(self, trained_model):
        health = 40
        killed_spirits = 0

        turn = 0
        is_won = False

        while not is_won and health > 0:
            turn += 1
            self.grid.convert_glyphs()

            if turn < 7:
                self.grid.generate_glyphs()
            else:
                health -= 1

            action = 10
            double_jump_left = 2
            skip_turn = False

            while action > 0 and not skip_turn:
                grid_numeric = self.grid.to_numeric()
                predicted_one_hot = trained_model.predict(np.array([grid_numeric]))[0]
                spell, direction = one_hot_to_action(predicted_one_hot, 4, 4)

                if spell is Constants.SpellType.SKIP:
                    skip_turn = True
                    continue

                if spell == Constants.SpellType.ASTRAL_JUMP:
                    health, killed_spirits = self.grid.astral_jump(direction, health, killed_spirits)
                elif spell == Constants.SpellType.DOUBLE_JUMP:
                    health, killed_spirits = self.grid.double_jump(direction, health, killed_spirits)
                    double_jump_left -= 1
                elif spell == Constants.SpellType.ATTRACT:
                    health = self.grid.attract(direction, health)

                action -= 1

                if health <= 0:
                    return killed_spirits

                is_won = self.grid.is_won()

                if is_won:
                    return killed_spirits
        return killed_spirits
