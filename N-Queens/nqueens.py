import numpy as np
import copy

queens = []
n = 8

def allDifferent_column(queens):
    #If the length of the list (N) is equal to number of unique elements in the list, then all elements are unique
    return len(queens) == len(np.unique(queens))

def consistent_diagonal(queens):
    # Quens are placed diagonally if the difference between their indexes is equal to the difference between their values
    for i in range(len(queens)):
        for j in range(i + 1, len(queens)):
            if abs(i - j) == abs(queens[i] - queens[j]):
                return False
    return True


# I can now define a function that checks if all the queens are placed correctly
def nqueens_satisfied(queens):
    return allDifferent_column(queens) and consistent_diagonal(queens)


def rotate_90(queens, n): #clockwise
    return [n - 1 - queens.index(i) for i in range(n)]

def rotate_180(queens, n):
    return [n - 1 - i for i in queens]

def rotate_270(queens, n):
    return (rotate_90(rotate_180(queens, n), n))

def flip_hor(queens, n):
    return [n - i for i in queens]

def flip_ver(queens, n):
    return [i for i in reversed(queens)]


def remove_col_from_row(row, col):
    if col in row:
        row.remove(col)

def remove_cells_under_attack(domain, q):
    # Create a deep copy to avoid modifying the original domain
    domain = copy.deepcopy(domain)
    for j in range(len(queens), n):
        remove_col_from_row(domain[j], q)  # Same column
        remove_col_from_row(domain[j], q + (j - len(queens)))  # Diagonal attack to the right
        remove_col_from_row(domain[j], q - (j - len(queens)))  # Diagonal attack to the left
    return domain

def bt(domain=None, failed_q=None):

    if domain is None:
        domain = {i: list(range(n)) for i in range(n)}
    
    if not domain[len(queens)]:
        # No possible positions for the current queen, backtrack
        return queens.pop() if queens else None

    q = np.random.choice(domain[len(queens)])
    
    domain = remove_cells_under_attack(domain, q)
    queens.append(q)

    if len(queens) == n:
        print("Solution:", queens)
        return None
    
    while domain.get(len(queens), []):
        failed_q = bt(domain, None)
        if failed_q is not None:
            domain[len(queens)].remove(failed_q)
        else:
            return None

    return queens.pop()  # Backtrack

bt()

nqueens_satisfied(queens)