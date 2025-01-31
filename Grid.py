from Constants import *
from Cell import Cell
import random
import numpy as np


class Grid:
    def __init__(self):
        self.cells = [[Cell(x, y, False) for y in range(Constants.GRID_SIZE)] for x in range(Constants.GRID_SIZE)]

    def get_cell(self, x, y):
        if not (Constants.GRID_SIZE > x >= 0 and Constants.GRID_SIZE > y >= 0):
            return None
        return self.cells[x][y]

    def get_player_cell(self):
        for i in range(Constants.GRID_SIZE):
            for j in range(Constants.GRID_SIZE):
                if self.get_cell(i, j).get_entity() == Constants.Entity.PLAYER:
                    return self.get_cell(i, j)

        return None

    def initialize(self):
        lines = Constants.GRID_SHAPE.split("\n")

        for i in range(Constants.GRID_SIZE):
            for j in range(Constants.GRID_SIZE):
                is_reachable = lines[i][j * 2] == 'O'

                self.cells[i][j] = Cell(i, j, is_reachable)

    def to_numeric(self):
        flat_grid = []

        for i in range(Constants.GRID_SIZE):
            for j in range(Constants.GRID_SIZE):
                cell = self.get_cell(i, j)
                if cell.is_reachable() is False:
                    flat_grid.append(0)  # Unreachable cell
                else:
                    if cell.has_glyph() is True:
                        if cell.get_entity() == Constants.Entity.PLAYER:
                            flat_grid.append(5)  # Glyph + player cell
                        elif cell.get_entity() == Constants.Entity.SPIRIT:
                            flat_grid.append(6)  # Glyph + spirit cell
                        else:
                            flat_grid.append(4)  # Glyph cell
                    else:
                        if cell.get_entity() == Constants.Entity.PLAYER:
                            flat_grid.append(2)  # Player cell
                        elif cell.get_entity() == Constants.Entity.SPIRIT:
                            flat_grid.append(3)  # Spirit cell
                        else:
                            flat_grid.append(1)  # Empty cell

        return flat_grid

    def jump(self, player_cell: Cell, target_cell: Cell, health: int, killed_spirits: int):

        if target_cell is None:
            return 0, killed_spirits

        player = player_cell.get_entity()
        target_entity = target_cell.get_entity()

        if not self.can_jump_and_push(target_cell):
            return 0, killed_spirits  # Game is lost

        health -= 1

        if health <= 0:
            return 0, killed_spirits  # Game is lost

        had_spirit = False

        if target_entity == Constants.Entity.SPIRIT:
            health += 1
            had_spirit = True

        player_cell.set_entity(None)
        target_cell.set_entity(player)

        if self.attract_spirits(target_cell, False, had_spirit):
            health = 0  # Game is lost

        if health > 0 and had_spirit:
            killed_spirits += 1

        return health, killed_spirits

    def astral_jump(self, direction, health, killed_spirits):
        player_cell = self.get_player_cell()
        x = 0
        y = 0

        if direction == Constants.Direction.UP:
            x = -1
        elif direction == Constants.Direction.RIGHT:
            y = 1
        elif direction == Constants.Direction.DOWN:
            x = 1
        elif direction == Constants.Direction.LEFT:
            y = -1

        target_cell = self.get_cell(player_cell.get_x() + x, player_cell.get_y() + y)

        return self.jump(player_cell, target_cell, health, killed_spirits)

    def double_jump(self, direction, health, killed_spirits):
        player_cell = self.get_player_cell()
        x = 0
        y = 0

        if direction == Constants.Direction.UP:
            x = -2
        elif direction == Constants.Direction.RIGHT:
            y = 2
        elif direction == Constants.Direction.DOWN:
            x = 2
        elif direction == Constants.Direction.LEFT:
            y = -2

        target_cell = self.get_cell(player_cell.get_x() + x, player_cell.get_y() + y)

        return self.jump(player_cell, target_cell, health, killed_spirits)

    def attract(self, direction, health):
        player_cell = self.get_player_cell()
        x = 0
        y = 0

        if direction == Constants.Direction.UP:
            x = -1
            y = 1
        elif direction == Constants.Direction.RIGHT:
            x = 1
            y = 1
        elif direction == Constants.Direction.DOWN:
            x = 1
            y = -1
        elif direction == Constants.Direction.LEFT:
            x = -1
            y = -1

        target_cell = self.get_cell(player_cell.get_x() + x, player_cell.get_y() + y)

        self.attract_spirits(target_cell, True, False)
        health -= 5

        return health

    def can_jump_and_push(self, target_cell):
        target_x = target_cell.get_x()
        target_y = target_cell.get_y()

        if not (target_cell.has_entity() and target_cell.get_entity() == Constants.Entity.SPIRIT):
            return True

        for x in range(target_x - 1, target_x + 2):
            for y in range(target_y - 1, target_y + 2):
                if not (x == target_x and y == target_y):
                    current_cell = self.get_cell(x, y)

                    if current_cell.is_reachable():
                        entity = current_cell.get_entity()

                        if entity == Constants.Entity.SPIRIT:
                            dx = x - target_x
                            dy = y - target_y
                            new_x = x + dx
                            new_y = y + dy

                            new_cell = self.get_cell(new_x, new_y)
                            if not new_cell.is_reachable() or new_cell.get_entity() == Constants.Entity.SPIRIT:
                                return False

                            if abs(dx) == abs(dy):
                                behind_1_cell = self.get_cell(x + dy, y)
                                if not behind_1_cell.is_reachable() or behind_1_cell.get_entity() == Constants.Entity.SPIRIT:
                                    return False

                                behind_2_cell = self.get_cell(x, y + dx)
                                if not behind_2_cell.is_reachable() or behind_2_cell.get_entity() == Constants.Entity.SPIRIT:
                                    return False

        # Si tous les esprits peuvent être poussés, retourne True
        return True

    def is_won(self):
        for i in range(Constants.GRID_SIZE):
            for j in range(Constants.GRID_SIZE):
                cell = self.get_cell(i, j)
                if cell.get_entity() == Constants.Entity.SPIRIT or cell.has_glyph():
                    return False
        return True

    def generate_glyphs(self):
        glyph_count = 0

        while glyph_count < 6:
            x = random.randint(0, Constants.GRID_SIZE - 1)
            y = random.randint(0, Constants.GRID_SIZE - 1)
            cell = self.get_cell(x, y)

            if cell.is_reachable() and not cell.has_entity() and not cell.has_glyph():
                cell.set_glyph(True)
                glyph_count += 1

    def convert_glyphs(self):
        for i in range(Constants.GRID_SIZE):
            for j in range(Constants.GRID_SIZE):
                cell = self.get_cell(i, j)
                if cell.has_glyph() and cell.get_entity() is None:
                    cell.set_entity(Constants.Entity.SPIRIT)
                cell.set_glyph(False)

    def generate_player(self, x, y):
        if 0 <= x < Constants.GRID_SIZE and 0 <= y < Constants.GRID_SIZE:
            player_cell = self.get_cell(x, y)
            if player_cell.is_reachable() and not player_cell.has_entity():
                player_cell.set_entity(Constants.Entity.PLAYER)
            else:
                raise RuntimeError(f"Cannot place player at cell ({x}, {y})")
        else:
            raise ValueError(f"Invalid coordinates: x={x}, y={y}")

    def attract_spirits(self, target_cell, from_attract_spell, had_spirit):
        target_x = target_cell.get_x()
        target_y = target_cell.get_y()
        is_game_over = False

        for distance in range(1, Constants.GRID_SIZE):
            for x in range(-distance, distance + 1):
                for y in range(-distance, distance + 1):
                    if abs(x) != distance and abs(y) != distance:
                        continue

                    current_x = target_x + x
                    current_y = target_y + y

                    # Exclure les cases situées à 1 case de distance de targetCell si hadSpirit est true
                    if had_spirit and abs(x) <= 1 and abs(y) <= 1:
                        continue

                    if 0 <= current_x < Constants.GRID_SIZE and 0 <= current_y < Constants.GRID_SIZE:
                        current_cell = self.get_cell(current_x, current_y)

                        if current_cell.is_reachable():
                            entity = current_cell.get_entity()

                            if entity == Constants.Entity.SPIRIT:
                                dx = -np.sign(x)
                                dy = -np.sign(y)

                                # Check if the spirit is in a diagonal position
                                if abs(x) == abs(y):
                                    new_x = current_x + dx
                                    new_y = current_y + dy

                                    new_cell = self.get_cell(new_x, new_y)
                                    if new_cell.is_reachable() and not new_cell.has_entity():
                                        new_cell.set_entity(entity)
                                        current_cell.set_entity(None)
                                        if new_cell == target_cell:
                                            is_game_over = True
                                    elif new_cell.get_entity() == Constants.Entity.PLAYER and not from_attract_spell:
                                        is_game_over = True
                                else:
                                    if abs(x) > abs(y):
                                        new_x = current_x + dx
                                        new_y = current_y
                                    else:
                                        new_x = current_x
                                        new_y = current_y + dy

                                    if 0 <= new_x < Constants.GRID_SIZE and 0 <= new_y < Constants.GRID_SIZE:
                                        new_cell = self.get_cell(new_x, new_y)
                                        if new_cell.is_reachable() and not new_cell.has_entity():
                                            new_cell.set_entity(entity)
                                            current_cell.set_entity(None)
                                        elif new_cell.get_entity() == Constants.Entity.PLAYER and not from_attract_spell:
                                            is_game_over = True
        return is_game_over

    def __str__(self) -> str:
        res = str()
        for i in range(Constants.GRID_SIZE):
            for j in range(Constants.GRID_SIZE):
                res += str(self.get_cell(i, j))
                if j < Constants.GRID_SIZE - 1:
                    res += " "
            res += "\n"
        return res
