"""
A flask server that presents a control panel for Bowie
"""
from __future__ import print_function

from io import BytesIO
import json
import struct
import queue
import time
import _thread

import picamera
import serial

from flask import Flask, g, current_app
from flask import request, render_template, send_from_directory, send_file

TEENSY_DEVICE = '/dev/ttyACM0'

APP = Flask(__name__, static_folder='static', static_url_path='')

@APP.teardown_appcontext
def close_serial(exception):
    fd = g.get('serial_fd', None)

def init_port():
    """
    init serial port and start port reader
    """
    g.serial_fd = serial.Serial(TEENSY_DEVICE)
    g.packet_queue = queue.Queue(10)
    print('setting up logger')
    def logserial(port, queue):
        """
        log serial data, send packets to queue
        """
        print('in logserial')
        while True:
            data = port.readline()
            if chr(data[0]) == '$' and chr(data[-3]) == '!':  # assume it's a packet
                print('Logger '+':'.join('{:02x}'.format(c) for c in data))
                queue.put(data)
            print(data)
    g.logger = _thread.start_new_thread(logserial, (g.serial_fd, g.packet_queue))
    return g.serial_fd


def write_command(action, cmd1, key1, value1, cmd2, key2, value2):
    """
    get port file descriptor and write command to it
    """
    serial_fd = g.get('serial_fd', None)
    print('in write_command ' + str(serial_fd))
    if not serial_fd:
        serial_fd = init_port()
    _write_command(serial_fd, action, cmd1, key1, value1, cmd2, key2, value2)


def _write_command(port, action, cmd1, key1, value1, cmd2, key2, value2):
    """
    properly format packet and send it
    """
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


@APP.route('/bowieaction', methods=['POST'])
def bowie_action():
    """
    proxy request to teensy
    """
    req = json.loads(str(request.data, 'utf-8'))
    write_command(req['action'], req['cmd1'], int(req['key1']), int(req['val1']),
                  req['cmd2'], int(req['key2']), int(req['val2']))
    return '{"status": "ok"}'


@APP.route('/picam.jpg')
def capture_picture():
    """
    grab a frame from the camera and stream it back
    """
    cam = picamera.PiCamera()
    byte_stream = BytesIO()
    cam.start_preview()
    time.sleep(2)
    cam.capture(byte_stream, 'jpeg')
    cam.stop_preview()
    cam.close()
    byte_stream.seek(0)
    return send_file(byte_stream, mimetype='img/jpeg', cache_timeout=2)

@APP.route('/<path:path>')
def send_static(path):
    """
    serve all static content
    """
    return send_from_directory(APP.static_folder, path)


@APP.route('/')
def main_page():
    """
    serve index.html fromt template
    """
    return render_template('index.html')


if __name__ == '__main__':
    APP.run(debug=True, host='0.0.0.0')
