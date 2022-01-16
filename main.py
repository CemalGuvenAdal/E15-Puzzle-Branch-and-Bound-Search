"""
@authors: GÜVEN ADAL
          BATUHAN BUDAK
          CANKAT ANDAY KADİM
          FURKAN AHİ
	  Umutcan Baştepe
"""
from queue import PriorityQueue
import random
import PySimpleGUI as sg
from collections import namedtuple
import matplotlib.pyplot as plt

SIDE_LENGTH = 4
VISITED = []
PATH = []
MOVES = []
STEPS = []


class Node:
    def __init__(self, puzzle, level, cost, parent, old_loc, new_loc):
        self.puzzle = puzzle
        self.level = level
        self.cost = cost
        self.parent = parent
        self.old_loc = old_loc
        self.new_loc = new_loc

    def __lt__(self, other):
        return self.level + self.cost < other.level + other.cost

    # Draw state and its moves
    def draw_puzzle(self, window, stepNo, moves):
        # Arranging Locations for steps with respect to step number
        if (stepNo < 8):
            rectangle_x = stepNo * 230
            rectangle_y = 25
        elif (stepNo >= 8 and stepNo < 16):
            rectangle_x = 1610 - abs(stepNo - 8) * 230
            rectangle_y = 200
        elif (stepNo >= 16 and stepNo < 24):
            rectangle_x = (stepNo - 16) * 230
            rectangle_y = 375
        elif (stepNo >= 24 and stepNo < 32):
            rectangle_x = 1610 - abs(stepNo - 24) * 230
            rectangle_y = 550
        elif (stepNo >= 32 and stepNo < 40):
            rectangle_x = (stepNo - 32) * 230
            rectangle_y = 725
        else:  # If step no > 40 cannot display so locations are assigned as 1
            rectangle_x = 1
            rectangle_y = 1
        graph = window.Element("graph")
        for i in range(4):
            for j in range(4):
                # Arrange colors to display better
                if (self.puzzle[j * SIDE_LENGTH + i] == 1):
                    fill_color = "orange"
                elif (self.puzzle[j * SIDE_LENGTH + i] == 2):
                    fill_color = "lightgreen"
                elif (self.puzzle[j * SIDE_LENGTH + i] == 3):
                    fill_color = "cyan"
                elif (self.puzzle[j * SIDE_LENGTH + i] == 4):
                    fill_color = "yellow"
                elif (self.puzzle[j * SIDE_LENGTH + i] == 5):
                    fill_color = "purple"
                else:
                    fill_color = "white"
                # Draw squares
                graph.draw_rectangle((rectangle_x + i * 30, rectangle_y + j * 30),
                                     (rectangle_x + (i + 1) * 30, rectangle_y + (j + 1) * 30),
                                     fill_color,
                                     line_color="black")
                if (self.puzzle[j * SIDE_LENGTH + i] != 0):  # If square is not blank the draw number
                    graph.draw_text(int(self.puzzle[j * SIDE_LENGTH + i]),
                                    (rectangle_x + 15 + i * 30, rectangle_y + 15 + j * 30))
                if (stepNo < 7):
                    graph.DrawImage(filename="arrowRight.png", location=(rectangle_x + 160, rectangle_y + 48))
                    graph.draw_text(moves[stepNo], location=(rectangle_x + 180, rectangle_y + 30))
                    if (stepNo == 0):  # If state is initial write "Initial State" under it
                        graph.draw_text("Initial State", location=(rectangle_x + 60, rectangle_y + 130))
                elif (stepNo == 7 or stepNo == 15 or stepNo == 23 or stepNo == 31):
                    graph.DrawImage(filename="arrowDown.png", location=(rectangle_x + 48, rectangle_y + 130))
                    graph.draw_text(moves[stepNo], location=(rectangle_x + 85, rectangle_y + 145))
                elif (stepNo > 7 and stepNo < 16):
                    graph.DrawImage(filename="arrowLeft.png", location=(rectangle_x - 70, rectangle_y + 46))
                    graph.draw_text(moves[stepNo], location=(rectangle_x - 50, rectangle_y + 30))
                elif (stepNo > 15 and stepNo < 24):
                    graph.DrawImage(filename="arrowRight.png", location=(rectangle_x + 160, rectangle_y + 48))
                    graph.draw_text(moves[stepNo], location=(rectangle_x + 180, rectangle_y + 30))
                elif (stepNo > 23 and stepNo < 32):
                    graph.DrawImage(filename="arrowLeft.png", location=(rectangle_x - 70, rectangle_y + 46))
                    graph.draw_text(moves[stepNo], location=(rectangle_x - 50, rectangle_y + 30))
                elif (stepNo > 31 and stepNo < 40):
                    graph.DrawImage(filename="arrowRight.png", location=(rectangle_x + 160, rectangle_y + 48))
                    graph.draw_text(moves[stepNo], location=(rectangle_x + 180, rectangle_y + 30))
        return graph


