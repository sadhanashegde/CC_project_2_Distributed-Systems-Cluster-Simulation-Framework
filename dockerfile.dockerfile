FROM python:3.9-slim
COPY node_simulator.py /node_simulator.py
CMD ["python", "/node_simulator.py"]
