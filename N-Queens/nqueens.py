import numpy as np

queens = []
n = 8


def remove_col_from_row(row, col):
    if col in row:
        row.remove(col)

def remove_cells_under_attack(queens, domain, q):
    for j in range(len(queens) + 1, n):
        remove_col_from_row(domain[j], q)  # Same column
        remove_col_from_row(domain[j], q + (j - len(queens)))  # Diagonal attack from the left
        remove_col_from_row(domain[j], q - (j - len(queens)))  # Diagonal attack from the right
    return domain


def remove_failed_q(domain, failed_q, step):
    if failed_q is None:
        return domain
    dom = domain.copy()
    dom[step].remove(failed_q)
    return dom


def bt(domain=None, failed_q=None):
    
    if domain is None:
        domain = {i: list(range(n)) for i in range(n)}
    
    q = np.random.choice(domain[len(queens)])

    domain = remove_cells_under_attack(queens, domain, q)
    
    queens.append(q)

    if len(queens) == n:
        return None
    
    while len(domain[len(queens)]) != 0:
        failed_q = bt(remove_failed_q(domain, failed_q, len(queens)), failed_q)
        if failed_q is not None:
            domain[len(queens)].remove(failed_q)
        else:
            return None
        
    return queens.pop() # failed_q

bt()
