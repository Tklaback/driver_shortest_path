from flask import Flask, request, jsonify
from main_logic import handler

app = Flask(__name__)

@app.route("/clusters", methods=["POST"])
def getClusters():
    data = request.json
    return jsonify(handler(data))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)