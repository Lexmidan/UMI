import unittest
from AC3 import CSPSolver
import queue
from nqueens import nqueens_satisfied

# Assuming the CSPSolver class is already defined as you provided

def n_queens_with_ac3(n):
    solutions = []
    queens = []

    # Initialize CSP components
    variables = list(range(n))
    arcs = []
    constraints = {}

    # Build arcs and constraints
    for i in variables:
        for j in variables:
            if i != j:
                arcs.append((i, j))
                # Define the constraint function for (i, j)
                def constraint(x, y, i=i, j=j):
                    return x != y and abs(x - y) != abs(i - j)
                constraints[(i, j)] = constraint

    def bt(domain=None):
        if domain is None:
            domain = {i: list(range(n)) for i in variables}
        
        row = len(queens)
        
        if row == n:
            solutions.append(queens.copy())
            return

        if not domain[row]:
            # No possible positions for the current queen, backtrack
            return

        # Apply AC-3 to the current domains
        csp_solver = CSPSolver(arcs, domain.copy(), constraints)
        ac3_result = csp_solver.solve()
        
        if not ac3_result:
            # AC-3 detected inconsistency, backtrack
            return
        
        domain = ac3_result  # Use the reduced domains after AC-3

        if not domain[row]:
            # No possible positions for the current queen, backtrack
            return

        # Try each possible value for the current row
        for q in domain[row]:
            # Assign the queen to column q in row
            new_domain = {k: v.copy() for k, v in domain.items()}
            new_domain[row] = [q]  # Assign the value

            queens.append(q)
            bt(new_domain)
            queens.pop()  # Backtrack

    # Start the backtracking process
    bt()

    return solutions

if __name__ == "__main__":
    n = 8
    solutions = n_queens_with_ac3(n)
    print(f"Found {len(solutions)} solutions for the {n}-Queens problem.")
    for solution in solutions:
        print(f'{solution} - {nqueens_satisfied(solution)}')
