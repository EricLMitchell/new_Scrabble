from pydraw import *
from enum import Enum

# Screen setup
screen_width = 900
screen_height = int(screen_width * (2/3))
screen = Screen(screen_width, screen_height, "Scrabble")

# size classification
TILE_SIZE = screen_width / 25
BOARD_DIMENSION = 15  # rename this variable

# calculate screen margins
screen_x_margin = screen_width - (BOARD_DIMENSION * TILE_SIZE)
screen_y_margin = screen_height - (BOARD_DIMENSION * TILE_SIZE)

# parts of the screen dimension left over from after the grid
grid_start_x = screen_x_margin / 2
grid_start_y = screen_y_margin / 2


class Cell:
    class Bonus(Enum):
        NONE = 0
        DOUBLE_LETTER = 1
        TRIPLE_LETTER = 2
        DOUBLE_WORD = 3
        TRIPLE_WORD = 4

        def text(self):
            if self.name == 'DOUBLE_LETTER':
                return 'DL'
            elif self.name == 'TRIPLE_LETTER':
                return 'TL'
            elif self.name == 'DOUBLE_WORD':
                return 'DW'
            elif self.name == 'TRIPLE_WORD':
                return 'TW'
            else:
                return ''

    bonus_colors_dict = {
        Bonus.NONE: Color('white'),
        Bonus.DOUBLE_LETTER: Color('cyan'),
        Bonus.TRIPLE_LETTER: Color('blue'),
        Bonus.DOUBLE_WORD: Color('salmon'),
        Bonus.TRIPLE_WORD: Color('red')
    }

    def __init__(self, screen, x, y, cell_width, cell_height, bonus):
        self.screen = screen

        self.x = x
        self.y = y

        self.cell_width = cell_width
        self.cell_height = cell_height

        self.bonus = bonus

        # make the cell
        self.cell = Rectangle(self.screen, self.x, self.y, self.cell_width, self.cell_height,
                              color=Cell.bonus_colors_dict[self.bonus], border=Color('black'))

        # center on the object
        self.text = Text(self.screen, self.bonus.text(), self.x, self.y, size=16, bold=True)
        self.text.center(self.cell.center())


