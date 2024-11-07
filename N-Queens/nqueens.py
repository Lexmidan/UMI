import numpy as np

# N-queens problem
n = 8

# Define helper functions

def allDifferent_column(queens):
    #If the length of the list (N) is equal to number of unique elements in the list, then all elements are unique
    return len(queens) == len(np.unique(queens))

def allDifferent_diagonal(queens):
    # Quens are placed diagonally if the difference between their indexes is equal to the difference between their values
    for i in range(len(queens)):
        for j in range(i + 1, len(queens)):
            if abs(i - j) == abs(queens[i] - queens[j]):
                return False
    return True

# Another constraint is that there must be N queens on the board
def nQueens(queens, n):
    return len(queens) == n

# I can now define a function that checks if all the queens are placed correctly
def nqueens_satisfied(queens):
    return allDifferent_column(queens) and allDifferent_diagonal(queens)

# For each row, the possible positions for the queens. Initially, all positions are possible.
# i corresponds to the row, and the list contains the possible positions for the queens in that row.
poss_positions = {i: list(range(n)) for i in range(n)}

# The positions of the queens. Initially, no queens are placed.
# positions[i] is the column of the queen in row i.
positions = []

failed_sequences = {}

# Keep track of removed positions in each step
# i-th list doesn't contain dict for i-th row, because in i-th step we don't remove any position from i-th row
# there's no track for the last step, because it's granted that the last queen has only one possible position
removal_log = {i: {j: [] for j in list(set(range(n)) - {i})} for i in range(n - 1)}

def remove_col_from_row(i, j, row, col):
    if col in row:
        row.remove(col)
        removal_log[i][j].append(col)

def backtrack(f):  # f is the step number, that failed
    positions.pop()  # Remove the last queen from the board.
    for j in removal_log[f - 1]:
        poss_positions[j] += removal_log[f - 1][j]
        removal_log[f - 1][j] = []

# Main loop to solve the N-Queens problem
i = 0
while i < n:
    # Check if there are no possible positions for the queen in row i. Then backtrack
    if len(poss_positions[i]) == 0:
        
        if i in failed_sequences:
            failed_sequences[i].append(positions.copy())
        else:
            failed_sequences[i] = [positions.copy()]

        backtrack(i)
        i -= 1
        continue

    # Choose a position randomly from the available positions in the current row
    position = np.random.choice(poss_positions[i])
    positions.append(position)
    poss_positions[i].remove(position)

    # Remove the selected position from the possible positions for the other rows.
    # Remove the positions that are under diagonal attack from the selected position.
    for j in range(i + 1, n):
        remove_col_from_row(i, j, poss_positions[j], position)  # Same column
        remove_col_from_row(i, j, poss_positions[j], position + (j - i))  # Diagonal attack from the left
        remove_col_from_row(i, j, poss_positions[j], position - (j - i))  # Diagonal attack from the right

    # Move to the next row
    i += 1

# Print the solution
print(positions, 'satisfies the constraints:', nqueens_satisfied(positions, n))