# our scramble method sometimes does wonders
# and sometimes gives the puzzle in a solved state
def scramble(puzzle_goal, rand):
    puzzle = puzzle_goal.copy()
    last = 1
    empty = 15
    for i in range(rand):
        # this decides if we should go up(0), right(1), down(2) or left(3)
        second_rand = random.randint(0, 3)
        # this part makes sure we don't do up down or left right all the time
        # haven't come up with an efficient way to stop left up right down and such however
        if last != second_rand and abs(last - second_rand) != 2:
            if second_rand == 0:
                if empty >= SIDE_LENGTH:
                    puzzle[empty] = puzzle[empty - SIDE_LENGTH]
                    puzzle[empty - SIDE_LENGTH] = 0
                    empty -= SIDE_LENGTH
                    last = second_rand
            elif second_rand == 1:
                if empty % SIDE_LENGTH < SIDE_LENGTH - 1:
                    puzzle[empty] = puzzle[empty + 1]
                    puzzle[empty + 1] = 0
                    empty += 1
                    last = second_rand
            elif second_rand == 2:
                if empty < (SIDE_LENGTH - 1) * SIDE_LENGTH:
                    puzzle[empty] = puzzle[empty + SIDE_LENGTH]
                    puzzle[empty + SIDE_LENGTH] = 0
                    empty += SIDE_LENGTH
                    last = second_rand
            elif second_rand == 3:
                if empty % SIDE_LENGTH > 0:
                    puzzle[empty] = puzzle[empty - 1]
                    puzzle[empty - 1] = 0
                    empty -= 1
                    last = second_rand
            else:
                i -= 1
            # this is to stop the scrambler from sending a puzzle in a solved state
            # still doesn't work sometimes
            if puzzle == puzzle_goal:
                i = 0
            # print_puzzle(puzzle)
    return puzzle, empty


def create_15puzzle():
    puzzle = []
    for i in range(SIDE_LENGTH):
        for j in range(SIDE_LENGTH):
            if i * SIDE_LENGTH + j != 15:
                puzzle.append((i % SIDE_LENGTH + j) + 1 if (i % SIDE_LENGTH + j) + 1 < 5 else 5)
            else:
                puzzle.append(0)
    return puzzle


def print_puzzle(puzzle):
    for i in range(SIDE_LENGTH):
        for j in range(SIDE_LENGTH):
            print(" %-2s" % puzzle[i * SIDE_LENGTH + j], end="\t")
        print()
    print()


# looks at every node at the puzzle and checks if its different than the one in goal state
def calculate_cost(puzzle, puzzle_goal):
    cost = 0
    for i in range(SIDE_LENGTH):
        for j in range(SIDE_LENGTH):
            if puzzle[i * SIDE_LENGTH + j] != 0 and puzzle[i * SIDE_LENGTH + j] != puzzle_goal[i * SIDE_LENGTH + j]:
                cost += 1
    return cost


def window_init(title="Pentakill HW3"):
    # Initialize layout
    layout = [
        [
            sg.Graph(
                canvas_size=(1850, 950),
                graph_bottom_left=(0, 950),
                graph_top_right=(1850, 0),
                key="graph"
            )
        ]
    ]
    window = sg.Window(title, layout)
    window.Finalize()
    return window


def print_path(child):
    # until we reach the root node keep going
    if child is None:
        return
    # this is going on recursively as otherwise we would print the path from end to start
    print_path(child.parent)
    PATH.append(child)
    old_loc = child.old_loc
    new_loc = child.new_loc
    old_str = str(child.puzzle[old_loc])
    if old_str != "0":
        if new_loc - old_loc == -SIDE_LENGTH:
            MOVES.append(old_str + " down")
        elif new_loc - old_loc == 1:
            MOVES.append(old_str + " left")
        elif new_loc - old_loc == SIDE_LENGTH:
            MOVES.append(old_str + " up")
        else:
            MOVES.append(old_str + " right")
    print_puzzle(child.puzzle)


