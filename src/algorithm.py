import logging
import json
import os
from waitress import serve
from flask import Flask
app = Flask(__name__)


@app.route('/fit', methods=['POST'])
def fit():
    logging.info("fit")


@app.route('/apply', methods=['GET'])
def apply():
    logging.info("apply")
    return json.dumps({
        "a": "b",
    })


if __name__ == '__main__':
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
    serve(app, host="0.0.0.0", port=5002)
