import sys
from pdb import set_trace as bp


class IllegalColumnError(Exception):
    pass


class IllegalRowError(Exception):
    pass


class InvalidFileError(Exception):
    pass


class IllegalGameError(Exception):
    pass


def valid_game_params(*args):
    return args[2] <= min(args[:2])


def get_params(line):
    params = list(map(int, line.split()))

    if len(params) != 3:
        raise InvalidFileError

    if not valid_game_params(*params):
        raise IllegalGameError

    return params


class CollectZ:

    def __init__(self, first_line):
        # game params

        self.X, self.Y, self.Z = get_params(first_line)

        # keep track of current player
        self.current_player = 0

        self._won = 0

        # init grid
        self.grid = [[] for j in range(self.X)]

    def get_column(self, col_index):
        if col_index in range(self.X):
            return self.grid[col_index]
        else:
            raise IllegalColumnError

    def get_row(self, row_index):
        if row_index in range(self.Y):
            return ([col[row_index] for col in self.grid])
        else:
            raise IndexError('Invalid row_index')

    def get_diagonal(self):
        pass

    def append_move_to_grid(self, column):
        col = self.get_column(column)
        if len(col) < self.Y:
            self.grid[column].append(self.current_player)
        else:
            raise IllegalRowError

    def next_player(self):
        self.current_player = (self.current_player + 1) % 2

    def is_game_won(self):
        return bool(self._won)

    def winner(self):
        return (self._won + 1)

    def move(self, line):
        self.append_move_to_grid(line)

        # switch to next player
        self.next_player()


def parse_move(line):
    return int(line.strip())


def main():
    filename = sys.argv[1]

    with open(filename) as fp:
        line = fp.readline()

        # initialize game
        game = CollectZ(line)

        # read first move before loop
        line = fp.readline()

        while line:
            # check if valid line
            try:
                move = parse_move(line)
            except ValueError:
                return 'invalid line'

            if move and game.is_game_won():
                # 'Illegal continue'
                return 4

            try:
                game.move(move)
            except IllegalColumnError:
                return 6
            except IllegalRowError:
                return 5

            line = fp.readline()

    print(game.grid)
    bp()

    if game.is_game_won():
        # one of players won
        return game.winner()
    else:
        # 'Draw'
        return 0


if __name__ == "__main__":
    result = main()
    print(result)
