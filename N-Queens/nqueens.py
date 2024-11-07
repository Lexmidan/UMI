import numpy as np 

# N-queens problem
n = 8

# Define helper functions

def allDifferent_column(queens):
    #If the length of the list (N) is equal to number of unique elements in the list, then all elements are unique
    return len(queens) == len(np.unique(queens))

def allDifferent_diagonal(queens, n):
    # Quens are placed diagonally if the difference between their indexes is equal to the difference between their values
    for i in range(n):
        for j in range(i + 1, n):
            if abs(i - j) == abs(queens[i] - queens[j]):
                return False
    return True

# Another constraint is that there must be N queens on the board
def nQueens(queens, n):
    return len(queens) == n

# I can now define a function that checks if all the queens are placed correctly
def nqueens_satisfied(queens, n):
    return allDifferent_column(queens) and allDifferent_diagonal(queens, n) and nQueens(queens, n)


# For each row, the possible positions for the queens. Initially, all positions are possible.
# i corresponds to the row, and the list contains the possible positions for the queens in that row.
poss_positions = {i: list(range(n)) for i in range(n)}

# The positions of the queens. Initially, no queens are placed.
# positions[i] is the column of the queen in row i.
positions = []

# Keep track of removed positions in each step
# i-th list doesn't contain dict for i-th row, because in i-th step we don't remove any position from i-th row
# there's no track for the last step, because it's granted that the last queen has only one possible position
removal_log = {i: {j:[] for j in list(set(range(n))-{i})} for i in range(n-1)}

def remove_col_from_row(i, j, row, col):
    if col in row:
        row.remove(col)
        removal_log[i][j].append(col)

i = 0
while i < n:

    position = np.random.choice(poss_positions[i]) 
    positions.append(position)
    # Remove the selected position from the possible positions for the other rows.
    # Remove the position that are under diagonal attack from the selected position.
    if i == n - 1:
        break
    for j in range(n):
        if j == i:
            continue
        remove_col_from_row(i, j, poss_positions[j], position) # Same column
        remove_col_from_row(i, j, poss_positions[j], position + abs(i - j)) # Diagonal attack from the left
        remove_col_from_row(i, j, poss_positions[j], position - abs(i - j)) # Diagonal attack from the right
    i += 1

nqueens_satisfied(positions, n) 