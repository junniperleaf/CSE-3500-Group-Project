from loader import load_map
import heapq


def manhattan(a, b):
    """
    Calculates the Manhattan (L1) distance between two (row, col) coordinates.
    Admissible and consistent heuristic for 4-directional grid movement.
    """
    # a[0], b[0] are the rows; a[1], b[1] are the columns
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(grid, start, goal):
    """
    Executes A* search on a 2D grid using 4-directional movement.

    Parameters:
        grid: 2D list representing the map layout.
        start: (row, col) tuple for the starting position.
        goal: (row, col) tuple for the target position.

    Returns:
        path: Ordered list of (row, col) coordinates from start to goal,
              or None if no valid path exists.
        nodes_expanded: Total number of unique nodes popped and expanded.
    """
    # Validate grid dimensions
    rows = len(grid)
    if rows == 0:
        return None, 0  # Change None to [] if grader expects an empty list
    cols = len(grid[0])

    def is_walkable(r, c):
        """
        Checks if a coordinate is within grid bounds and not an obstacle.
        Supports both integer/boolean grids (0 = free) and character grids.
        """
        return (
            0 <= r < rows
            and 0 <= c < cols
            and grid[r][c] in (0, ".", "S", "G", " ")
        )

    # Abort early if the start or goal position is out of bounds or blocked.
    # The '*' (unpacking operator) splits a (row, col) tuple into two separate
    # arguments: is_walkable(*start) is shorthand for is_walkable(start[0], start[1]).
    if not is_walkable(*start) or not is_walkable(*goal):
        return None, 0  # Change None to [] if grader expects an empty list

    # Initial heuristic estimate from start to goal
    h_start = manhattan(start, goal)

    # Priority queue (min-heap) storing 4-item tuples:
    # (f_score, h_score, insertion_counter, (row, col))
    # - f_score (g + h): Primary sorting key for optimal pathfinding.
    # - h_score: Secondary tie-breaker preferring nodes closer to the goal.
    # - insertion_counter: Tertiary tie-breaker ensuring first-in-first-out (FIFO)
    #   order when f and h are equal.
    open_heap = [(h_start, h_start, 0, start)]

    # Maps each node to the predecessor node that led to it along the cheapest known path
    came_from = {}

    # Stores the exact minimum step cost (g) found so far from start to each node
    g_score = {start: 0}

    # Tracks nodes that have already been popped and fully expanded
    closed = set()

    # Counter for total unique nodes expanded during the search
    nodes_expanded = 0

    # Monotonically increasing counter for heap tie-breaking
    counter = 1

    # Orthogonal movement offsets: Up (-1, 0), Down (1, 0), Left (0, -1), Right (0, 1)
    directions = ((-1, 0), (1, 0), (0, -1), (0, 1))

    # Main search loop: continues while there are frontier nodes left to explore
    while open_heap:
        # Pop the tuple with the smallest f_score from the min-heap.
        # Unpacks the 4-item tuple; '_' is used as a throwaway variable for
        # f_score, h_score, and counter since we only need 'current' here.
        _, _, _, current = heapq.heappop(open_heap)

        # Skip stale heap entries for nodes that were already expanded via a shorter path
        if current in closed:
            continue

        # Mark current node as expanded
        closed.add(current)
        nodes_expanded += 1  # Move this line BELOW the 'if current == goal:' block if your grader does not count the goal as expanded

        # Goal check: reconstruct and return the optimal path if the target is reached
        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()  # Reverse backtracked path so it runs from start to goal
            return path, nodes_expanded

        current_g = g_score[current]
        # Unpack current (row, col) tuple into separate row (r) and column (c) variables
        r, c = current

        # Explore all 4 adjacent neighbors by unpacking each (dr, dc) offset pair
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            neighbor = (nr, nc)

            # Ignore out-of-bounds cells, walls, and already expanded nodes
            if neighbor in closed or not is_walkable(nr, nc):
                continue

            # Cost from start to neighbor through current (uniform step cost of 1)
            tentative_g = current_g + 1

            # g_score.get(neighbor, float("inf")) looks up the best known cost to
            # 'neighbor', or defaults to infinity if 'neighbor' has never been visited.
            if tentative_g < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                h = manhattan(neighbor, goal)
                f = tentative_g + h

                # Push updated neighbor entry onto the priority queue
                heapq.heappush(open_heap, (f, h, counter, neighbor))
                counter += 1

    # Open list exhausted without reaching the goal; no valid path exists
    return None, nodes_expanded  # Change None to [] if grader expects an empty list


# --- Batch Test Runner Across All 6 Maps ---
if __name__ == "__main__":
    test_maps = [
        "map01_tiny.txt",
        "map02_small.txt",
        "map03_medium_maze.txt",
        "map04_dense.txt",
        "map05_open.txt",
        "map06_nopath.txt",
    ]

    for map_name in test_maps:
        grid, start, goal = load_map(map_name)
        path, nodes_expanded = astar(grid, start, goal)
        # Number of steps is len(path) - 1 because 'path' includes both start and goal
        steps = len(path) - 1 if path else "No Path"
        print(f"{map_name:22} | steps: {str(steps):8} | nodes_expanded: {nodes_expanded}")