# The Lost Counter... Morphed into a Count Down Timer

Fun tool to track how long its been since we've lost something in this house... Nope, not any more.  Now it counts down to an exciting event.  Usually Camping, but it could be anything.

It's an RGB dot matrix display powered by a raspberry pi running python using hzeller's rpi-rgb-led-matrix library found here:

https://github.com/hzeller/rpi-rgb-led-matrix

## Just getting started...
This will have more info if I ever have time...

### Hardware
RPI 3
Adafruit Medium 16x32 RGB LED matrix panel - 6mm Pitch (420)
Adafruit RGB matrix bonnett (3211)

### Files
- *display_control.py*
  - Modified example to count down to the target time read from t0.json
- *displaybase.py*
  - Base Class supplied by hzeller's library used by display_control.py
- *t0.json*
  - Contains the target time
- *config.json*
  - Unused
- *launcher.sh*
  - Bash script used to launch the countdown timer when the RPI starts up
