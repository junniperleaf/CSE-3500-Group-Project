import os, sys
import heapq
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "group11_test_maps"))

from loader import load_map
from bfs_dfs import bfs, dfs

MAPS_DIR = os.path.join(os.path(__file__), "..", "group11_test_maps")


# --- A_star Algorithm ----

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(grid, start, goal):
    rows, cols = len(grid), len(grid[0])

    h_start = manhattan(start, goal)
    open_heap = [(h_start, h_start, 0, start)]   # (f, h, g, node)
    g_score = {start: 0}
    parent = {start: None}
    closed = set()
    nodes_expanded = 0

    while open_heap:
        f, h, g, node = heapq.heappop(open_heap)

        if node in closed:
            continue
        closed.add(node)
        nodes_expanded += 1

        if node == goal:
            path = []
            while node is not None:
                path.append(node)
                node = parent[node]
            return path[::-1], nodes_expanded

        r, c = node
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            neighbor = (nr, nc)
            if not (0 <= nr < rows and 0 <= nc < cols) or grid[nr][nc] == 1:
                continue

            new_g = g + 1
            if neighbor not in g_score or new_g < g_score[neighbor]:
                g_score[neighbor] = new_g
                parent[neighbor] = node
                new_h = manhattan(neighbor, goal)
                heapq.heappush(open_heap, (new_g + new_h, new_h, new_g, neighbor))

    return None, nodes_expanded

if __name__ == "__main__":
    MAP_NAME = "map01_tiny.txt"
    grid, start, goal = load_map(os.path.join(MAPS_DIR, MAP_NAME))

    for algo_name, algo in [("BFS", bfs), ("DFS", dfs), ("A*", a_star)]:
        path, nodes_expanded = algo(grid, start, goal)
        print(algo_name, "path length:", len(path) if path else None, "nodes expanded:", nodes_expanded)
