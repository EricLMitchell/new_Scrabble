from pydraw import *
from enum import Enum

# Screen setup
screen_width = 900
screen_height = int(screen_width * (2 / 3))
screen = Screen(screen_width, screen_height, "Scrabble")

# size classification
TILE_SIZE = screen_width / 25
BOARD_DIMENSION = 15  # dimension value in number of cells, works best when odd

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

        def color(self):
            if self.name == 'DOUBLE_LETTER':
                return Color('cyan')
            elif self.name == 'TRIPLE_LETTER':
                return Color('blue')
            elif self.name == 'DOUBLE_WORD':
                return Color('salmon')
            elif self.name == 'TRIPLE_WORD':
                return Color('red')
            else:
                return Color('white')

    def __init__(self, screen, x, y, cell_width, cell_height, bonus):
        self.screen = screen

        self.x = x
        self.y = y

        self.cell_width = cell_width
        self.cell_height = cell_height

        self.bonus = bonus

        # make the cell
        self.cell = Rectangle(self.screen, self.x, self.y, self.cell_width, self.cell_height,
                              color=self.bonus.color(), border=Color('black'))

        # center on the object
        self.text = Text(self.screen, self.bonus.text(), self.x, self.y, size=16, bold=True)
        self.text.center(self.cell.center())

    def set_color(self, color):
        """
        Set the color of an individual cell
        :param color: Color() from pydraw
        :return: N/A
        """
        self.cell.color(color)

    def get_x(self):
        return self.cell.x()

    def get_y(self):
        return self.cell.y()

    # revisit getter vs property
    def get_center(self):
        return self.cell.center()

    def contains(self, object):
        return self.cell.contains(object)


class Grid:
    # dictionary storing which cell locations correspond to bonus values
    bonus_location_dict = {
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
        self._grid_list = []

        for r in range(0, BOARD_DIMENSION):
            column = []  # temporary list to hold the elements in the column
            y_shift = r * self.cell_height  # y location shift changes when a new row is created
            for c in range(0, BOARD_DIMENSION):
                x_shift = c * self.cell_width  # x location shift is modified by which column it is in
                bonus = self.check_bonus(r, c)
                column.append(Cell(screen, self.x + x_shift, self.y + y_shift,
                                   self.cell_width, self.cell_height, bonus))
            self._grid_list.append(column)

        # make the center tile red with a circle in it
        center_tile = self._grid_list[math.floor(grid_width / 2)][math.floor(grid_height / 2)]
        center_tile.set_color(Color('red'))
        scale_factor = 2 / 3
        center_symbol = Oval(self.screen, center_tile.get_x(), center_tile.get_y(),
                             self.cell_width * scale_factor, self.cell_height * scale_factor,
                             color=Color('white'), border=Color('black'))
        center_symbol.center(center_tile.get_center())

    @staticmethod
    def check_bonus(r, c):
        """
        Checks if a certain cell location should contain a bonus value
        :param r: row of the cell
        :param c: column of the cell
        :return: Cell.Bonus value
        """
        if (r, c) not in Grid.bonus_location_dict:
            return Cell.Bonus.NONE
        else:
            return Grid.bonus_location_dict[(r, c)]

    @property
    def grid_list(self):
        return self._grid_list


class Tile:
    def __init__(self, screen, x, y, tile_width, tile_height, letter=''):
        self.screen = screen

        self.x = x
        self.y = y

        self.tile_width = tile_width
        self.tile_height = tile_height

        # make any inserted string uppercase
        letter = letter.upper()
        self._letter = letter

        self.tile = Rectangle(screen, self.x, self.y, self.tile_width, self.tile_height,
                              color=Color('tan'), border=Color('black'))

        self.text = Text(self.screen, self.letter, self.tile.x(), self.tile.y(),
                         bold=True, color=Color('Black'), size=24)
        self.text.center(self.tile.center())

        self._selected = False

    @property
    def letter(self):
        return self._letter

    @letter.setter
    def letter(self, new_letter):
        self._letter = new_letter

        # update the text
        self.text.text(new_letter)
        self.text.center(self.tile.center())

    # contains method for drag-n-drop
    def contains(self, location):
        return self.tile.contains(location)

    def center(self):
        return self.tile.center()

    def center(self, location):
        self.tile.center(location)
        self.text.center(self.tile.center())

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, selected):
        self._selected = selected


board = Grid(screen, grid_start_x, grid_start_y, BOARD_DIMENSION, BOARD_DIMENSION, TILE_SIZE, TILE_SIZE)
test_tile = Tile(screen, 10, 10, TILE_SIZE, TILE_SIZE, 'C')

# list containing all usable game tiles
all_tiles = [test_tile]


# Mouse Functions in pydraw package
class Mouse(Enum):
    LEFT = 1
    MIDDLE = 2
    RIGHT = 3


def mouseup(location, button):
    for tile in all_tiles:
        # if the cell is occupied, do not snap
        # otherwise, snap
        tile.selected = False


def mousedown(location, button):
    # select a tile/tell which tile is selected
    for tile in all_tiles:
        if tile.contains(location):
            tile.selected = True


def mousedrag(location, button):
    for tile in all_tiles:
        if tile.selected:
            tile.center(location)


# make the tile follow the mouse center

screen.listen()

running = True
FPS = 30
while running:
    screen.update()
    screen.sleep(1 / FPS)
screen.stop()
