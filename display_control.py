#!/usr/bin/env python
from displaybase import DisplayBase
from rgbmatrix import graphics
from datetime import datetime, timedelta
import time
import json

config_file = 't0.json'
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
class GraphicsTest(DisplayBase):
    def __init__(self, *args, **kwargs):
        super(GraphicsTest, self).__init__(*args, **kwargs)

    def run(self):
        global t0
        canvas = self.matrix
        font = graphics.Font()
        font.LoadFont("fonts/5x8.bdf")
        #blue = graphics.Color(0, 0, 255)
        green = graphics.Color(0, 255, 0)
        red = graphics.Color(255, 0, 0)
        white = graphics.Color(100,100,100)

        #set_t0()
        get_t0()

        interval = 1
        next_time = round(time.time() + interval) + 0.1
        while True:
            t1 = datetime.now()
            tdiff = t0 - t1
            if tdiff < timedelta(hours=-24):
                tdiff = timedelta(0)
                timecolor = white
                get_t0()
            elif tdiff < timedelta(0):
                tdiff = timedelta(0)
                timecolor = green
            else:
                timecolor = red


            tdiff_dhms = dt_dhms(tdiff)
            top_msg = f'{tdiff_dhms[0]:2d} {tdiff_dhms[1]:2d}'
            bot_msg = f'{tdiff_dhms[2]:2d} {tdiff_dhms[3]:2d}'
            day_msg = 'd'
            hour_msg = 'h'
            min_msg = 'm'
            sec_msg = 's'

            canvas.Clear()
            graphics.DrawText(canvas, font, 1, 7, timecolor, top_msg)
            graphics.DrawText(canvas, font, 1, 14, timecolor, bot_msg)
            graphics.DrawText(canvas, font, 11, 7, white, day_msg)
            graphics.DrawText(canvas, font, 26, 7, white, hour_msg)
            graphics.DrawText(canvas, font, 11, 14, white, min_msg)
            graphics.DrawText(canvas, font, 26, 14, white, sec_msg)

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
        #graphics_test.print_help() print help member does not seem to exist
        print('graphics_test.process failed!!')
