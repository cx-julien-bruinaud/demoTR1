from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest
from lxml import etree

app = Flask(__name__)


@app.route("/data", methods=["POST"])
def receive_data():
    if not request.is_json:
        raise BadRequest("Content-Type must be application/json")

    payload = request.get_json()
    return jsonify({"status": "received", "data": payload}), 200


@app.route("/xml", methods=["POST"])
def receive_xml():
    file = request.files.get("file")
    if file is None:
        raise BadRequest("Missing 'file' field in multipart form data")

    parser = etree.XMLParser(resolve_entities=False, no_network=True, huge_tree=False)
    try:
        root = etree.parse(file, parser=parser).getroot()
    except etree.XMLSyntaxError as exc:
        raise BadRequest(f"Invalid XML: {exc}")

    return jsonify({"status": "received", "root_tag": root.tag}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

