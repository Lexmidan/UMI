import numpy as np
import copy


def allDifferent_column(queens):
    return len(queens) == len(np.unique(queens))

def consistent_diagonal(queens):
    # Quens are placed diagonally if the difference between their indexes is equal to the difference between their values
    for i in range(len(queens)):
        for j in range(i + 1, len(queens)):
            if abs(i - j) == abs(queens[i] - queens[j]):
                return False
    return True

def nqueens_satisfied(queens):
    return allDifferent_column(queens) and consistent_diagonal(queens)

# The problem is symmetric with respect to rotations and mirroring
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

def flip_diag(queens, n):
    return flip_hor(flip_ver(queens, n), n)


def nqueens_symmetries(queens, n):
    symmetries = []
    symmetries.append(queens)
    symmetries.append(rotate_90(queens, n))
    symmetries.append(rotate_180(queens, n))
    symmetries.append(rotate_270(queens, n))
    symmetries.append(flip_hor(queens, n))
    symmetries.append(flip_ver(queens, n))
    symmetries.append(flip_diag(queens, n))
    return symmetries


def remove_col_from_row(row, col):
    if col in row:
        row.remove(col)


def remove_cells_under_attack(domain, q, row):
    domain = copy.deepcopy(domain)
    for j in range(row, n):
        remove_col_from_row(domain[j], q)  # Same column
        remove_col_from_row(domain[j], q + (j - row))  # Diagonal attack to the right
        remove_col_from_row(domain[j], q - (j - row))  # Diagonal attack to the left
    return domain


def bt(domain=None):
    if domain is None:
        domain = {i: list(range(n)) for i in range(n)}
    
    row = len(queens)
    
    if row == n:
        solutions.append(queens.copy())
        return

    if not domain[row]:
        # No possible positions for the current queen, backtrack
        return

    for q in domain[row]:
        new_domain = remove_cells_under_attack(domain, q, row) # forward checking
        queens.append(q)
        bt(new_domain)
        queens.pop()  # Backtrack


if __name__ == "__main__":
    n = 9
    queens = []
    solutions = []

    bt()
    print(f"Found {len(solutions)} solutions for the {n}-Queens problem.")
    for solution in solutions:
        print(f'{solution} - {nqueens_satisfied(solution)}')  
