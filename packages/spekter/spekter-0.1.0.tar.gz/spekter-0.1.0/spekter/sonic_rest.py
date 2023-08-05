from flask import Flask, jsonify, request
from spekter.sonic_utils import search, parse_search

app = Flask(__name__)

@app.route("/search", methods=["POST"])
def sonic_search():
    query = request.form.get("query")
    return jsonify(
        parse_search(search(query))
    )

if __name__=="__main__":
    app.run(host="127.0.0.1", port="1492", debug=True)