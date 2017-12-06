====================
Python Bowie Console
====================

This is a flask server that provides a simple web UI to control Bowie's functions.

Components
==========
* Flask
* AngularJS
* AngularMaterial

Current Status
==============
This UI simply provides buttons and a switch for binary functions, a joystick for driving and a video area
that contains a still image for now. The serial communication needs more work, but packets should be sent
properly. Incomming serial data is not handled yet.

Raspberry Pi 3
==============
The intended platform is running on a Raspbery Pi 3 w/ Raspbian Stretch.

Boot raspbian, run pisetup and enable ssh and camera, save, reboot
after it reboots, configure wifi
start a terminal and install the console
$ sudo -s
$ git clone https://github.com/RobotMissions/PyBowieConsole.git
$ cd PyBowieConsole
$ python3 setup.py install

to run the server
$ run.sh