class Grid:
    # dictionary storing the bonus values of all the tiles
    bonuses_dict = {
        # DOUBLE LETTER LOCATIONS
        (0, 3): Cell.Bonus.DOUBLE_LETTER, (0, 11): Cell.Bonus.DOUBLE_LETTER,
        (2, 6): Cell.Bonus.DOUBLE_LETTER, (2, 8): Cell.Bonus.DOUBLE_LETTER,
        (3, 0): Cell.Bonus.DOUBLE_LETTER, (3, 7): Cell.Bonus.DOUBLE_LETTER,
        (3, 14): Cell.Bonus.DOUBLE_LETTER, (6, 2): Cell.Bonus.DOUBLE_LETTER,
        (6, 6): Cell.Bonus.DOUBLE_LETTER, (6, 8): Cell.Bonus.DOUBLE_LETTER,
        (6, 12): Cell.Bonus.DOUBLE_LETTER, (7, 3): Cell.Bonus.DOUBLE_LETTER,
        (7, 11): Cell.Bonus.DOUBLE_LETTER, (8, 2): Cell.Bonus.DOUBLE_LETTER,
        (8, 6): Cell.Bonus.DOUBLE_LETTER, (8, 8): Cell.Bonus.DOUBLE_LETTER,
        (8, 12): Cell.Bonus.DOUBLE_LETTER, (11, 0): Cell.Bonus.DOUBLE_LETTER,
        (11, 7): Cell.Bonus.DOUBLE_LETTER, (11, 14): Cell.Bonus.DOUBLE_LETTER,
        (12, 6): Cell.Bonus.DOUBLE_LETTER, (12, 8): Cell.Bonus.DOUBLE_LETTER,
        (14, 3): Cell.Bonus.DOUBLE_LETTER, (14, 11): Cell.Bonus.DOUBLE_LETTER,

        # TRIPLE LETTER LOCATIONS
        (1, 5): Cell.Bonus.TRIPLE_LETTER, (1, 9): Cell.Bonus.TRIPLE_LETTER,
        (5, 1): Cell.Bonus.TRIPLE_LETTER, (5, 5): Cell.Bonus.TRIPLE_LETTER,
        (5, 9): Cell.Bonus.TRIPLE_LETTER, (5, 13): Cell.Bonus.TRIPLE_LETTER,
        (9, 1): Cell.Bonus.TRIPLE_LETTER, (9, 5): Cell.Bonus.TRIPLE_LETTER,
        (9, 9): Cell.Bonus.TRIPLE_LETTER, (9, 13): Cell.Bonus.TRIPLE_LETTER,
        (13, 5): Cell.Bonus.TRIPLE_LETTER, (13, 9): Cell.Bonus.TRIPLE_LETTER,

        # DOUBLE WORD LOCATIONS
        (1, 1): Cell.Bonus.DOUBLE_WORD, (2, 2): Cell.Bonus.DOUBLE_WORD,
        (3, 3): Cell.Bonus.DOUBLE_WORD, (4, 4): Cell.Bonus.DOUBLE_WORD,
        (10, 10): Cell.Bonus.DOUBLE_WORD, (11, 11): Cell.Bonus.DOUBLE_WORD,
        (12, 12): Cell.Bonus.DOUBLE_WORD, (13, 13): Cell.Bonus.DOUBLE_WORD,
        (13, 1): Cell.Bonus.DOUBLE_WORD, (12, 2): Cell.Bonus.DOUBLE_WORD,
        (11, 3): Cell.Bonus.DOUBLE_WORD, (10, 4): Cell.Bonus.DOUBLE_WORD,
        (4, 10): Cell.Bonus.DOUBLE_WORD, (3, 11): Cell.Bonus.DOUBLE_WORD,
        (2, 12): Cell.Bonus.DOUBLE_WORD, (1, 13): Cell.Bonus.DOUBLE_WORD,

        # TRIPLE WORD LOCATIONS
        (0, 0): Cell.Bonus.TRIPLE_WORD, (0, 7): Cell.Bonus.TRIPLE_WORD,
        (0, 14): Cell.Bonus.TRIPLE_WORD, (7, 0): Cell.Bonus.TRIPLE_WORD,
        (7, 14): Cell.Bonus.TRIPLE_WORD, (14, 0): Cell.Bonus.TRIPLE_WORD,
        (14, 7): Cell.Bonus.TRIPLE_WORD, (14, 14): Cell.Bonus.TRIPLE_WORD
    }

    def __init__(self, screen, x, y, grid_width, grid_height, cell_width, cell_height):
        self.screen = screen

        self.x = x
        self.y = y

        self.grid_width = grid_width
        self.grid_height = grid_height

        self.cell_width = cell_width
        self.cell_height = cell_height

        # create rectangle grid
        r = 0
        c = 0
        grid_list = []

        for r in range(0, BOARD_DIMENSION):
            column = []  # temporary list to hold the elements in the column
            y_shift = r * self.cell_height  # y location shift changes when a new row is created
            for c in range(0, BOARD_DIMENSION):
                x_shift = c * self.cell_width  # x location shift is modified by which column it is in
                bonus = self.check_bonus(r, c)
                column.append(Cell(screen, self.x + x_shift, self.y + y_shift,
                                   self.cell_width, self.cell_height, bonus))
            grid_list.append(column)

    @staticmethod
    def check_bonus(r, c):
        """
        Checks if a certain cell location should contain a bonus value
        :param r: row of the cell
        :param c: column of the cell
        :return: Cell.Bonus value
        """
        if (r, c) not in Grid.bonuses_dict:
            return Cell.Bonus.NONE
        else:
            return Grid.bonuses_dict[(r, c)]


board = Grid(screen, grid_start_x, grid_start_y, BOARD_DIMENSION, BOARD_DIMENSION, TILE_SIZE, TILE_SIZE)

screen.stop()
