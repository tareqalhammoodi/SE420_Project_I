from copy import deepcopy
from queue import PriorityQueue
from termcolor import colored

# HELPERS METHODS ----------------------------------------------------------------------------------------------
# Function that visualizes the board.
def print_board(board):
    print("-------------")
    for row in board:
        row_visual = "|"
        for tile in row:
            if tile == 0:  # Blank tile
                row_visual += f" {colored(' ', 'cyan')} |"
            else:
                row_visual += f" {colored(str(tile), 'yellow')} |"
        print(row_visual)
        print("-------------")

# Function that prints the queue.
def print_queue(queue):
    print(colored("Current Queue:", "green"))
    for item in queue:
        print(f"f_score: {item.priority}, g_score: {item.cost}, state: {item.state}, move: {item.move}")
        # f: Total cost (f = g + h).
        # g: Cost from the start node to this node.
        # h: Heuristic estimate of the cost to the goal.
    print()

# Function that validate the given input from the user.
def validate_input(input):
    try:
        numbers = list(map(int, input.split()))
    except ValueError:
        raise ValueError("Invalid input: Please enter only numbers.")
    if len(numbers) != 9:
        raise ValueError("Invalid input: You must enter exactly 9 numbers.")
    if sorted(numbers) != [0, 0, 0, 0, 0, 0, 1, 2, 3]:
        raise ValueError("Invalid input: The input must include exactly one 1, one 2, one 3, and six 0s.")
    return [numbers[:3], numbers[3:6], numbers[6:]]

# ----------------------------------------------------------------------------------------------------------------

class Node:
    # The puzzle board configuration.
    def __init__(self, state, parent=None, move=None, depth=0, cost=0, parent_cost=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.depth = depth
        self.cost = cost  
        self.parent_cost = parent_cost 
        self.priority = 0

    def __lt__(self, other):
        return self.priority < other.priority

#req2: The tiles can be moved up, down, right, or left.
directions = {
    "U": (-1, 0),  # Move up
    "D": (1, 0),   # Move down
    "L": (0, -1),  # Move left
    "R": (0, 1)    # Move right
}

def move_tile(state, tile, direction):
    tile_pos = [(i, j) for i in range(3) for j in range(3) if state[i][j] == tile][0]
    dx, dy = directions[direction]
    x, y = tile_pos[0] + dx, tile_pos[1] + dy
    if 0 <= x < 3 and 0 <= y < 3 and state[x][y] == 0:  # Only move into blank space
        new_state = deepcopy(state)
        new_state[tile_pos[0]][tile_pos[1]], new_state[x][y] = new_state[x][y], new_state[tile_pos[0]][tile_pos[1]]
        return new_state
    return None

#req4: Distance(cost) between two neighboring states will be measured based on the move costs as given below
# right or left move  >  cost = 2
# up of down move     >  cost = 1
direction_costs = {
    "L": 2,
    "R": 2,
    "U": 1,
    "D": 1
}

def expand_node(node, goal, tile_to_move):
    expanded_nodes = []
    for direction_key, (dx, dy) in directions.items():
        new_state = move_tile(node.state, tile_to_move, direction_key)
        if new_state:
            move_cost = direction_costs.get(direction_key)
            new_node = Node(
                state=new_state,
                parent=node,
                move=f"Tile {tile_to_move} {direction_key}",
                depth=node.depth + 1,
                cost=node.cost + move_cost,
                parent_cost=node.cost
            )
            h = manhattan_distance(new_state, goal)
            new_node.priority = new_node.cost + h
            expanded_nodes.append((new_node, h))
    return expanded_nodes

#req5: The A* search will be implemented with Manhattan distance as heuristics.
def manhattan_distance(state, goal):
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] in [1, 2, 3]:
                tile = state[i][j]
                goal_pos = [(x, y) for x in range(3) for y in range(3) if goal[x][y] == tile][0]
                distance += abs(goal_pos[0] - i) + abs(goal_pos[1] - j)
    return distance

def a_star_search(initial_state, goal_state):
    current_state = deepcopy(initial_state)
    frontier = PriorityQueue()
    queue_snapshot = []
    root = Node(state=current_state, cost=0)
    root.priority = manhattan_distance(root.state, goal_state)
    frontier.put(root)
    queue_snapshot.append(root)
    explored = set()
    #req3: The game will begin by the move of Tile #1 (if required) and go on with the moves of other tiles in order.
    tiles_order = [1, 2, 3]
    expansion_count = 0
    expansion_limit = 10

    while not frontier.empty() and expansion_count < expansion_limit:
        node = frontier.get()
        queue_snapshot.remove(node)
        explored.add(tuple(map(tuple, node.state)))

        #req6: The expansion will go on till 10th expanded node. The program will print out each expanded state and compare it with given goal state.
        expansion_count += 1
        print(colored(f"EXPANDED NODE {expansion_count}", "red"))
        print_board(node.state)
        # if goal stated was reached print "Goal reached" message and return.
        if node.state == goal_state:
            print(colored("Goal reached! 🥳🥳🥳", "blue"))
            print(f"Total Cost: {node.cost}")
            return

        tile_to_move = tiles_order[(expansion_count - 1) % 3]
        children = expand_node(node, goal_state, tile_to_move)

        print(colored("Possible Next Moves:", "green"))
        for child, child_h in children:
            queue_snapshot.append(child)
            if tuple(map(tuple, child.state)) not in explored:
                frontier.put(child)
            print(f"  Move: {child.move}, f: {child.priority}, g: {child.cost}, h: {child_h}")
        print()

        print_queue(queue_snapshot)
    # if goal wasn't reached during the given expansion limit the program will quit the loop.
    print("Search ended. Goal state not reached within expanded node limit.")

if __name__ == "__main__":

    # Hard-coded initial and goal states for testing.
    '''
    initial_state = [[1, 0, 2],
                     [0, 3, 0],
                     [0, 0, 0]]

    goal_state = [[0, 0, 0],
                  [0, 1, 2],
                  [0, 0, 3]]
    '''
    # sample initial state 1 0 2 0 3 0 0 0 0
    # sample goal state    0 0 0 0 1 2 0 0 3

    #req1: The initial and goal states will be given by user
    while True:
        try:
            print("Enter the initial state as 9 numbers (e.g., 1 0 2 0 3 0 0 0 0):")
            initial_state = validate_input(input().strip())
            break
        except ValueError as e:
            print(e)
    while True:
        try:
            print("Enter the goal state as 9 numbers (e.g., 0 0 0 0 1 2 0 0 3):")
            goal_state = validate_input(input().strip())
            break
        except ValueError as e:
            print(e)

    a_star_search(initial_state, goal_state)