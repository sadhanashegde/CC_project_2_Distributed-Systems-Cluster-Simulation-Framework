from flask import Flask, request, jsonify, render_template
from threading import Thread
import docker
import time
import uuid

# Initialize Flask app and Docker client
app = Flask(__name__, template_folder='templates')
docker_client = docker.from_env()

# In-memory cluster state
cluster = {
    "nodes": {},  # node_id -> {"cpu_cores": int, "available_cores": int, "pods": list}
    "pods": {},   # pod_id -> {"cpu_requirement": int, "node_id": str}
}

def health_monitor():
    """Periodically checks node health."""
    while True:
        for node_id in list(cluster["nodes"].keys()):
            try:
                container = docker_client.containers.get(node_id)
                if container.status != 'running':
                    raise Exception("Node not running")
            except Exception:
                # Handle node failure
                failed_node = cluster["nodes"].pop(node_id)
                print(f"Node {node_id} failed. Rescheduling pods...")
                for pod_id in failed_node["pods"]:
                    reschedule_pod(pod_id)
        time.sleep(10)

def reschedule_pod(pod_id):
    """Attempts to reschedule a pod to a healthy node."""
    pod = cluster["pods"].pop(pod_id, None)
    if not pod:
        return
    for node_id, node in cluster["nodes"].items():
        if node["available_cores"] >= pod["cpu_requirement"]:
            node["available_cores"] -= pod["cpu_requirement"]
            node["pods"].append(pod_id)
            cluster["pods"][pod_id] = {"cpu_requirement": pod["cpu_requirement"], "node_id": node_id}
            print(f"Pod {pod_id} rescheduled to Node {node_id}")
            return
    print(f"Failed to reschedule Pod {pod_id}. No available nodes.")

@app.route('/')
def home():
    return render_template('index.html', nodes=cluster["nodes"], pods=cluster["pods"])

@app.route('/add_node', methods=['POST'])
def add_node():
    cpu_cores = request.form.get('cpu_cores')
    if not cpu_cores:
        return jsonify({"error": "CPU cores not specified"}), 400

    node_id = str(uuid.uuid4())
    try:
        docker_client.containers.run("alpine", "sleep 3600", detach=True, name=node_id)
    except Exception as e:
        return jsonify({"error": f"Failed to launch container: {str(e)}"}), 500

    cluster["nodes"][node_id] = {"cpu_cores": int(cpu_cores), "available_cores": int(cpu_cores), "pods": []}
    return jsonify({"message": "Node added successfully", "node_id": node_id}), 200

@app.route('/list_nodes', methods=['GET'])
def list_nodes():
    return jsonify([{"node_id": node_id, **node} for node_id, node in cluster["nodes"].items()])

@app.route('/launch_pod', methods=['POST'])
def launch_pod():
    cpu_requirement = request.form.get('cpu_requirement')
    if not cpu_requirement:
        return jsonify({"error": "CPU requirement not specified"}), 400

    pod_id = str(uuid.uuid4())
    for node_id, node in cluster["nodes"].items():
        if node["available_cores"] >= int(cpu_requirement):
            node["available_cores"] -= int(cpu_requirement)
            node["pods"].append(pod_id)
            cluster["pods"][pod_id] = {"cpu_requirement": int(cpu_requirement), "node_id": node_id}
            return jsonify({"message": "Pod launched successfully", "pod_id": pod_id}), 200

    return jsonify({"error": "No available nodes"}), 400

@app.route('/list_pods', methods=['GET'])
def list_pods():
    return jsonify([{"pod_id": pod_id, **pod} for pod_id, pod in cluster["pods"].items()])

if __name__ == '__main__':
    Thread(target=health_monitor, daemon=True).start()
    app.run(debug=True)