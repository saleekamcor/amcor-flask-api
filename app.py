from flask import Flask, request, jsonify, abort
import os, json

app = Flask(__name__)
DATA_DIR = "./data"  # This folder will hold all your JSON files
API_KEY = "your-secret-key"  # Change this to a strong secret!

def check_auth():
    if request.headers.get("X-API-KEY") != API_KEY:
        abort(403)

@app.route("/read/<filename>", methods=["GET"])
def read_file(filename):
    check_auth()
    fn = os.path.join(DATA_DIR, filename)
    if not os.path.exists(fn):
        return jsonify({}), 200
    with open(fn, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except:
            return jsonify({"error": "Corrupt or invalid file"}), 500
    return jsonify(data), 200

@app.route("/write/<filename>", methods=["POST"])
def write_file(filename):
    check_auth()
    fn = os.path.join(DATA_DIR, filename)
    data = request.json
    with open(fn, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return jsonify({"status": "ok"}), 200

@app.route("/ping")
def ping():
    return "pong", 200

if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)
    app.run(host="0.0.0.0", port=8000)
