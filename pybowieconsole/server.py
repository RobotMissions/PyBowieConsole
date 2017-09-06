import json
import struct
import thread

from flask import Flask, g
from flask import request, render_template, send_from_directory

app = Flask(__name__)

@app.teardown_appcontext
def close_serial(exception):
    fd = getattr(g, 'serial_fd', None)
    if fd is not None:
        fd.close()

def init_port():
    g.serial_fd = open('/dev/cu.usbmodem3302311', 'rb+')
    print("setting up logger")
    def logserial(port):
        while True:
            data = port.read()
            print "Logger "+":".join("{:02x}".format(ord(c)) for c in data)
    #g.logger = thread.start_new_thread(logserial, (g.serial_fd,))


def write_command(action, cmd1, key1, value1, cmd2, key2, value2):
    if getattr(g, 'serial_fd', None) is None:
        init_port()
    fd = getattr(g, 'serial_fd', None)
    print(fd)
    _write_command(fd, action, cmd1, key1, value1, cmd2, key2, value2)


def _write_command(port, action, cmd1, key1, value1, cmd2, key2, value2):
    data = struct.pack('<ccBcHccBcHc', action.encode(), cmd1.encode(), key1, ',', value1, ',', cmd2.encode(), key2, ',', value2, '!')
    print "data len "+str(len(data))
    print ":".join("{:02x}".format(ord(c)) for c in data)
    port.write(data)


@app.route('/bowieaction', methods=['POST'])
def bowie_action():
    req = json.loads(request.data)
    write_command(req['action'], req['cmd1'], int(req['key1']), int(req['val1']),
                  req['cmd2'], int(req['key2']), int(req['val2']))
    return '{"status": "ok"}'


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


@app.route('/images/<path:path>')
def send_images(path):
    return send_from_directory('images', path)


@app.route('/')
def main_page():
    return render_template('index.html')
