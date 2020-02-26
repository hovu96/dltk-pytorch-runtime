import logging
import json
import os


if __name__ == '__main__':
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
    while True:
        import time
        time.sleep(3)
