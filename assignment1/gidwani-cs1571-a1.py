#things to edit in part 1:
	#make breadth and depth first naive implementations
	#record number of nodes in mem and assigned
	#figure out how to print string in the same format

import sys
import time
import csp
import search
import itertools
import re
from functools import reduce

def flatten(seqs):
    return sum(seqs, [])

easy1 = '.3..4..32.313.2.'
#harder1 = '4173698.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'

#edit/read this
_R3 = list(range(2))
_CELL = itertools.count().__next__
_BGRID = [[[[_CELL() for x in _R3] for y in _R3] for bx in _R3] for by in _R3]
_BOXES = flatten([list(map(flatten, brow)) for brow in _BGRID])
_ROWS = flatten([list(map(flatten, zip(*brow))) for brow in _BGRID])
_COLS = list(zip(*_ROWS))

#read this
_NEIGHBORS = {v: set() for v in flatten(_ROWS)}
for unit in map(set, _BOXES + _ROWS + _COLS):
    for v in unit:
        _NEIGHBORS[v].update(unit - {v})

def different_values_constraint(A, a, B, b):
	return a != b

class sudoku2(csp.CSP):
    """A Sudoku problem.
    The box grid is a 3x3 array of boxes, each a 3x3 array of cells.
    Each cell holds a digit in 1..9. In each box, all digits are
    different; the same for each row and column as a 9x9 grid.
    >>> e = Sudoku(easy1)
    >>> e.display(e.infer_assignment())
    . . 3 | . 2 . | 6 . .
    9 . . | 3 . 5 | . . 1
    . . 1 | 8 . 6 | 4 . .
    ------+-------+------
    . . 8 | 1 . 2 | 9 . .
    7 . . | . . . | . . 8
    . . 6 | 7 . 8 | 2 . .
    ------+-------+------
    . . 2 | 6 . 9 | 5 . .
    8 . . | 2 . 3 | . . 9
    . . 5 | . 1 . | 3 . .
    >>> AC3(e); e.display(e.infer_assignment())
    True
    4 8 3 | 9 2 1 | 6 5 7
    9 6 7 | 3 4 5 | 8 2 1
    2 5 1 | 8 7 6 | 4 9 3
    ------+-------+------
    5 4 8 | 1 3 2 | 9 7 6
    7 2 9 | 5 6 4 | 1 3 8
    1 3 6 | 7 9 8 | 2 4 5
    ------+-------+------
    3 7 2 | 6 8 9 | 5 1 4
    8 1 4 | 2 5 3 | 7 6 9
    6 9 5 | 4 1 7 | 3 8 2
    >>> h = Sudoku(harder1)
    >>> backtracking_search(h, select_unassigned_variable=mrv, inference=forward_checking) is not None
    True
    """  # noqa
    R3 = _R3
    Cell = _CELL
    bgrid = _BGRID
    boxes = _BOXES
    rows = _ROWS
    cols = _COLS
    neighbors = _NEIGHBORS

    def __init__(self, grid):
        """Build a Sudoku problem from a string representing the grid:
        the digits 1-9 denote a filled cell, '.' or '0' an empty one;
        other characters are ignored."""
        squares = iter(re.findall(r'\d|\.', grid))
        domains = {var: [ch] if ch in '1234' else '1234'
                   for var, ch in zip(flatten(self.rows), squares)}
        for _ in squares:
            raise ValueError("Not a Sudoku grid", grid)  # Too many squares
        csp.CSP.__init__(self, None, domains, self.neighbors, different_values_constraint)

    def display(self, assignment):
        def show_box(box): return [' '.join(map(show_cell, row)) for row in box]

        def show_cell(cell): return str(assignment.get(cell, '.'))

        def abut(lines1, lines2): return list(
            map(' | '.join, list(zip(lines1, lines2))))

        print('\n----+----\n'.join(
            '\n'.join(reduce(
                abut, map(show_box, brow))) for brow in self.bgrid))

    #def actions

def main():
	alg = sys.argv[1]
	fileName = sys.argv[2]
	slots1 = sys.argv[3]
	file = open("exampleSudokus-q1.txt", "r")
	all_lines = file.readlines()
	for line in all_lines:
		grid=line
		sudokuSolver(grid, alg)
	#scheduleCourses(fileName, slots1)
	findPath("Forbes,Bouquet", "Forbes,Bigelow", "Astar")

def sudokuSolver(grid, alg):
	board = sudoku2(grid)
	if alg == "bfs":
		bfs(board)
	elif alg == "dfs":
		dfs(board)
	elif alg=="backtracking":
		backtracking(board)
	elif alg == "backtracking-ordered":
		start_time = time.time()
		csp.backtracking_search(board, select_unassigned_variable=csp.mrv, order_domain_values=csp.lcv, inference=csp.forward_checking)
		end_time = time.time()
		elapsed_time = (end_time-start_time)
		solution = board.infer_assignment()
		#put into format of input
