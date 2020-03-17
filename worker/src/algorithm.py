import logging
import json
import os
import datetime
from waitress import serve
import torch.distributed as dist
from torch.distributed import rpc
from flask import Flask, jsonify
app = Flask(__name__)

import sys
sys.path.insert(0, "/code")


def inner_fit(events):
    logging.info("received inner_fit request")
    dltk_code = __import__("dltk_code")
    results = dltk_code.fit(events)
    logging.info("inner_fit done")
    return results


@app.route('/fit', methods=['POST'])
def fit():
    logging.info("received /fit request")
    return jsonify({
        "dltk-pytorch-runtime-method": "fit",
    })


@app.route('/apply', methods=['GET'])
def apply():
    logging.info("apply")
    return jsonify({
        "dltk-pytorch-runtime-method": "apply",
    })


if __name__ == '__main__':
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
    # dist.init_process_group('gloo')
    rank = int(os.environ.get("RANK"))
    rpc.init_rpc(
        "Worker%s" % rank,
        world_size=int(os.environ.get("WORLD_SIZE")),
        rank=rank,
        rpc_backend_options=rpc.backend_registry.construct_rpc_backend_options(
            rpc.backend_registry.BackendType.PROCESS_GROUP,
            rpc_timeout=datetime.timedelta(hours=1)
        )
    )
    serve(
        app,
        host="0.0.0.0",
        port=5001,
        channel_timeout=100000,
    )
