import docker
import threading
import time
import uuid

class Node:
    def __init__(self, node_id, cpu_cores):
        self.node_id = node_id
        self.cpu_cores = cpu_cores
        self.available_cores = cpu_cores
        self.pods = []

    def add_pod(self, pod_id, cpu_requirement):
        if self.available_cores >= cpu_requirement:
            self.pods.append(pod_id)
            self.available_cores -= cpu_requirement
            return True
        return False

class ClusterManager:
    def __init__(self):
        self.nodes = {}
        self.pods = {}
        self.docker_client = docker.from_env()
        self.health_check_interval = 10

    def add_node(self, cpu_cores):
        node_id = str(uuid.uuid4())
        self.nodes[node_id] = Node(node_id, cpu_cores)
        # Launch a container for the node
        self.docker_client.containers.run("alpine", "sleep 3600", detach=True, name=node_id)
        return node_id

    def list_nodes(self):
        return [{"node_id": node.node_id, "cpu_cores": node.cpu_cores,
                 "available_cores": node.available_cores, "pods": node.pods} for node in self.nodes.values()]

    def launch_pod(self, cpu_requirement):
        pod_id = str(uuid.uuid4())
        for node in self.nodes.values():
            if node.add_pod(pod_id, cpu_requirement):
                self.pods[pod_id] = node.node_id
                return pod_id
        return None

    def health_check(self):
        while True:
            for node_id, node in list(self.nodes.items()):
                try:
                    container = self.docker_client.containers.get(node_id)
                    if not container.status == 'running':
                        raise Exception("Node not running")
                except Exception:
                    del self.nodes[node_id]
            time.sleep(self.health_check_interval)

    def start_health_monitoring(self):
        threading.Thread(target=self.health_check, daemon=True).start()
