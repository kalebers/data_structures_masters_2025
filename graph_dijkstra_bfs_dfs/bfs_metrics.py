from collections import deque

def bfs(graph, start, end):
    # Inicializa a fila com o nó inicial e o caminho contendo apenas ele
    queue = deque([(start, [start])])
    expanded_nodes = 0  # Contador de nós expandidos (visitados)
    visited = set([start])  # Conjunto de nós já visitados para evitar ciclos

    while queue:
        # Remove o nó da frente da fila
        current_node, path = queue.popleft()
        expanded_nodes += 1  # Incrementa o contador de nós expandidos

        # Se chegou ao nó final, calcula o custo total do caminho
        if current_node == end:
            total_cost = 0
            for i in range(len(path) - 1):
                u, v = path[i], path[i+1]
                if graph.has_edge(u, v):
                    total_cost += graph[u][v]['weight']
            # Retorna o caminho, o custo total e o número de nós expandidos
            return path, total_cost, expanded_nodes

        # Para cada vizinho do nó atual
        for neighbor in graph.neighbors(current_node):
            if neighbor not in visited:  # Evita visitar o mesmo nó novamente
                visited.add(neighbor)
                new_path = path + [neighbor]
                queue.append((neighbor, new_path))  # Adiciona o vizinho à fila

    # Se não encontrou caminho, retorna None, infinito e número de nós expandidos
    return None, float('inf'), expanded_nodes