# swaps the locations inside the puzzle
def swap(puzzle_original, old_loc, new_loc):
    puzzle = puzzle_original.copy()
    temp = puzzle[old_loc]
    puzzle[old_loc] = puzzle[new_loc]
    puzzle[new_loc] = temp
    return puzzle


# this part creates each possible childres
def handleChildren(puzzle_goal, node, i):
    empty = node.new_loc
    # checks if the parent can create a child in the right, left, up or down
    if i == 0:
        if empty >= SIDE_LENGTH:
            empty -= SIDE_LENGTH
    elif i == 1:
        if empty % SIDE_LENGTH < SIDE_LENGTH - 1:
            empty += 1
    elif i == 2:
        if empty < (SIDE_LENGTH - 1) * SIDE_LENGTH:
            empty += SIDE_LENGTH
    elif i == 3:
        if empty % SIDE_LENGTH > 0:
            empty -= 1
    if empty == node.new_loc:
        return None
    # creates the puzzle from the parents puzzle but changes the empty part accordingly to each child
    child_puzzle = swap(node.puzzle, node.new_loc, empty)
    # calculates the cost for each child
    child_cost = calculate_cost(child_puzzle, puzzle_goal)
    child = Node(child_puzzle, node.level + 1, child_cost, node, node.new_loc, empty)
    # here we check for duplication in each child.
    if checkDup(child):
        return None
    # print("Child Puzzle")
    # print_puzzle(child_puzzle)
    return child


# stores each visited node in an array and with it the cost
def checkDup(node):
    for i in range(len(VISITED)):
        # if the node is visited before amd the cost is lower
        # than the child the child will no longer go down that path
        if (VISITED[i].puzzle == node.puzzle) and (VISITED[i].cost <= node.cost):
            return True
        # I couldn't think of a point where this would apply but its better to be prepared for that
        elif VISITED[i].puzzle == node.puzzle:
            VISITED[i] = node
            return False
        # If we haven't visited that before add it to the list
    VISITED.append(node)
    return False


# this part meshes all the previous parts to solve the E-15 puzzle
def solve(puzzle_goal, queue):
    if queue.empty():
        return
    node = queue.get()
    if node.cost == 0:
        print("Printing Path")
        print("Done in " + str(node.level) + " steps.")
        STEPS.append(node.level)
        print_path(node)
        MOVES.append("GOAL")
        return node.level
    # the only loop is used for the child creation and handling
    # couldn't come up with a better way
    for i in range(SIDE_LENGTH):
        child = handleChildren(puzzle_goal, node, i)
        if child is not None:
            queue.put(child)
    solve(puzzle_goal, queue)


def main():
    for i in range(25):
        puzzle_goal = create_15puzzle()
        rand = random.randint(25, 30)
        puzzle, empty = scramble(puzzle_goal, rand)
        print("INITIAL STATE " + str(i))
        print_puzzle(puzzle)
        root = Node(puzzle, 0, calculate_cost(puzzle, puzzle_goal), None, empty, empty)
        queue = PriorityQueue()
        queue.put(root)
        solve(puzzle_goal, queue)
        if i == 5 or i == 16:
            window = window_init()
            for j in range(len(PATH)):
                PATH[j].draw_puzzle(window, j, MOVES)
            window.read()
        PATH.clear()
        MOVES.clear()
        VISITED.clear()
        puzzle.clear()
    number = sum(STEPS) / len(STEPS)
    print('Finished with an average of: {0:.4}'.format(number))

    left = []
    tick_label = []
    for i in range(25):
        left.append(i)
        tick_label.append("s" + str(i))
    # heights of bars
    height = STEPS

    # labels for bars

    # plotting a bar chart
    plt.bar(left, height, tick_label=tick_label,
            width=0.8, color=['red', 'green'])
    plt.xticks(rotation=90)

    # naming the x-axis
    plt.xlabel('x - axis')
    # naming the y-axis
    plt.ylabel('y - axis')
    plt.axline((0, number), (len(STEPS), number), linewidth=4, color='purple', label="Average")
    plt.legend()
    # plot title
    plt.title('STEP COUNT vs. INITIAL STEPS')

    # function to show the plot
    plt.show()


if __name__ == '__main__':
    main()
