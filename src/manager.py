import logging
import json
from flask import Flask, request
app = Flask(__name__)


@app.route('/algorithm', methods=['PUT'])
def program():
    logging.info("algorithm")


@app.route('/model/<name>', methods=['PUT', 'DELETE'])
def model(name):
    if request.method == 'POST':
        logging.info("add model %s" % name)
    if request.method == 'DELETE':
        logging.info("remove model %s" % name)


if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
