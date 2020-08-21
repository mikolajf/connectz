from collections import namedtuple


class IllegalColumnError(Exception):
    pass


class IllegalRowError(Exception):
    pass


class InvalidFileError(Exception):
    pass


class IllegalGameError(Exception):
    pass


def valid_game_params(*args):
    return args[2] <= max(args[:2])


def get_params(line):
    try:
        params = list(map(int, line.split()))
    except ValueError:
        raise InvalidFileError

    if len(params) != 3:
        raise InvalidFileError

    if not valid_game_params(*params):
        raise IllegalGameError

    return params


def get_sublists(vec, length):
    return (vec[i:(i+length)] for i in range(len(vec) - length + 1))


def check_all_equal(vec):
    unique = set(vec)
    return len(unique) <= 1 and 0 not in unique


Point = namedtuple('Point', ['x', 'y'])


class CollectZ:

    def __init__(self, x, y, z):
        # game params

        self.X = x
        self.Y = y
        self.Z = z

        # keep track of current player
        self.current_player = 0
        self._won = 0
        self._last_move = Point(0, 0)

        # init grid
        self.grid = [[] for j in range(self.X)]

    def get_last_column(self):
        return self.grid[self._last_move.x][-self.Z:]

    def get_last_row(self):
        l_bound = max(0, self._last_move.x - self.Z)
        u_bound = min(self.X, self._last_move.x + self.Z)

        row = []
        for j in range(l_bound, u_bound + 1):
            try:
                row.append(self.grid[j][self._last_move.y])
            except IndexError:
                row.append(0)
        return row

    def get_last_upward_diagonal(self):
        l_bound = - min(min(self._last_move), self.Z)
        u_bound = min(max(self.X - self._last_move.x,
                          self.Y - self._last_move.y), self.Z)

        diag = []
        for j in range(l_bound, u_bound + 1):
            try:
                diag.append(self.grid[self._last_move.x + j]
                            [self._last_move.y + j])
            except IndexError:
                diag.append(0)
        return diag

    def get_last_downward_diagonal(self):
        l_bound = - min(min(self._last_move.x, self.Y -
                            self._last_move.y), self.Z)
        u_bound = min(max(self.X - self._last_move.x,
                          self._last_move.y), self.Z)

        diag = []
        for j in range(l_bound, u_bound + 1):
            try:
                diag.append(self.grid[self._last_move.x + j]
                            [self._last_move.y - j])
            except IndexError:
                diag.append(0)
        return diag

    def append_move_to_grid(self, column):
        # convert user input to python index
        col_index = column - 1

        if col_index not in range(0, self.X):
            raise IllegalColumnError
        elif len(self.grid[col_index]) < self.Y:
            # append to column
            self.grid[col_index].append(self.current_player + 1)

            # set _last_move variable
            self._last_move = Point(col_index, len(self.grid[col_index]) - 1)
        else:
            raise IllegalRowError

    def next_player(self):
        self.current_player = (self.current_player + 1) % 2

    def is_game_won(self):
        return bool(self._won)

    def winner(self):
        return (self._won)

    def check_win(self, vec):
        if len(vec) >= self.Z:
            for sublist in get_sublists(vec, self.Z):
                if check_all_equal(sublist):
                    self._won = self.current_player + 1
                    break

    def check_if_winning_move(self):

        # check one column just appended
        last_column = self.get_last_column()
        self.check_win(last_column)

        # check only the row that has changed
        self.check_win(self.get_last_row())

        # check all diagonals
        self.check_win(self.get_last_upward_diagonal())
        self.check_win(self.get_last_downward_diagonal())

    def move(self, line):
        self.append_move_to_grid(line)

        self.check_if_winning_move()

        # switch to next player
        self.next_player()

    def check_complete_game(self):
        return sum([len(self.grid[j])
                    for j in range(self.X)]) == self.X * self.Y


def parse_move(line):
    return int(line.strip())


def main(filename):
    with open(filename) as fp:
        line = fp.readline()

        try:
            x, y, z = get_params(line)
        except InvalidFileError:
            return 8
        except IllegalGameError:
            return 7

        # initialize game
        game = CollectZ(x, y, z)

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

    # print(game.grid)
    # bp()

    if game.is_game_won():
        # one of players won
        return game.winner()
    elif game.check_complete_game():
        # 'Draw'
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
