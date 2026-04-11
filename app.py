"""
LogicLens — Flask app
Phases 1-4 unified: Graph explorer + What-If AI engine (streaming via SSE)
"""

from __future__ import annotations

import json
import os
import queue
import threading
import io
import sys
from contextlib import redirect_stdout

from flask import Flask, Response, jsonify, render_template, request, stream_with_context
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()
print(f"GROQ KEY LOADED: {'YES' if os.environ.get('GROQ_API_KEY') else 'NO'}")
print("Using Groq LLM for Agent Engine")
from extractor import analyze_project

app = Flask(__name__)

# ── Neo4j connection ───────────────────────────────────────────────────────────
URI      = os.environ.get("NEO4J_URI",      "neo4j://127.0.0.1:7687")
NEO4J_UN = os.environ.get("NEO4J_USERNAME", "neo4j")
NEO4J_PW = os.environ.get("NEO4J_PASSWORD", "password123")
AUTH     = (NEO4J_UN, NEO4J_PW)


# ══════════════════════════════════════════════════════════════════════════════
# Existing routes
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    data = request.get_json()
    if not data or "path" not in data:
        return jsonify({"error": "Missing 'path' in request body."}), 400

    directory_path = data["path"].strip().strip('"').strip("'")

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
        print("Neo4j Query Started")
        with GraphDatabase.driver(URI, auth=AUTH) as driver:
            with driver.session() as session:
                result = session.run("MATCH (n)-[r]->(m) RETURN n, r, m")
                for record in result:
                    n = record["n"]; m = record["m"]; r = record["r"]
                    n_id = str(n.element_id);  m_id = str(m.element_id)

                    if n_id not in nodes:
                        nodes[n_id] = {
                            "id":     n_id,
                            "label":  n.get("name", "Unknown"),
                            "file":   n.get("file", ""),
                            "line":   n.get("line", 0),
                            "author": n.get("author", ""),
                        }
                    if m_id not in nodes:
                        nodes[m_id] = {
                            "id":     m_id,
                            "label":  m.get("name", "Unknown"),
                            "file":   m.get("file", ""),
                            "line":   m.get("line", 0),
                            "author": m.get("author", ""),
                        }
                    edges.append({"from": n_id, "to": m_id, "label": r.type})

                result2 = session.run("MATCH (n) WHERE NOT (n)--() RETURN n")
                for record in result2:
                    n = record["n"];  n_id = str(n.element_id)
                    if n_id not in nodes:
                        nodes[n_id] = {
                            "id":     n_id,
                            "label":  n.get("name", "Unknown"),
                            "file":   n.get("file", ""),
                            "line":   n.get("line", 0),
                            "author": n.get("author", ""),
                        }
        print("Neo4j Query Completed")
        print(f"Graph payload: {len(nodes)} nodes, {len(edges)} edges")

    except Exception as e:
        print("Neo4j Query Failed", e)
        return jsonify({"error": str(e)}), 500

    return jsonify({"nodes": list(nodes.values()), "edges": edges})

@app.route("/api/check_env", methods=["GET"])
def api_check_env():
    has_key = bool(os.environ.get("GROQ_API_KEY"))
    return jsonify({"groq_api_key_present": has_key})


# ── List all function names (for the What-If dropdown) ────────────────────────
@app.route("/api/functions", methods=["GET"])
def api_functions():
    try:
        with GraphDatabase.driver(URI, auth=AUTH) as driver:
            with driver.session() as session:
                records = session.run("MATCH (f:Function) RETURN f.name AS name ORDER BY f.name")
                names = [r["name"] for r in records if r["name"]]
        return jsonify({"functions": names})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ══════════════════════════════════════════════════════════════════════════════
# What-If SSE endpoint  — streams every agent step as a JSON event
# ══════════════════════════════════════════════════════════════════════════════

def _sse(data: dict) -> str:
    """Format a dict as an SSE message."""
    return f"data: {json.dumps(data)}\n\n"


class _QueueStream(io.StringIO):
    """StringIO-like sink that forwards each write() to a queue as an SSE event."""
    def __init__(self, q: "queue.Queue[str | None]"):
        super().__init__()
        self._q = q

    def write(self, text: str) -> int:
        if text.strip():
            self._q.put(_sse({"type": "log", "text": text.rstrip()}))
        return len(text)

    def flush(self): pass


@app.route("/api/whatif")
def api_whatif():
    target = request.args.get("function", "").strip()
    if not target:
        return jsonify({"error": "Missing ?function= parameter"}), 400

    print(f"What-If request received for: {target}")
    from whatif_engine import run_whatif_engine

    print('What-If Response Created')
    return Response(
        run_whatif_engine(target),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'X-Accel-Buffering': 'no',
        },
    )


# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app.run(debug=True, port=5000, threaded=True)
