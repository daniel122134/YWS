import asyncio
import json
import os
import socket

from flask import Flask, send_from_directory, request

from backend.dal import installation, drinks, recipes
from backend.logic import cocktails, cleaning

ROOT_FOLDER = "my-app/build"
app = Flask(__name__, static_folder=os.path.join(ROOT_FOLDER, 'static'))

from functools import wraps

from flask import Response


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

@app.route('/clean', methods=["POST"])
@response_wrapper
def clean():
    global is_task_currently_running
    if is_task_currently_running:
        return
    is_task_currently_running = True
    result = asyncio.run(cleaning.clean_all())
    is_task_currently_running = False
    return result

@app.route('/makeDrink', methods=["POST"])
@response_wrapper
def make_drink():
    data = request.json
    name = data["name"]

    global is_task_currently_running
    if is_task_currently_running:
        return "task_already_running"

    is_task_currently_running = True
    asyncio.run(cocktails.make_cocktail(name))
    is_task_currently_running = False
    return "done"

@app.route('/getKnownDrinks', methods=["POST"])
@response_wrapper
def get_known_drinks():
    known_drinks = drinks.get_known_drinks()
    result = [{"name": drink["name"], "pic": drink["picture"]} for drink in known_drinks]
    return result


@app.route('/getAllAvailableRecipes', methods=["POST"])
@response_wrapper
def get_all_available_recipes():
    available_recipes = recipes.get_all_available_recipes()
    result = [{"name": recipe["name"], "ingredients": recipe["ingredients"], "pic": recipe["picture"]} for
              recipe in available_recipes]
    return result


@app.route('/getInstallations', methods=["POST"])
@response_wrapper
def get_installations():
    installations = installation.get_pumps_configuration()
    result = [{"pin": installation["pin"], "location": installation["location"], "drink": installation["drink"]} for
              installation in installations]
    return result


@app.route('/setDrinkToPump', methods=["POST"])
@response_wrapper
def set_drink_to_pump():
    data = request.json
    name = data["drink"]
    pin = data["pin"]
    location = data["location"]
    return installation.set_drink_to_pump(name, pin, location)


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
