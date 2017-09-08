import json
import serial
import struct
import _thread
import time

from flask import Flask, g
from flask import request, render_template, send_from_directory

TEENSY_DEVICE = '/dev/ttyACM0'


app = Flask(__name__, static_folder='static', static_url_path='')

@app.teardown_appcontext
def close_serial(exception):
    fd = getattr(g, 'serial_fd', None)
    #print('closing serial port !!!!!!!!!!!!!!!!!!!!!!!')
    #if fd is not None:
    #    fd.close()

def init_port():
    g.serial_fd = serial.Serial(TEENSY_DEVICE)
    print("setting up logger")
    def logserial(port):
        while True:
            data = port.readline()
            print(data)
            time.sleep(1)
            #print("Logger "+":".join("{:02x}".format(c) for c in data))
    g.logger = _thread.start_new_thread(logserial, (g.serial_fd,))


def write_command(action, cmd1, key1, value1, cmd2, key2, value2):
    if getattr(g, 'serial_fd', None) is None:
        init_port()
    fd = getattr(g, 'serial_fd', None)
    print(fd)
    _write_command(fd, action, cmd1, key1, value1, cmd2, key2, value2)


def _write_command(port, action, cmd1, key1, value1, cmd2, key2, value2):
    data = struct.pack('<ccBcHccBcHc',
        action.encode('ascii'),
        cmd1.encode('ascii'),
        key1,
        ','.encode('ascii'),
        value1,
        ','.encode('ascii'),
        cmd2.encode('ascii'),
        key2,
        ','.encode('ascii'),
        value2,
        '!'.encode('ascii')
    )
    print("data len "+str(len(data)))
    print(":".join("{:02x}".format(c) for c in data))
    port.write(data)


@app.route('/bowieaction', methods=['POST'])
def bowie_action():
    req = json.loads(str(request.data, 'utf-8'))
    write_command(req['action'], req['cmd1'], int(req['key1']), int(req['val1']),
                  req['cmd2'], int(req['key2']), int(req['val2']))
    return '{"status": "ok"}'


@app.route('/<path:path>')
def send_css(path):
    return send_from_directory(app.static_folder, path)


@app.route('/')
def main_page():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
