from Constants import *


class Cell:
    def __init__(self, x: int, y: int, reachable: bool):
        self.x = x
        self.y = y
        self.reachable = reachable
        self.glyph = False
        self.entity = None

    def get_x(self) -> int:
        return self.x

    def get_y(self) -> int:
        return self.y

    def has_glyph(self) -> bool:
        return self.glyph

    def is_reachable(self) -> bool:
        return self.reachable

    def get_entity(self) -> Constants:
        return self.entity

    def set_glyph(self, glyph: bool) -> None:
        self.glyph = glyph

    def set_reachable(self, reachable: bool) -> None:
        self.reachable = reachable

    def set_entity(self, entity: Constants.Entity or None) -> None:
        self.entity = entity

    def has_entity(self) -> bool:
        return self.entity is not None

    def __str__(self) -> str:
        if not self.reachable:
            return "-"

        if self.entity is not None:
            if self.entity == Constants.Entity.PLAYER:
                if self.glyph:
                    return "p"
                return "P"
            elif self.entity == Constants.Entity.SPIRIT:
                if self.glyph:
                    return "s"
                return "S"

        if self.glyph:
            return "G"

        return "+"
