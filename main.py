from model.devices import Light_Device
import json
from model.state import State
import time
from threading import Thread

devices = {}
settings = {}
last_update_time = -1
amt_updates = 0


state = None

def set_bulb_colour(device):

    hsv_colour = state.hsv() # Mixed RGB + Brightness

    device.set_hsv_colour(hsv_colour)

def run():

    # Handle on globals
    global amt_updates
    global last_update_time

    # Obtain State
    st = time.time()
    state.update_state()

    # Main check
    if state.changed() and settings['UPDATE_INTERVAL'] <= (time.time() - last_update_time):
        amt_updates = amt_updates + 1
        r, g, b = state.rgb()
        brightness = state.brightness()
        lt = time.time() - st
        threads = []
        for dev_name in devices:
            try:
                thr = Thread(target = set_bulb_colour, args =[devices[dev_name]])
                thr.start()
                threads.append(thr)
                last_update_time = time.time()
            except Exception as e:
                print(e)

        # Wait for the leds to update
        for th in threads:
            th.join()

        lut = last_update_time - st
        print('State Updated {0:03d} times with RGB values: ({1:03d}, {2:03d}, {3:03d}) and brightness: {4:03d} and time: {5:06f}s and request sent time: {6:06f}s'.format(amt_updates, r, b, g, brightness, lt, lut), end='\r')

def load_config():


    global settings
    global devices

    config = {}
    connections = {}

    with open('config.json') as f:
        config = json.load(f)

    settings = config['settings']

    for dev_name in config['devices']:
        device = config['devices'][dev_name]
        device['name'] = dev_name
        connections[dev_name] = Light_Device(device, DEBUG=settings['DEBUG'])


    devices = connections

if __name__ == "__main__":
    # get a connection on all devices in JSON
    load_config()
    state = State(
        SOUND=settings['ENABLE_SOUND'],
        COLOUR=settings['ENABLE_COLOUR'],
        DEFAULT_COLOUR=settings['DEFAULT_COLOUR'],
        DEFAULT_BRIGHTNESS=settings['DEFAULT_BRIGHTNESS'],
        audio_device_id=settings['AUDIO_DEVICE_ID']
        )
    while True:
        # Exec Program
        run()
