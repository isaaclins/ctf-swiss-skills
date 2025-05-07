from flask import Flask, jsonify, send_from_directory
import os

app = Flask(__name__)

SHIPMENTS_DIR = "shipments"

@app.route('/shipments/<shipment_id>')
def get_shipment(shipment_id):
    file_path = os.path.join(SHIPMENTS_DIR, f"shipment-{shipment_id}.json")
    if os.path.exists(file_path):
        return send_from_directory(SHIPMENTS_DIR, f"shipment-{shipment_id}.json")
    else:
        return jsonify({
            "error": f"Shipment #{shipment_id} not found. Please check the shipment ID and try again."
        }), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)