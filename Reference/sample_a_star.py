import heapq

class Node:
    def __init__(self, position, parent=None):
        self.position = position  # (x, y) coordinates
        self.parent = parent      # Reference to the previous node to trace the path
        
        self.g = 0  # Cost from start node to current node
        self.h = 0  # Heuristic cost (estimated distance from current to goal)
        self.f = 0  # Total cost: f = g + h

    # Required for heapq to compare nodes by their 'f' cost
    def __lt__(self, other):
        return self.f < other.f

def heuristic(a, b):
    # Using Manhattan distance heuristic (good for grid-based movement with 4 directions)
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(grid, start, goal):
    # Initialize start and goal nodes
    start_node = Node(start, None)
    goal_node = Node(goal, None)

    # Initialize open and closed sets
    open_set = []
    closed_set = set()

    # Add the start node to the open set
    heapq.heappush(open_set, start_node)

    # Loop until the open set is empty
    while open_set:
        # Get the node with the lowest f cost
        current_node = heapq.heappop(open_set)
        closed_set.add(current_node.position)

        # Found the goal! Reconstruct and return the path
        if current_node.position == goal_node.position:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path (start to goal)

        # Generate neighbors (Up, Down, Left, Right)
        neighbors = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for new_position in neighbors:
            node_position = (current_node.position[0] + new_position[0], 
                             current_node.position[1] + new_position[1])

            # Make sure within grid bounds
            if (node_position[0] < 0 or node_position[0] >= len(grid) or 
                node_position[1] < 0 or node_position[1] >= len(grid[0])):
                continue

            # Make sure walkable terrain (assume 0 is free, 1 is obstacle)
            if grid[node_position[0]][node_position[1]] != 0:
                continue

            # If node is already evaluated, skip it
            if node_position in closed_set:
                continue

            # Create neighbor node
            neighbor = Node(node_position, current_node)

            # Calculate g, h, and f costs
            neighbor.g = current_node.g + 1
            neighbor.h = heuristic(neighbor.position, goal_node.position)
            neighbor.f = neighbor.g + neighbor.h

            # If a node with the same position is already in the open set with a lower g cost, skip
            if any(open_node.position == neighbor.position and open_node.g <= neighbor.g for open_node in open_set):
                continue

            # Add neighbor to the open set
            heapq.heappush(open_set, neighbor)

    return None # Return None if no path found

# --- Example Usage ---
if __name__ == "__main__":
    # 0 = Free path, 1 = Obstacle/Wall
    grid_map = [
        [0, 0, 0, 0, 1, 0],
        [0, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0]
    ]

    start_pos = (0, 0)
    goal_pos = (4, 5)

    path = a_star(grid_map, start_pos, goal_pos)
    print("Found Path:", path)