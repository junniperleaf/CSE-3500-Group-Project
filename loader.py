"""
Shared map loader for Group 11's A* comparison project.

Every algorithm should take the SAME inputs so the benchmark is fair:
    path, nodes_expanded = your_algorithm(grid, start, goal)

where:
    grid  = list of rows, each a list of ints: 0 = open, 1 = wall
    start = (row, col)
    goal  = (row, col)

Movement is 4-directional (up/down/left/right). Use the Manhattan
heuristic for A* on these maps. If the group switches to 8-directional
(diagonals allowed), use Euclidean or Chebyshev instead.
"""

def load_map(path):
    """Load a .txt map in char format. Returns (grid, start, goal)."""
    start = goal = None
    grid = []
    with open(path) as f:
        for r, line in enumerate(f.read().splitlines()):
            row = []
            for c, ch in enumerate(line):
                if ch == '#':
                    row.append(1)
                else:
                    row.append(0)          # '.', 'S', 'G' are all walkable
                    if ch == 'S':
                        start = (r, c)
                    elif ch == 'G':
                        goal = (r, c)
            grid.append(row)
    return grid, start, goal


if __name__ == "__main__":
    import sys
    g, s, go = load_map(sys.argv[1] if len(sys.argv) > 1 else "map01_tiny.txt")
    print(f"{len(g)}x{len(g[0])}  start={s}  goal={go}")
