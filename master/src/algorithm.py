import logging
import os
import datetime
import torch.distributed as dist
from torch.distributed import rpc
from waitress import serve
from flask import Flask, jsonify, request
app = Flask(__name__)

import sys
sys.path.insert(0, "/code")

world_size = int(os.environ.get("WORLD_SIZE"))


def inner_fit(events):
    return "master"


@app.route('/fit', methods=['POST'])
def fit():
    logging.info("fit")
    events = request.get_json()

    import algorithm
    worker_futures = []
    for rank in range(1, world_size):
        worker_name = "Worker%s" % rank
        f = rpc.rpc_async(worker_name, algorithm.inner_fit, (events,))
        #logging.info("worker_fit_result: %s" % worker_fit_result)
        worker_futures.append(f)

    dltk_code = __import__("dltk_code")
    result = dltk_code.fit(events)

    for f in worker_futures:
        f.wait()
        # result.append(r)

    return jsonify(result)

    # await ...


@app.route('/apply', methods=['GET'])
def apply():
    logging.info("apply")
    return jsonify({
        "dltk-pytorch-runtime-method": "apply-master",
    })


if __name__ == '__main__':
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
    rpc.init_rpc(
        "Master",
        world_size=world_size,
        rank=int(os.environ.get("RANK")),
        rpc_backend_options=rpc.backend_registry.construct_rpc_backend_options(
            rpc.backend_registry.BackendType.PROCESS_GROUP,
            rpc_timeout=datetime.timedelta(hours=1)
        )
    )
    logging.info("rpc inited")
    # dist.init_process_group('gloo')
    serve(
        app,
        host="0.0.0.0",
        port=5002,
        channel_timeout=100000,
    )
