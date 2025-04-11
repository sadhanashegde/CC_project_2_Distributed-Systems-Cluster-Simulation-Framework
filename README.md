# Cluster Management Dashboard

A web-based application to manage clusters, nodes, and pods with fault tolerance and a simple UI.

---

## Features

- **Node Management**: Add and display nodes with CPU cores and available resources.
- **Pod Management**: Launch pods, allocate resources, and view assignments.
- **Fault Tolerance**: Automatically handle node failures and reassign pods.

---

## Prerequisites

Ensure you have the following installed:

- Python 3.8 or later
- Flask (`pip install flask`)
- Git (to clone the repository)

---

## Installation and Setup

1. **Clone the Repository**  
   Use the following command to clone the project:
   ```bash
   git clone <repository-url>
   ```
   Replace `<repository-url>` with the repository URL.

2. **Navigate to the Project Directory**  
   ```bash
   cd <project-folder-name>
   ```

3. **Install Dependencies**  
   Install the required Python dependencies:
   ```bash
   pip install flask
   ```

---

## Running the Application

Start the Flask server with the following command:
```bash
python3 api_server.py
```

Once the server is running, open your browser and go to:
```
http://127.0.0.1:5000
```

---

## Testing the Application

### 1. Add a Node  
- Enter the number of CPU cores in the "Add Node" form and click **Add Node**.
- Verify that the new node appears in the **Nodes** table.

### 2. Launch a Pod  
- Enter the CPU requirement in the "Launch Pod" form and click **Launch Pod**.
- Check that the pod is allocated to a node in the **Nodes** and **Pods** tables.

### 3. Fault Tolerance  
- Simulate node failure by removing or modifying a node. Verify that pods are reassigned to available nodes.

---

---


