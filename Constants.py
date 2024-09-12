class Constants:
    GRID_SIZE = 31
    GRID_SHAPE = """- - - - - - - - - - - - - - - - O O O O O O - - - - - - - - -
- - - - - - - - - - - - - - - O O O O O O O O - - - - - - - -
- - - - - - - - - - - - - - O O O O O O O O O O - - - - - - -
- - - - - - - - - - - - - O O O O O O O O O O O O - - - - - -
- - - - - - - - - - - - O O O O O O O O O O O O O O - - - - -
- - - - - - - - - - - O O O O O O O O O O O O O O O O - - - -
- - - - - - - - - - O O O O O O O O O O O O O O O O O O - - -
- - - - - - - - - O O O O O O O O O O O O O O O O O O O O - -
- - - - - - - - O O O O O O O O O O O O O O O O O O O O O O -
- - - - - - - O O O O O O O O O O O O O O O O O O O O O O O O
- - - - - - O O O O O O O O O O O O O O O O O O O O O O O O O
- - - - - O O O O O O O O O O O O O O O O O O O O O O O O O O
- - - - O O O O O O O O O O O O O O O O O O O O O O O O O O O
- - - O O O O O O O O O O O O O O O O O O O O O O O O O O O O
- - O O O O O O O O O O O O O O O O O O O O O O O O O O O O -
- O O O O O O O O O O O O O O O O O O O O O O O O O O O O - -
O O O O O O O O O O O O O O O O O O O O O O O O O O O O - - -
O O O O O O O O O O O O O O O O O O O O O O O O O O O - - - -
O O O O O O O O O O O O O O O O O O O O O O O O O O - - - - -
- O O O O O O O O O O O O O O O O O O O O O O O O - - - - - -
- - O O O O O O O O O O O O O O O O O O O O O O - - - - - - -
- - - O O O O O O O O O O O O O O O O O - O O - - - - - - - -
- - - - O O O O O O O O O O O O O O O O O O - - - - - - - - -
- - - - - O O O O O O O O O O O O O O O O - - - - - - - - - -
- - - - - - O O O O O O O O O O O O O O - - - - - - - - - - -
- - - - - - - O O O O O O O O O O O O - - - - - - - - - - - -
- - - - - - - - O O O O O O O O O O - - - - - - - - - - - - -
- - - - - - - - - O O O O O O O O - - - - - - - - - - - - - -
- - - - - - - - - - O O O O O O - - - - - - - - - - - - - - -
- - - - - - - - - - - O O O O - - - - - - - - - - - - - - - -
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"""

    class SpellType:
        ASTRAL_JUMP = 1
        DOUBLE_JUMP = 2
        ATTRACT = 3
        SKIP = 4

    class Direction:
        UP = 1
        RIGHT = 2
        DOWN = 3
        LEFT = 4

    class Entity:
        PLAYER = 1
        SPIRIT = 2

