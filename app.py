from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest, UnsupportedMediaType
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
    if request.content_type != "application/xml":
        raise UnsupportedMediaType("Content-Type must be application/xml")

    parser = etree.XMLParser(resolve_entities=False, no_network=True)
    try:
        root = etree.fromstring(request.data, parser)
    except etree.XMLSyntaxError as e:
        raise BadRequest(f"Invalid XML: {e}")

    return jsonify({"status": "received", "root_tag": root.tag}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

