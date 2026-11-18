from collections import deque



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



# --- DFS Algorithm ----

def dfs(grid, start, goal):
    rows, cols = len(grid), len(grid[0])

    visited = set()
    stack = [(start, None)]
    parent = {}
    nodes_expanded = 0

    while stack:
        node, par = stack.pop()
        if node in visited:
            continue

        visited.add(node)
        parent[node] = par
        nodes_expanded += 1

        if node == goal:
            path = []
            while node is not None:
                path.append(node)
                node = parent[node]
            return path[::-1], nodes_expanded

        r, c = node
        for dr, dc in [(-1, 0), (1, 0), ( 0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            neighbor = (nr, nc)
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0 and neighbor not in visited:
                stack.append((neighbor, node))

    return None,  nodes_expanded



