import time
import requests

def send_heartbeat(api_url, node_id):
    while True:
        requests.post(f"{api_url}/heartbeat", json={"node_id": node_id})
        time.sleep(10)

# Simulate starting the script for a node
if __name__ == "__main__":
    import sys
    api_url = sys.argv[1]
    node_id = sys.argv[2]
    send_heartbeat(api_url, node_id)
