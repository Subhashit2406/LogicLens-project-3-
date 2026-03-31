from flask import Flask, request, jsonify, render_template
from neo4j import GraphDatabase
from extractor import analyze_project

app = Flask(__name__)

# Neo4j connection details (shared with extractor.py)
URI = "neo4j://127.0.0.1:7687"
AUTH = ("neo4j", "password123")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    data = request.get_json()
    if not data or "path" not in data:
        return jsonify({"error": "Missing 'path' in request body."}), 400

    directory_path = data["path"].strip()

    try:
        result = analyze_project(directory_path)
        return jsonify({"status": "success", **result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/graph", methods=["GET"])
def api_graph():
    nodes = {}
    edges = []

    try:
        with GraphDatabase.driver(URI, auth=AUTH) as driver:
            with driver.session() as session:
                # Fetch all relationships (covers all connected nodes)
                result = session.run("MATCH (n)-[r]->(m) RETURN n, r, m")
                for record in result:
                    n = record["n"]
                    m = record["m"]
                    r = record["r"]

                    n_id = n.element_id
                    m_id = m.element_id

                    if n_id not in nodes:
                        nodes[n_id] = {
                            "id":    n_id,
                            "label": n.get("name", "Unknown"),
                            "file":  n.get("file", ""),
                            "line":  n.get("line", 0),
                            "author": n.get("author", ""),
                        }
                    if m_id not in nodes:
                        nodes[m_id] = {
                            "id":    m_id,
                            "label": m.get("name", "Unknown"),
                            "file":  m.get("file", ""),
                            "line":  m.get("line", 0),
                            "author": m.get("author", ""),
                        }

                    edges.append({
                        "from":  n_id,
                        "to":    m_id,
                        "label": r.type,
                    })

                # Also fetch isolated nodes (no relationships)
                result2 = session.run(
                    "MATCH (n) WHERE NOT (n)--() RETURN n"
                )
                for record in result2:
                    n = record["n"]
                    n_id = n.element_id
                    if n_id not in nodes:
                        nodes[n_id] = {
                            "id":    n_id,
                            "label": n.get("name", "Unknown"),
                            "file":  n.get("file", ""),
                            "line":  n.get("line", 0),
                            "author": n.get("author", ""),
                        }

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "nodes": list(nodes.values()),
        "edges": edges,
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
