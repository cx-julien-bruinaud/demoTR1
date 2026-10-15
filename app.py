from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest, UnsupportedMediaType
from lxml import etree
from lxml.html.clean import Cleaner

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


_cleaner = Cleaner(
    scripts=True,
    javascript=True,
    comments=True,
    style=True,
    links=True,
    meta=True,
    page_structure=False,
    processing_instructions=True,
    embedded=True,
    frames=True,
    forms=False,
    annoying_tags=True,
    safe_attrs_only=True,
)


@app.route("/sanitize-html", methods=["POST"])
def sanitize_html():
    if not request.content_type or not request.content_type.startswith("text/html"):
        raise UnsupportedMediaType("Content-Type must be text/html")

    raw_html = request.data.decode("utf-8", errors="replace")
    if not raw_html.strip():
        raise BadRequest("Request body must not be empty")

    try:
        cleaned = _cleaner.clean_html(raw_html)
    except Exception as e:
        raise BadRequest(f"Failed to sanitize HTML: {e}")

    return cleaned, 200, {"Content-Type": "text/html; charset=utf-8"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

