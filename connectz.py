from collections import namedtuple


# define multiple exceptions classes to map return codes in the task

class IllegalColumnError(Exception):
    # 6 Illegal column
    pass


class IllegalRowError(Exception):
    # 5 Illegal row
    pass


class InvalidFileError(Exception):
    # 8 Invalid file
    pass


class IllegalGameError(Exception):
    # 7 Illegal game
    pass


def check_valid_game_params(*args):
    """Check if dimensions describe a game that can be won."""
    return args[2] <= max(args[:2])


def check_all_positive_int(*args):
    """Check if all dimensions are postive integers, Invalid file otheriwse"""
    # must be handled separately to valid_game_params
    # Invalid file, not game specs
    return all(x > 0 for x in args)


def parse_game_dimensions(line):
    """Get params from first line. Convert to positive integer, return x,y,z"""

    # check if contains leading/trailing whitespace
    trimmed = line.rstrip('\n')
    if trimmed.startswith(' ') or trimmed.endswith(' '):
        raise InvalidFileError

    try:
        params = list(map(int, trimmed.split(' ')))
        # provide sep ' ' so that multiple whitespaces aren't grouped together
    except ValueError:
        raise InvalidFileError

    if len(params) != 3:
        # if less than 3 dimensions, treat as invalid file
        raise InvalidFileError
    elif not check_all_positive_int(*params):
        # exception if not all positive
        raise InvalidFileError
    elif not check_valid_game_params(*params):
        # game must be winnable
        raise IllegalGameError

    return params


def parse_move(line):
    """Check if move can be converted to postive integer."""
    trimmed = line.rstrip('\n')

    # check if contains any whitespace
    if ' ' in trimmed:
        raise ValueError
    else:
        number = int(trimmed)
        if number < 1:
            raise ValueError
        return number


# define a namedtuple to store information on last move
Point = namedtuple('Point', ['x', 'y'])


class Connectz:
    """
    Class representation of Connect Z game
    """

    def __init__(self, x, y, z):
        # game params
        self.X = x
        self.Y = y
        self.Z = z

        # keep track of current player
        self.current_player = 0
        self.won = 0

        # keep track of the last move
        self.last_move = Point(0, 0)

        # init grid as array of empty columns
        self.grid = [[] for j in range(self.X)]

    def get_last_column(self):
        """Get a column that has changed in last move. Slice only Z items."""
        return self.grid[self.last_move.x][-self.Z:]

    def get_last_row(self):
        """Get a row that has changed in last move. Only max Z items."""
        l_bound = max(0, self.last_move.x - self.Z)
        u_bound = min(self.X, self.last_move.x + self.Z)

        row = []
        for j in range(l_bound, u_bound + 1):
            try:
                row.append(self.grid[j][self.last_move.y])
            except IndexError:
                row.append(0)
        return row

    def get_last_upward_diagonal(self):
        """
        Get an upward diagonal that has changed in last move.
        Bound by grid size and Z.
        """
        l_bound = - min(min(self.last_move), self.Z)
        u_bound = min(max(self.X - self.last_move.x,
                          self.Y - self.last_move.y), self.Z)

        diag = []
        for j in range(l_bound, u_bound + 1):
            try:
                diag.append(self.grid[self.last_move.x + j]
                            [self.last_move.y + j])
            except IndexError:
                diag.append(0)
        return diag

    def get_last_downward_diagonal(self):
        """
        Get a downward diagonal that has changed in last move.
        Bound by grid size and Z.
        """
        l_bound = - min(min(self.last_move.x, self.Y -
                            self.last_move.y), self.Z)
        u_bound = min(max(self.X - self.last_move.x,
                          self.last_move.y), self.Z)

        diag = []
        for j in range(l_bound, u_bound + 1):
            try:
                diag.append(self.grid[self.last_move.x + j]
                            [self.last_move.y - j])
            except IndexError:
                diag.append(0)
        return diag

    def append_move_to_grid(self, column):
        """Function to reflect the move in the grid."""
        # convert user input to python index
        col_index = column - 1

        if col_index not in range(0, self.X):
            raise IllegalColumnError
        elif len(self.grid[col_index]) < self.Y:
            # append to column stack
            self.grid[col_index].append(self.current_player + 1)

            # set last_move variable, later used to check if game won
            self.last_move = Point(col_index, len(self.grid[col_index]) - 1)
        else:
            raise IllegalRowError

    def next_player(self):
        """Switcher between players."""
        self.current_player = (self.current_player + 1) % 2

    def is_game_won(self):
        """Getter if game won by one of the players."""
        return bool(self.won)

    def get_winner(self):
        """Get game winner."""
        return (self.won)
    
    @staticmethod
    def get_sublists(vec, length):
        """Get all sublist of desired length."""
        return (vec[i:(i+length)] for i in range(len(vec) - length + 1))

    @staticmethod
    def check_all_equal_is_winner(vec):
        """Check if a vector consists of one non-zero values."""
        unique = set(vec)
        return len(unique) <= 1 and 0 not in unique

    def check_vector_for_win(self, vec):
        """Check if any of row/column/diag sublists contain winning pattern."""
        for sublist in self.get_sublists(vec, self.Z):
            if self.check_all_equal_is_winner(sublist):
                self.won = self.current_player + 1
                break

    def check_if_winning_move(self):
        """Check if the lates move won the game."""
        # check one column just appended
        last_column = self.get_last_column()
        self.check_vector_for_win(last_column)

        # check only the row that has changed
        self.check_vector_for_win(self.get_last_row())

        # check all diagonals
        self.check_vector_for_win(self.get_last_upward_diagonal())
        self.check_vector_for_win(self.get_last_downward_diagonal())

    def move(self, line):
        """Move logic called on single file line."""
        # first make a move
        self.append_move_to_grid(line)

        # check if the move won the game
        self.check_if_winning_move()

        # switch to next player
        self.next_player()

    def check_complete_game(self):
        """Check if all grid spaces are filled."""
        return sum([len(self.grid[j])
                    for j in range(self.X)]) == self.X * self.Y


def main(filename):
    try:
        fp = open(filename, 'r')
        line = fp.readline()

        try:
            x, y, z = parse_game_dimensions(line)
        except InvalidFileError:
            return 8
        except IllegalGameError:
            return 7

        # initialize game
        game = Connectz(x, y, z)

        # read first move before loop
        line = fp.readline()

        while line:
            try:
                move = parse_move(line)
            except ValueError:
                # Invalid move line
                return 8

            if move and game.is_game_won():
                # Illegal continue
                return 4

            try:
                game.move(move)
            except IllegalColumnError:
                return 6
            except IllegalRowError:
                return 5

            line = fp.readline()

    except FileNotFoundError:
        # File error
        return 9

    if game.is_game_won():
        # one of players won
        return game.get_winner()
    elif game.check_complete_game():
        # draw
        return 0
    else:
        # Incomplete
        return 3


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print('connectz.py: Provide one input file')
    else:
        result = main(sys.argv[1])
        print(result)
