Python
import os
import csv
import hashlib
import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuration
config = {
    "tracker_name": "DecentTracker",
    "blockchainNodeType": "full",  # full, light, or none
    "network_id": "decenttracker-net",
    "node_port": 5000,
    "max_connections": 10,
    "security_tools": [
        {"name": "Nmap", "version": "7.92"},
        {"name": "Burp Suite", "version": "2022.2.2"}
    ]
}

# Blockchain Node Configuration
blockchain_node_config = {
    "node_type": config["blockchainNodeType"],
    "node_id": hashlib.sha256(config["network_id"].encode()).hexdigest(),
    "genesis_block": {
        "block_number": 0,
        "block_hash": "0" * 64,
        "previous_block_hash": "0" * 64,
        "transactions": []
    }
}

# Database Configuration
db_config = {
    "file_name": "decenttracker.db",
    "table_name": "security_tools"
}

# Routes
@app.route('/add_tool', methods=['POST'])
def add_tool():
    tool_data = request.get_json()
    tool_data["added_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(db_config["file_name"], "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([tool_data["name"], tool_data["version"], tool_data["added_at"]])
    return jsonify({"message": "Tool added successfully"})

@app.route('/get_tools', methods=['GET'])
def get_tools():
    tools = []
    with open(db_config["file_name"], "r") as file:
        reader = csv.reader(file)
        for row in reader:
            tools.append({"name": row[0], "version": row[1], "added_at": row[2]})
    return jsonify({"tools": tools})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config["node_port"], debug=True)