#		for index in range(len(solution)):     
#			print(solution[index])
		file_sudoku_print("BT-ordered", elapsed_time, solution)
	elif alg == "backtracking-noOrdering":
		#no value and variable ordering
		start_time = time.time()
		csp.backtracking_search(board, select_unassigned_variable=csp.first_unassigned_variable, order_domain_values=csp.unordered_domain_values, inference=csp.forward_checking)
		end_time = time.time()
		solution = board.infer_assignment()
		elapsed_time = print(end_time-start_time)
		file_sudoku_print("BT-noOrder", elapsed_time, solution)
	elif alg == "backtracking-reverse":
		start_time = time.time()
		csp.backtracking_search(board, select_unassigned_variable=csp.lcvar, order_domain_values=csp.mcv, inference=csp.forward_checking)
		solution = board.infer_assignment()
		end_time = time.time()
		elapsed_time = end_time-start_time
		file_sudoku_print("BT-reverse", elapsed_time, solution)

def bfs(problem):
	start_time = time.time()
	#print("next problem")
	search.breadth_first_tree_search(problem)
	#problem.display(problem.infer_assignment())
	csp.AC3(problem)
	#problem.display(problem.infer_assignment())
	solution = problem.infer_assignment()
	end_time = time.time()
	elapsed_time = end_time-start_time
	file_sudoku_print("BFS", elapsed_time, solution)

def dfs(problem):
	start_time = time.time()
	#print("next problem")
	search.depth_first_tree_search(problem)
	#problem.display(problem.infer_assignment())
	csp.AC3(problem)
	#problem.display(problem.infer_assignment())
	solution = problem.infer_assignment()
	end_time = time.time()
	elapsed_time = end_time - start_time
	file_sudoku_print("DFS", elapsed_time, solution)

def backtracking(problem):
	start_time = time.time()
	csp.backtracking_search(problem, select_unassigned_variable=csp.mrv, order_domain_values=csp.lcv, inference=csp.forward_checking)
	#problem.display(problem.infer_assignment())
	csp.AC3(problem)
	#problem.display(problem.infer_assignment())
	solution = problem.infer_assignment()
	end_time = time.time()
	elapsed_time = end_time - start_time
	file_sudoku_print("backtracking", elapsed_time, solution)

def file_sudoku_print(alg, time, solution):
	file = open("output.txt", "a")
	file.write(alg)
	file.write("\nSolution: " + str(solution))
	file.write("\nRunning time: " + str(time) + "\n")
	file.close()

#The same teacher can’t teach two different classes at the same time
#Two different sections of the same class shouldn’t be scheduled at the same time.
#Classes in the same area shouldn’t be scheduled at the same time.
#Note: don’t worry about the labs and recitations, just the main sections of the courses

#Run a backtracking search (using mrv, a degree heuristic, and lcv) with AC-3 
#inference on this problem to output to a file a viable schedule to this problem, 
#given the file and number of timeslots. Your file should consist of a series of 
#“course number-teacher-section” and timeslot pairs “CS1571-Walker-1, 0”, separated by semicolons.	
#This requires two modifications to the existing codebase:
#-	The implementation and use of a class that extends CSP and sets up the variables, 
#domains, and constraints for the course scheduling problem
#-	The implementation of the degree heuristic function, named “degree”
#We will be providing a sample input file for you to test your code on named partB-courseList-shortened.txt.

#set up variables domains and constraints of course scheduling problem
#courseNumber, courseName, sections, labs, recitations, (profess), (sections each prof teaches), (areas)
		
def class_constraints(A, a, B, b):
    """Constraint is satisfied (true) if A, B are really the same variable,
    or if they are not in the same row, down diagonal, or up diagonal."""
    return A == B or (a != b and A + a != B + b and A - a != B - b)

class courseSchedule(csp.CSP):
    def __init__(self, variables, domains, neighbors):
        self.variables = variables
        self.domains = domains
        csp.CSP.__init__(self, variables, domains, neighbors, class_constraints)

def scheduleCourses(file, slots):
	f = open(file, "r")
	variables = []
	domains = {}
	courseList = f.readlines()
	for line in range(len(courseList)):
		course = courseList[line].split(";")
		variables.append(course[1])
	for var in variables:
		domains[var] = list(range(1, int(slots)))
		neighbors = variables.remove(var)
		scheduler = courseSchedule(variables, domains, neighbors)
		csp.backtracking_search(scheduler, select_unassigned_variable=csp.mrv, order_domain_values=csp.unordered_domain_values, inference=csp.AC3)
		csp.backtracking_search(scheduler, select_unassigned_variable=csp.first_unassigned_variable, order_domain_values=csp.lcv, inference=csp.AC3)

graph = search.Graph()

class createGraph(search.Graph):
	#routeFile = open("partc-intersection.txt", "r")
	def __init__(self, graph_dict=None, directed=False):
		graph_dict = {}
		self.directed = directed
	distFile = open("partc-distances.txt", "r")
	distLines = distFile.readlines()
	for dist in distLines:
		full_line = dist.split(",");
		int1 = full_line[0] + "," + full_line[1]
		int2 = full_line[2] + "," + full_line[3]
		distance = full_line[4]
		graph.connect(int1, int2, distance)
	def h(self, state):
		return self.graph.least_costs[state]

def findPath(intersect1, intersect2, alg):
	#search.GraphProblem.__init__(intersect1, intersect2, graph)
	graphTree = createGraph()
	#print(graphTree.get(intersect1))
	#print(graphTree.nodes)
	#search.GraphProblem.__init__(intersect1, intersect2, graphTree)
	#if alg == "Astar":
		#search.astar_search(graph, h=intersect2)

#graph has no attribute h -- figure out how to call astar on it 

if __name__ == '__main__':
	main()






