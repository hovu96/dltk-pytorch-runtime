import logging
import json
import subprocess
import sys
import threading
import os
import shutil
from waitress import serve
from flask import Flask, request, jsonify

app = Flask(__name__)

lock = threading.Lock()
algorithm_process = None

models_path = "/models"


def restart_algorithm():
    lock.acquire()
    try:
        global algorithm_process
        if algorithm_process:
            logging.info("terminating current algorithm")
            algorithm_process.terminate()
        logging.info("starting new algorithm")
        algorithm_process = subprocess.Popen([sys.executable, 'algorithm.py'])
        return {}
    finally:
        lock.release()


restart_algorithm()


@app.route('/algorithm', methods=['PUT'])
def program():
    logging.info("received new algorithm")
    a = restart_algorithm()
    return json.dumps(a)


@app.route('/models', methods=['GET'])
def list_models():
    model_names = []
    for model_name in os.listdir(models_path):
        if model_name == "lost+found":
            continue
        full_path = os.path.join(models_path, model_name)
        if os.path.isdir(full_path):
            model_names.append(model_name)
    return jsonify(model_names)


@app.route('/model/<model_name>', methods=['PUT', 'DELETE'])
def model(model_name):
    if request.method == 'PUT':
        logging.info("creating model %s ..." % model_name)
        full_path = os.path.join(models_path, model_name)
        os.mkdir(full_path)
        return jsonify({})
    if request.method == 'DELETE':
        logging.info("removing model %s ..." % model_name)
        full_path = os.path.join(models_path, model_name)
        shutil.rmtree(full_path)
        return jsonify({})


if __name__ == '__main__':
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
    serve(app, host="0.0.0.0", port=5001)
