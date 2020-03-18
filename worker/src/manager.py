import logging
import json
import subprocess
import sys
import threading
import os
import shutil
import http
import pathlib
import socketio
import urllib.request
import urllib.parse


master_api_host = os.environ.get("MASTER_API_HOST")
master_api_url = "http://%s:5001" % master_api_host

sio = socketio.Client()

lock = threading.Lock()
algorithm_process = None

models_path = "/models"
code_dir = "/code"
pathlib.Path(code_dir).mkdir(parents=True, exist_ok=True)
code_module_path = os.path.join(code_dir, "dltk_code.py")


def reload_code():

    code_url = urllib.parse.urljoin(master_api_url, "code")
    try:
        download_request = urllib.request.Request(code_url, method="GET")
        download_response = urllib.request.urlopen(download_request)
        code = download_response.read().decode()
    except urllib.error.HTTPError as e:
        if e.code != 404:
            logging.error("no code found")
            return
        logging.error("error downloading updated code: %s" % e)
        return
    logging.info('downloaded new code')

    lock.acquire()
    try:
        global algorithm_process
        if algorithm_process:
            logging.info("terminating current algorithm")
            algorithm_process.terminate()

        with open(code_module_path, "w") as f:
            f.write(code)
        logging.info('written code to disk')

        logging.info("starting new algorithm")
        algorithm_process = subprocess.Popen([sys.executable, 'algorithm.py'])
        return {}
    finally:
        lock.release()


@sio.event
def connect():
    logging.info("connection established")


@sio.event
def code(data):
    logging.info('code event received')
    reload_code()


@sio.event
def model(data):
    logging.info('models updated')


@sio.event
def disconnect():
    logging.info('disconnected from server')


if __name__ == '__main__':
    logging.basicConfig(
        level=os.environ.get("LOGLEVEL", "INFO"),
        format='%(asctime)s %(levelname)-8s %(message)s',
    )

    reload_code()

    logging.info('connecting to %s' % master_api_url)
    sio.connect(master_api_url)
    sio.wait()
