from flask import Flask, request
from flask import jsonify
from main_logic import handler

app = Flask(__name__)

@app.route("/clusters", methods=["POST"])
def getClusters():
    data = request.json
    return_data = handler(data)
    if return_data:
        my_data = jsonify(return_data)
        return my_data
    return jsonify({"Message:" : "Error"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)