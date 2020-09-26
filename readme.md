# README

## Key considerations of designing the game checker:
- It has been mentioned in task specification that some files may be very large. With that in mind, it is necessary to parse the file line by line instead of reading entire file at once. If illegal game dimensions are provided or an illegal move is made, we can early terminate the execution.
- The game tracker has been implemented as an array of empty columns (also arrays). On each move, relevant column is appended with player 1 or 2 'counter'. Again, from optimization perspective, appending to an empty array was superior to creating arrays with predefined height.
- Once a move has proved legal, i.e. conforms to format and does not overfill column or row, we check if last move has won the game. Here it is enough to check only one column that has just been appended to, one row where the 'counter' has landed and two diagonals that have been affected by the 'counter'. As we are looking for the winning sequence of length Z, it is enough to check only elements in Z-proximity of last move.
