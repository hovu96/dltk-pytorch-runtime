import logging
import json
import subprocess
import sys
import threading
import os
from waitress import serve
from flask import Flask, request, jsonify

app = Flask(__name__)

lock = threading.Lock()
algorithm_process = None


@app.route('/algorithm', methods=['PUT'])
def program():
    logging.info("received new algorithm")
    lock.acquire()
    try:
        global algorithm_process
        if algorithm_process:
            logging.info("terminating current algorithm")
            algorithm_process.terminate()
        logging.info("starting new algorithm")
        algorithm_process = subprocess.Popen([sys.executable, 'algorithm.py'])
    finally:
        lock.release()
    return json.dumps({})


@app.route('/models', methods=['GET'])
def list_models():
    return jsonify(["a", "b"])


@app.route('/model/<name>', methods=['PUT', 'DELETE'])
def model(name):
    if request.method == 'PUT':
        logging.info("add model %s" % name)
        return jsonify({})
    if request.method == 'DELETE':
        logging.info("remove model %s" % name)
        return jsonify({})


if __name__ == '__main__':
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
    serve(app, host="0.0.0.0", port=5001)
