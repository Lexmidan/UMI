"""
https://github.com/noahbass/ac-3/blob/master/AC3.py

Copyright (c) 2018 Noah Bass

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""
import queue

class CSPSolver:
    worklist = queue.Queue()  # a queue of arcs (this can be a queue or set in ac-3)

    # arcs: list of tuples
    # domains: dict of { tuples: list }
    # constraints: dict of { tuples: list }
    def __init__(self, arcs: list, domains: dict, constraints: dict):
        self.arcs = arcs
        self.domains = domains
        self.constraints = constraints

    # returns an empty dict if an inconsistency is found and domains for variables otherwise
    # generate: bool (choose whether or not to use a generator)
    def solve(self, generate=False) -> dict:
        result = self.solve_helper()

        if generate:
            return result
        else:
            return_value = []

            for step in result:
                if step == None:
                    return step  # inconsistency found
                else:
                    return_value = step

            return return_value[1]  # return only the final domain

    # returns a generator for each step in the algorithm, including the end result
    # each yield is a tuple containing: (edge, new domains, edges to consider)
    def solve_helper(self) -> dict:
        # setup queue with given arcs
        [self.worklist.put(arc) for arc in self.arcs]

        # continue working while worklist is not empty
        while not self.worklist.empty():
            (xi, xj) = self.worklist.get()

            if self.revise(xi, xj):
                if len(self.domains[xi]) == 0:
                    # found an inconsistency
                    yield None
                    break

                # get all of xj's neighbors
                neighbors = [neighbor for neighbor in self.arcs if neighbor[0] == xj]
                
                # put all neighbors into the worklist to be evaluated
                [self.worklist.put(neighbor) for neighbor in neighbors]

                yield ((xi, xj), self.domains, neighbors)
            else:
                yield ((xi, xj), self.domains, None)

        # yield the final return value
        yield (None, self.domains, None)

    # returns true if and only if the given domain i
    def revise(self, xi: object, xj: object) -> bool:
        revised = False

        # get the domains for xi and xj
        xi_domain = self.domains[xi]
        xj_domain = self.domains[xj]

        # get a list of constraints for (xi, xj)
        constraints = [constraint for constraint in self.constraints if constraint[0] == xi and constraint[1] == xj]

        for x in xi_domain[:]:
            satisfies = False  # there is a value in xjDomain that satisfies the constraint(s) between xi and xj

            for y in xj_domain:
                for constraint in constraints:
                    check_function = self.constraints[constraint]

                    # check y against x for each constraint
                    if check_function(x, y):
                        satisfies = True

            if not satisfies:
                # delete x from xiDomain
                xi_domain.remove(x)
                revised = True

        return revised