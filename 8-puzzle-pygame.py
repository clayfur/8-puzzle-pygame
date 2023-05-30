import pygame
import heapq
import time

# Define the size of the window
WINDOW_SIZE = (900, 900)

# Define the colors and font
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
pygame.init()
FONT = pygame.font.SysFont(None, 120)

# Define the delay between each step (in seconds)
DELAY = 0.5

# Define the puzzle board
class Puzzle:
    def __init__(self, state):
        self.state = state

    def __str__(self):
        return str(self.state)

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(str(self))

    def is_goal(self):
        return self.state == [[1, 2, 3], [4, 5, 6], [7, 8, None]]

    def actions(self):
        # Find the position of the empty cell
        row, col = self.find(None)
        actions = []
        # Check available actions based on the empty cell's position
        if row > 0:
            actions.append('up')
        if row < 2:
            actions.append('down')
        if col > 0:
            actions.append('left')
        if col < 2:
            actions.append('right')
        return actions

    def result(self, action):
        # Find the position of the empty cell
        row, col = self.find(None)
        # Calculate the new position based on the action
        if action == 'up':
            new_row = row - 1
            new_col = col
        elif action == 'down':
            new_row = row + 1
            new_col = col
        elif action == 'left':
            new_row = row
            new_col = col - 1
        elif action == 'right':
            new_row = row
            new_col = col + 1
        else:
            raise ValueError("Invalid action")
        # Create a new state by swapping the empty cell with the adjacent cell
        new_state = [row[:] for row in self.state]
        new_state[row][col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[row][col]
        return Puzzle(new_state)

    def find(self, value):
        # Find the position of a given value in the puzzle board
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == value:
                    return i, j

    def manhattan(self):
        # Calculate the sum of Manhattan distances for each tile
        distance = 0
        for i in range(3):
            for j in range(3):
                value = self.state[i][j]
                if value is not None:
                    # Calculate the expected position (goal position) for each tile
                    row_goal, col_goal = (value - 1) // 3, (value - 1) % 3
                    # Calculate the Manhattan distance for the tile and add it to the total distance
                    distance += abs(row_goal - i) + abs(col_goal - j)
        return distance

# Define the node class for the search tree
class Node:
    def __init__(self, puzzle, parent=None, action=None, g=0, h=0):
        self.puzzle = puzzle
        self.parent = parent
        self.action = action
        self.g = g
        self.h = h

    def f(self):
        # Calculate the total cost of the node (g + h)
        return self.g + self.h

    def __lt__(self, other):
        # Compare nodes based on their total cost (f value)
        return self.f() < other.f()

# Define the solver class
class Solver:
    def __init__(self, puzzle):
        self.puzzle = puzzle

    def solve(self):
        # Create the initial node with the puzzle state and heuristic value
        start_node = Node(self.puzzle, g=0, h=self.puzzle.manhattan())
        heap = [start_node]  # Use a priority queue (heap) to store nodes
        visited = set()  # Keep track of visited puzzle states to avoid duplicates
        while heap:
            node = heapq.heappop(heap)  # Pop the node with the lowest total cost
            if node.puzzle.is_goal():  # Check if the puzzle state is the goal state
                # If it is, reconstruct and return the solution path
                path = []
                while node.parent is not None:
                    path.append(node)
                    node = node.parent
                path.append(node)
                path.reverse()
                return path
            visited.add(str(node.puzzle))
            for action in node.puzzle.actions():
                child = node.puzzle.result(action)
                if str(child) not in visited:
                    # Create a child node and add it to the priority queue
                    child_node = Node(child, parent=node, action=action, g=node.g + 1, h=child.manhattan())
                    heapq.heappush(heap, child_node)
        return []

# Define the main function
def main():
    # Initialize pygame and create the window
    pygame.init()
    window = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("8 Puzzle")

    # Define the initial state of the puzzle
    initial_state = [[8, 5, 6], [2, 4, 1], [3, 7, None]]

    # Create the puzzle and solver instances
    puzzle = Puzzle(initial_state)
    solver = Solver(puzzle)

    # Solve the puzzle and visualize the solution path
    solution = solver.solve()
    if not solution:
        print("No solution found")
        return
    for node in solution:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Draw the board at the current state
        window.fill(WHITE)
        for i in range(3):
            for j in range(3):
                rect = pygame.Rect(j * 300, i * 300, 300, 300)
                pygame.draw.rect(window, GRAY, rect, 2)
                if node.puzzle.state[i][j] is not None:
                    text = FONT.render(str(node.puzzle.state[i][j]), True, BLACK)
                    text_rect = text.get_rect(center=rect.center)
                    window.blit(text, text_rect)
        pygame.display.flip()

        # Wait for the delay
        time.sleep(DELAY)

    # Wait for the user to close the window
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

# Call the main function
if __name__ == '__main__':
    main()
