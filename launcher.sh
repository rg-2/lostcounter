#!/bin/sh
# launcher.sh
# navigate to app directory, launch then back home

cd /
cd /home/pi/rpi-rgb-led-matrix/bindings/python/samples
sudo python3 time_test.py --led-rows 16 --led-cols 32
cd /home/pi

