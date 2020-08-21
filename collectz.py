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
    try:
        params = list(map(int, line.split()))
    except ValueError:
        raise InvalidFileError
        
    if len(params) != 3:
        raise InvalidFileError

    if not valid_game_params(*params):
        raise IllegalGameError

    return params


class CollectZ:

    def __init__(self, x, y, z):
        # game params

        self.X = x
        self.Y = y
        self.Z = z
    
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
    
    def check_win(vec):
        pass
    
    def check_if_winning_move(self):
        
        # check one column just appended
        # TODO hardcoded 0
        last_column = self.get_column(0)
        self.check_win(last_column)
        
        # check all rows
        for y in range(self.Y):
            self.check_win(self.get_row(y))
        
        # check all diagonals      

    def move(self, line):
        self.append_move_to_grid(line)

        self.check_if_winning_move()
        
        # switch to next player
        self.next_player()


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

    print(game.grid)
    # bp()

    if game.is_game_won():
        # one of players won
        return game.winner()
    else:
        # 'Draw'
        return 0


if __name__ == "__main__":
    # TODO error if more than one file has been provided
    
    result = main(sys.argv[1])
    print(result)
