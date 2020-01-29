import logging
import json
import subprocess
import sys
import threading
from flask import Flask, request
app = Flask(__name__)


lock = threading.Lock()
algorithm_process = None


@app.route('/algorithm', methods=['PUT'])
def program():
    logging.info("algorithm")
    lock.acquire()
    try:
        global algorithm_process
        if algorithm_process:
            algorithm_process.terminate()
        algorithm_process = subprocess.Popen([sys.executable, 'algorithm.py'])
    finally:
        lock.release()


@app.route('/model/<name>', methods=['PUT', 'DELETE'])
def model(name):
    if request.method == 'POST':
        logging.info("add model %s" % name)
    if request.method == 'DELETE':
        logging.info("remove model %s" % name)


if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
