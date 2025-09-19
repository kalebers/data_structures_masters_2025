import heapq

def dijkstra(graph, start, end):
    distances = {node: float('infinity') for node in graph.nodes()}
    distances[start] = 0
    pq = [(0, start)]
    previous_nodes = {node: None for node in graph.nodes()}
    expanded_nodes = 0

    while pq:
        current_distance, current_node = heapq.heappop(pq)
        expanded_nodes += 1

        if current_distance > distances[current_node]:
            continue
        
        if current_node == end:
            break

        for neighbor, data in graph[current_node].items():
            weight = data['weight']
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))
    
    path = []
    current = end
    while current is not None:
        path.insert(0, current)
        current = previous_nodes[current]
    
    return path, distances[end], expanded_nodes