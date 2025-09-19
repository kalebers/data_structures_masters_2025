from collections import deque

def bfs(graph, start, end):
    queue = deque([(start, [start])])
    expanded_nodes = 0

    while queue:
        current_node, path = queue.popleft()
        expanded_nodes += 1

        if current_node == end:
            total_cost = 0
            for i in range(len(path) - 1):
                u, v = path[i], path[i+1]
                if graph.has_edge(u, v):
                    total_cost += graph[u][v]['weight']
            return path, total_cost, expanded_nodes

        for neighbor in sorted(graph.neighbors(current_node)):
            if neighbor not in path:
                new_path = path + [neighbor]
                queue.append((neighbor, new_path))

    return None, float('inf'), expanded_nodes