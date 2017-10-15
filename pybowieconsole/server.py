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

from flask import Flask
from flask import request, render_template, send_from_directory, send_file

TEENSY_DEVICE = '/dev/ttyACM0'

APP = Flask(__name__, static_folder='static', static_url_path='')

@APP.teardown_appcontext
def close_serial(exception):
    pass #fd = g.get('serial_fd', None)

_serial = serial.Serial(TEENSY_DEVICE)
_queue = queue.Queue(10)

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
_thread.start_new_thread(logserial, (_serial, _queue))


def write_command(action, cmd1, key1, value1, cmd2, key2, value2):
    """
    get port file descriptor and write command to it
    """
    _write_command(_serial, action, cmd1, key1, value1, cmd2, key2, value2)


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


@APP.route('/bowiesensors')
def bowie_sensors():
    """
    returns any sensor data queued
    """
    msgs = []
    _queue
    print('in queue: '+str(_queue.qsize()))
    while _queue.qsize() > 0:
        msgs.append(_queue.get())
    return json.dumps(msgs)


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
