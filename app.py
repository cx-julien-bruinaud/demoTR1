from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest

app = Flask(__name__)

password="ghp_dghsjdfhsksDSFDfdds123456!!!!!"
password2="ghp_dghsjdfhsksDSFDfdds123422256!!!!!"


@app.route("/data", methods=["POST"])
def receive_data():
    if not request.is_json:
        raise BadRequest("Content-Type must be application/json")

    payload = request.get_json()
    return jsonify({"status": "received", "data": payload}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

