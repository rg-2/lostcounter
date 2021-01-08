#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import graphics
from datetime import datetime, timedelta
import time
import json

config_file = '/home/pi/time_test_config.json'
app_data = {}
t0 = datetime.now()

def dt_dhms(dt):
    return dt.days, dt.seconds//3600, (dt.seconds//60)%60, dt.seconds%60

# Set a new t0
def set_t0():
    global t0
    t0 = datetime.now()
    app_data['t0'] = t0.isoformat()

    try:
        with open(config_file, 'w') as f:
            json.dump(app_data, f, indent=4)

    except:
        print('err')

    return t0

# get t0 from config file
def get_t0():
    global t0

    try:
        with open(config_file) as f:
            app_data = json.load(f)

        t0 = datetime.fromisoformat(app_data['t0'])

    except:
        print('err')
        set_t0()

    return t0

#--ledrows=16 --led-cols=32
class GraphicsTest(SampleBase):
    def __init__(self, *args, **kwargs):
        super(GraphicsTest, self).__init__(*args, **kwargs)

    def run(self):
        global t0
        canvas = self.matrix
        font = graphics.Font()
        font.LoadFont("../../../fonts/5x8.bdf")
        blue = graphics.Color(0, 0, 255)
        red = graphics.Color(255, 0, 0)

        #set_t0()
        get_t0()

        interval = 1
        next_time = round(time.time() + interval) + 0.1
        while True:
            t1 = datetime.now()
            tdiff = t1 - t0
            tdiff_dhms = dt_dhms(tdiff)
            top_msg = f'{tdiff_dhms[0]:02d}d{tdiff_dhms[1]:02d}h'
            bot_msg = f'{tdiff_dhms[2]:02d}m{tdiff_dhms[3]:02d}s'
            canvas.Clear()
            graphics.DrawText(canvas, font, 1, 7, blue, top_msg)
            graphics.DrawText(canvas, font, 1, 14, red, bot_msg)

            # Force time updates to happen on uniform intervals\
            sleep_time = next_time - time.time()
            if sleep_time < 0.1:
                next_time = round(time.time() + interval) + 0.1
                sleep_time = 0.2
            # print(f'sleep:{sleep_time} next{next_time} time{time_temp}')
            time.sleep(sleep_time)
            next_time += interval

# Main function
if __name__ == "__main__":
    graphics_test = GraphicsTest()
    if (not graphics_test.process()):
        graphics_test.print_help()
