import asyncio
import base64
import json
import os
import socket

import this

from flask import Flask, send_from_directory, request

from backend.dal.wardrobe import add_item, remove_item, get_all_items
from backend.entities.Item import Item
from backend.shirtSize import get_line_data, get_line_data_for_image

ROOT_FOLDER = "frontend"
app = Flask(__name__, static_folder=os.path.join(ROOT_FOLDER, 'static'))

from functools import wraps

from flask import Response

wardrobe = {}


class BarbotResponse(object):
    def __init__(self, data, status="success", http_status_code=200, http_extra_headers=None):
        self.data = data
        self.status = status
        self.http_status_code = http_status_code
        self.http_extra_headers = http_extra_headers

    def dictify(self):
        return {"status": self.status, "data": self.data}


def response_wrapper(func):
    @wraps(func)
    def wrapper(**params):

        try:
            func_result = func(**params)
            if type(func_result) is Response:
                return func_result

            response = BarbotResponse(func_result)


        except Exception as err:
            response = BarbotResponse(str(err), "error", 500, {})

        return _make_http_response(response.dictify(), response.http_status_code, response.http_extra_headers)

    return wrapper


def _make_http_response(content=None, status_code=200, extra_headers=None, mimetype="application/json"):
    extra_headers = extra_headers or {}

    if content is None:
        content_string = ""
        mimetype = "text/plain"
    else:
        if mimetype == "application/json":
            content_string = json.dumps(content)
        else:
            content_string = content

    return Response(content_string, status_code, extra_headers, mimetype)


is_task_currently_running = False


@app.route('/getLineForImage', methods=["POST"])
@response_wrapper
def get_line():
    image_data_b64 = request.json["data"]
    image_data = base64.b64decode(image_data_b64)
    with open("./tmp.jpeg", "wb") as file:
        file.write(image_data)
    
    return get_line_data("./tmp.jpeg")





@app.route('/removeItem', methods=["POST"])
@response_wrapper
def remove_item_req():
    data = request.json
    remove_item(data["_id"])
    return wardrobe


@app.route('/addItem', methods=["POST"])
@response_wrapper
def add_item_req():
    data = request.json
    add_item(Item.from_dict(data))
    x= get_all_items()
    return x


@app.route('/getServerIp', methods=["POST"])
@response_wrapper
def get_server_ip():
    if os.name != "nt":
        import fcntl
        import struct

    def get_interface_ip(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', bytes(ifname[:15], 'utf-8'))
            # Python 2.7: remove the second argument for the bytes call
        )[20:24])

    ip = socket.gethostbyname(socket.gethostname())
    if ip.startswith("127.") and os.name != "nt":
        interfaces = ["eth0", "eth1", "eth2", "wlan0", "wlan1", "wifi0", "ath0", "ath1", "ppp0"]
        for ifname in interfaces:
            try:
                ip = get_interface_ip(ifname)
                break
            except IOError:
                pass
    return ip


@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>', methods=["GET"])
def files(path):
    return send_from_directory(ROOT_FOLDER, path)


if __name__ == '__main__':
    app.run("0.0.0.0", 80, debug=True)
