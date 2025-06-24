from flask import Flask, render_template, request, jsonify
from algorithms.dijkstra import dijkstra
from algorithms.astar import a_star
from algorithms.bellman_ford import bellman_ford
from linked_list import LinkedList

app = Flask(__name__)

graph = {
    "nodes": set(),
    "edges": []
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_edge', methods=['POST'])
def add_edge():
    data = request.json
    from_node = data['from']
    to_node = data['to']
    weight = float(data['weight'])

    graph["nodes"].add(from_node)
    graph["nodes"].add(to_node)

    graph["edges"].append({
        "from": from_node,
        "to": to_node,
        "weight": weight
    })

    return jsonify({"message": "Edge added successfully."})

@app.route('/delete_edge', methods=['POST'])
def delete_edge():
    data = request.json
    from_node = data['from']
    to_node = data['to']

    graph["edges"] = [
        edge for edge in graph["edges"]
        if not (edge["from"] == from_node and edge["to"] == to_node)
    ]

    return jsonify({"message": "Edge deleted successfully."})

@app.route('/shortest_path', methods=['POST'])
def shortest_path():
    data = request.json
    source = data.get("source")
    destination = data.get("destination")
    algo = data.get("algo")

    if not source or not destination:
        return jsonify({"error": "Source and destination are required."}), 400

    all_weights = [edge["weight"] for edge in graph["edges"]]
    has_negative = any(w < 0 for w in all_weights)

    if has_negative and algo in ["dijkstra", "a-star"]:
        return jsonify({
            "error": f"{algo.upper()} cannot handle negative weights. Please switch to Bellman-Ford."
        }), 400

    graph_data = {
        "nodes": list(graph["nodes"]),
        "edges": graph["edges"]
    }

    try:
        if algo == "dijkstra":
            path, total = dijkstra(graph_data, source, destination)
        elif algo == "bellman-ford":
            path, total = bellman_ford(graph_data, source, destination)
        elif algo == "a-star":
            path, total = a_star(graph_data, source, destination)
        else:
            return jsonify({"error": "Invalid algorithm"}), 400

        if not path:
            return jsonify({"error": "No path found."}), 404

        ll = LinkedList()
        for node in path:
            ll.append(node)

        return jsonify({
            "path": path,
            "total_weight": total,
            "linked_list": ll.to_list()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
