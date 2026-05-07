from flask import Flask, jsonify
from db_config import collection

app = Flask(__name__)

# Home route
@app.route("/")
def home():
    return "Threat Intel API Running 🚀"

# Get all data
@app.route("/data")
def get_data():
    data = list(collection.find({}, {"_id": 0}))
    return jsonify(data)

# Get only high risk IPs
@app.route("/high-risk")
def high_risk():
    data = list(collection.find({"risk": "high"}, {"_id": 0}))
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
