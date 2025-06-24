let map = L.map('map').setView([28.6139, 77.2090], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

const nodes = {};
const edges = [];

map.on('click', function (e) {
    const latlng = e.latlng;
    const nodeId = prompt("Enter node ID:");
    if (nodeId && !nodes[nodeId]) {
        nodes[nodeId] = latlng;
        L.marker(latlng).addTo(map).bindPopup(`Node: ${nodeId}`).openPopup();
        addNodeToList(nodeId);
    }
});

function addNodeToList(nodeId) {
    const li = document.createElement("li");
    li.textContent = nodeId;
    document.getElementById("node-list").appendChild(li);
}

function addEdge() {
    const from = document.getElementById("fromNode").value;
    const to = document.getElementById("toNode").value;
    const weight = parseFloat(document.getElementById("weight").value);

    if (!from || !to || isNaN(weight)) {
        alert("Please fill all fields.");
        return;
    }

    if (!nodes[from] || !nodes[to]) {
        alert("Both nodes must exist on the map.");
        return;
    }

    fetch('/add_edge', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ from, to, weight })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) return alert(data.error);
        drawEdge(from, to, weight);
        appendEdgeToList(from, to, weight);
    });
}

function drawEdge(from, to, weight) {
    const latlngs = [nodes[from], nodes[to]];
    const line = L.polyline(latlngs, { color: 'blue' }).addTo(map);
    line.bindPopup(`${from} → ${to} (W: ${weight})`);
    line._from = from;
    line._to = to;
    edges.push(line);
}

function appendEdgeToList(from, to, weight) {
    const li = document.createElement("li");
    li.textContent = `${from} → ${to} (Weight: ${weight})`;

    const btn = document.createElement("button");
    btn.textContent = "❌";
    btn.style.marginLeft = "10px";
    btn.onclick = function () {
        fetch('/delete_edge', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ from, to })
        }).then(() => {
            li.remove();
            const line = edges.find(e => e._from === from && e._to === to);
            if (line) map.removeLayer(line);
        });
    };

    li.appendChild(btn);
    document.getElementById("edge-list").appendChild(li);
}

function findPath() {
    const source = document.getElementById("sourceNode").value;
    const destination = document.getElementById("destNode").value;
    const algo = document.getElementById("algorithm").value;

    fetch('/shortest_path', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ source, destination, algo })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) return alert(data.error);

        // Clear previous lines
        edges.forEach(e => map.removeLayer(e));
        edges.length = 0;

        // Draw path
        for (let i = 0; i < data.path.length - 1; i++) {
            drawEdge(data.path[i], data.path[i + 1], "?");
        }

        document.getElementById("pathResult").textContent =
            `Shortest Path: ${data.path.join(" → ")} | Total Weight: ${data.total_weight}`;

        const linkedList = document.getElementById("linkedListDisplay");
        linkedList.textContent = `Linked List Path: ${data.linked_list.join(" -> ")}`;
    });
}
