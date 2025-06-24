import heapq

def a_star(graph_data, start, end):
    graph = {}
    for edge in graph_data["edges"]:
        graph.setdefault(edge["from"], []).append((edge["to"], edge["weight"]))

    def heuristic(n1, n2):
        return 0  # Dummy heuristic

    queue = [(heuristic(start, end), 0, start, [])]
    visited = set()

    while queue:
        (est_cost, cost, node, path) = heapq.heappop(queue)
        if node in visited:
            continue
        visited.add(node)
        path = path + [node]
        if node == end:
            return path, cost
        for neighbor, weight in graph.get(node, []):
            if neighbor not in visited:
                heapq.heappush(queue, (cost + weight + heuristic(neighbor, end), cost + weight, neighbor, path))
    return [], 0
