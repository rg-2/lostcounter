#!/usr/bin/env python
from displaybase import DisplayBase
from rgbmatrix import graphics
from datetime import datetime, timedelta
import time
import json
import os
from color_converter import create_graphics_colors, load_config_from_json, get_label_color, get_time_color


config_file = 't0.json'
app_data = {}
label_rgb = (255, 255, 255)
time_rgb = (255, 255, 255)
label_color = graphics.Color(255, 255, 255)
default_time = graphics.Color(255, 255, 255)
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

def get_colors():

    try:
        label_rgb, time_rgb = create_graphics_colors(config_file)
        
        # Check if colors were found
        if label_rgb is None:
            print("Warning: Could not find or parse label_color")
            label_rgb = (255, 255, 255)  # Default to white
         
        if time_rgb is None:
            print("Warning: Could not find or parse time_color") 
            time_rgb = (255, 255, 255)  # Default to white
        
        # Create colors with defaults if needed
        label_color = graphics.Color(*label_rgb)
        time_color = graphics.Color(*time_rgb)
        
    except Exception as e:
        print(f"Error loading colors: {e}")
        # Use default colors
        label_color = graphics.Color(255, 255, 255)  # White
        time_color = graphics.Color(0, 0, 0)         # Black
        print("Using default colors")

    return label_color, time_color

#--ledrows=16 --led-cols=32
class GraphicsTest(DisplayBase):
    def __init__(self, *args, **kwargs):
        super(GraphicsTest, self).__init__(*args, **kwargs)

    def run(self):
        global t0
        canvas = self.matrix
        font = graphics.Font()
        font.LoadFont("fonts/5x8.bdf")
        blue = graphics.Color(0, 0, 255)
        dark_green = graphics.Color(0, 100, 0)
        green = graphics.Color(0, 255, 0)
        red = graphics.Color(255, 0, 0)
        white = graphics.Color(200, 200, 200)
        orange = graphics.Color(255, 128, 0)
        brown = graphics.Color(102, 51, 0)
        purple = graphics.Color(75, 0, 130)

        label_color, default_time = get_colors()

        #label_color = purple
        #default_time = orange

        #set_t0()
        get_t0()
        last_mtime = os.path.getmtime(config_file)

        interval = 1
        next_time = round(time.time() + interval) + 0.1
        while True:
            # Reload t0.json if it changed
            try:
                current_mtime = os.path.getmtime(config_file)
                if current_mtime != last_mtime:
                    print(f'{config_file} changed, reloading')
                    get_t0()
                    label_color, default_time = get_colors()
                    last_mtime = current_mtime
            except OSError:
                pass  # file might be momentarily missing during a save 

            t1 = datetime.now()
            tdiff = t0 - t1
            if tdiff < timedelta(hours=-24):
                tdiff = timedelta(0)
                timecolor = default_time
                get_t0()
            elif tdiff < timedelta(0):
                tdiff = timedelta(0)
                timecolor = red
            else:
                timecolor = default_time


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
            graphics.DrawText(canvas, font, 11, 7, label_color, day_msg)
            graphics.DrawText(canvas, font, 26, 7, label_color, hour_msg)
            graphics.DrawText(canvas, font, 11, 14, label_color, min_msg)
            graphics.DrawText(canvas, font, 26, 14, label_color, sec_msg)

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
