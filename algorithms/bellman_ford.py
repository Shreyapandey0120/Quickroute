def bellman_ford(graph_data, start, end):
    distance = {node: float('inf') for node in graph_data["nodes"]}
    predecessor = {node: None for node in graph_data["nodes"]}
    distance[start] = 0

    for _ in range(len(graph_data["nodes"]) - 1):
        for edge in graph_data["edges"]:
            u, v, w = edge["from"], edge["to"], edge["weight"]
            if distance[u] + w < distance[v]:
                distance[v] = distance[u] + w
                predecessor[v] = u

    for edge in graph_data["edges"]:
        u, v, w = edge["from"], edge["to"], edge["weight"]
        if distance[u] + w < distance[v]:
            raise ValueError("Graph contains a negative weight cycle")

    path = []
    current = end
    while current is not None:
        path.insert(0, current)
        current = predecessor[current]

    if distance[end] == float('inf'):
        return [], 0
    return path, distance[end]
