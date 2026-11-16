import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "group11_test_maps"))
map_path = os.path.join(os.path.dirname(__file__), "..", "group11_test_maps", "map02_small.txt")

from loader import load_map
grid, start, goal = load_map(map_path)

from collections import deque
import heapq


# --- BFS Algorithm ----
def bfs(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    if start == goal:
        return [start], 1

    visited = {start}
    queue = deque([start])
    parent = {start: None}
    nodes_expanded = 0

    while queue:
        r, c = queue.popleft()
        nodes_expanded += 1

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            neighbor = (nr, nc)
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0 and neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = (r, c)

                if neighbor == goal:
                    path = []
                    while neighbor is not None:
                        path.append(neighbor)
                        neighbor = parent[neighbor]
                    return path[::-1], nodes_expanded

                queue.append(neighbor)

    return None, nodes_expanded

path, nodes_expanded = bfs(grid, start, goal)
print("BFS path length:", len(path) if path else None, "nodes expanded:", nodes_expanded)



# --- DFS Algorithm ----

def dfs(grid, start, goal):
    rows, cols = len(grid), len(grid[0])

    visited = set()
    stack = [(start, None)]
    parent = {}
    nodes_explained = 0

    while stack:
        node, par = stack.pop()
        if node in visited:
            continue

        visited.add(node)
        parent[node] = par
        nodes_explained += 1

        if node == goal:
            path = []
            while node is not None:
                path.append(node)
                node = parent[node]
            return path[::-1], nodes_explained

        r, c = node
        for dr, dc in [(-1, 0), (1, 0), ( 0, -1), (0, 1)]:
            nr, nc = r + dr, c + dr
            neighbor = (nr, nc)
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0 and neighbor not in visited:
                stack.append((neighbor, node))

    return None,  nodes_expanded

path, nodes_expanded = dfs(grid, start, goal)
print("DFS path length:", len(path) if path else None, "nodes expanded:", nodes_expanded)



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

path, nodes_expanded = a_star(grid, start, goal)
print("A_start path length:", len(path) if path else None, "nodes expanded:", nodes_expanded)

