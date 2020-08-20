import sys

def main():
    filename = sys.argv[1]
    
    with open(filename) as fp:
        line = fp.readline()
        while line:
            print(line)
            line = fp.readline()

if __name__ == "__main__":
    main()