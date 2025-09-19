import heapq

def dijkstra(graph, start, end):
    # Inicializa as distâncias de todos os nós como infinito
    distances = {node: float('infinity') for node in graph.nodes()}
    distances[start] = 0  # Distância do nó inicial para ele mesmo é zero

    # Fila de prioridade para escolher o próximo nó com menor distância
    pq = [(0, start)]

    # Armazena o nó anterior para reconstruir o caminho
    previous_nodes = {node: None for node in graph.nodes()}

    # Contador de nós expandidos (visitados)
    expanded_nodes = 0

    while pq: # o que é pq: é uma fila de prioridade que armazena os nós a serem explorados, ordenados pela distância acumulada
        # Remove o nó com menor distância da fila de prioridade
        current_distance, current_node = heapq.heappop(pq)
        expanded_nodes += 1  # Incrementa o contador de nós expandidos

        # Se já encontramos uma distância menor anteriormente, ignora
        if current_distance > distances[current_node]:
            continue
        
        # Se chegou ao nó final, encerra o loop
        if current_node == end:
            break

        # Para cada vizinho do nó atual
        for neighbor, data in graph[current_node].items():
            weight = data['weight']  # Peso da aresta
            distance = current_distance + weight  # Calcula nova distância

            # Se a nova distância é menor, atualiza
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))  # Adiciona na fila

    # Reconstrói o caminho do nó final até o inicial
    path = []
    current = end
    while current is not None:
        path.insert(0, current)
        current = previous_nodes[current]
    
    # Retorna o caminho, a distância total e o número de nós expandidos
    return path, distances[end], expanded_nodes