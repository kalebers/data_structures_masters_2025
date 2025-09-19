def dfs(graph, start, end):
    # Inicializa a pilha com o nó inicial e o caminho contendo apenas ele
    stack = [(start, [start])]
    expanded_nodes = 0  # Contador de nós expandidos (visitados)
    
    while stack:
        # Remove o nó do topo da pilha
        current_node, path = stack.pop()
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
        
        # Para cada vizinho do nó atual (em ordem reversa para DFS)
        for neighbor in sorted(graph.neighbors(current_node), reverse=True):
            if neighbor not in path:  # Evita ciclos
                new_path = path + [neighbor]
                stack.append((neighbor, new_path))  # Adiciona o vizinho à pilha
    
    # Se não encontrou caminho, retorna None, infinito e número de nós expandidos
    return None, float('inf'), expanded_nodes