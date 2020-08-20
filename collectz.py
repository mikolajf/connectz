import sys
from math import min


def get_params(line):
    params = line.split()

    if len(params) != 3:
        raise ValueError
    
    return params


def main():
    filename = sys.argv[1]
    
    with open(filename) as fp:
        line = fp.readline()
        
        # check first line format
        # parse params
        try:
            x, y, z = get_params(line)
        except ValueError:
            return 'wrong first line'
        
        if z > min(x, y):
            return 'wrong game'
        
        while line:
            print(line)
            line = fp.readline()


if __name__ == "__main__":
    result = main()
    print(result)
