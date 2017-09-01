import json
import struct

from flask import Flask
from flask import request, render_template, send_from_directory

app = Flask(__name__)


def write_command(action, cmd1, key1, value1, cmd2, key2, value2):
    with open('/dev/cu.usbmodem3302311', 'rb+') as port:
        _write_command(port, action, cmd1, key1, value1, cmd2, key2, value2)


def _write_command(port, action, cmd1, key1, value1, cmd2, key2, value2):
    data = struct.pack('<ccBcHccBcHc', action.encode(), cmd1.encode(), key1, ',', value1, ',', cmd2.encode(), key2, ',', value2, '!')
    print "data len "+str(len(data))
    print ":".join("{:02x}".format(ord(c)) for c in data)
    port.write(data)


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


@app.route('/images/<path:path>')
def send_images(path):
    return send_from_directory('images', path)


@app.route('/bowieaction', methods=['POST'])
def bowie_action():
    req = json.loads(request.data)
    write_command(req['action'], req['cmd1'], int(req['key1']), int(req['val1']),
                  req['cmd2'], int(req['key2']), int(req['val2']))
    return '{"status": "ok"}'


@app.route('/')
def main_page():
    return render_template('index.html')
