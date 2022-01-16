# E15-Puzzle-Branch-and-Bound-Search
The implemented program uses the PySimpleGUI, matplotlib, and three .png files. .png 
files are needed for the GUI of the program. To run the program, these libraries should be 
imported, and .png files should be installed.
def create_15puzzle() function creates a 4x4 puzzle that puts in the E15-Puzzle specified in the 
instructions.
def scramble(puzzle_goal, rand) function takes the unaltered puzzle from create_15puzzle() 
then moves to empty spaces around the create a solvable E15-Puzzle.
def print_puzzle(puzzle) prints the given 4x4 puzzle.
def calculate_cost(puzzle, puzzle_goal) This function calculates the number of different entries 
from the goal.
def print_path(child) Since we store each parent in the respective child, we can recursively print 
each child and recreate the path we followed.
def swap(puzzle_original, old_loc, new_loc) Since we store each puzzle in the respective child, 
we do the swapping in this function.
def handleChildren(puzzle_goal, node, i) checking the nodes by comparing their costs and 
defining current children. As well as creating each possible child, we could arrive from the 
parent.
def checkDup(node) is the dynamic programming part of our branch and bound algorithm. We 
store each visited node in the array concerning its cost. If the current child has been visited 
before and the cost is lower in the visited node, we don't continue going down a path in that 
child
