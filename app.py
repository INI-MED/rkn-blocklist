import logging
import os
import urllib.parse

from flask import Flask, request, redirect

from storage import storage_instance
from utils.timer import CustomTimer
from utils.swagger import swaggerui_blueprint, SWAGGER_URL

server = Flask(__name__)
server.register_blueprint(swaggerui_blueprint, urlprefix=SWAGGER_URL)
logging.basicConfig(level=logging.INFO)


def start_check():
    interval = int(os.environ.get("TIMER", 3600))
    logging.info(f"Scheduling task with interval {interval}")
    check_thread = CustomTimer.create_thread(interval, storage_instance.get_latest)
    check_thread.daemon = True
    check_thread.start()


@server.route("/")
def url():
    if not storage_instance.is_ready:
        return {"error": "Storage not ready"}

    address = request.args.get("url")
    if address is None:
        return redirect("http://0.0.0.0:5000/swagger")

    unquote_address = urllib.parse.unquote(address)
    blocked = storage_instance.check(unquote_address)
    return {"blocked_status": blocked}


def start_app():
    start_check()
    server.run(host="0.0.0.0", port=5000)


if __name__ == '__main__':
    start_app()

