import logging
import json
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


@app.route('/program', methods=['GET'])
def program():
    logging.info("apply")
    return json.dumps({
        "a": "b",
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
