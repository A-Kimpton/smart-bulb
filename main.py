print('Program Active')

# Imports
import json
import time
from PIL import ImageGrab, ImageStat

# Custom Model Imports
import model.image_processor as imProc
from model.devices import SmartDevice, SmartBulb
from model.state import State

# Consts
UPDATE_INTERVAL = 1
state = State()
connections = {}

def set_bulb_colour(device):
    # Seperate colours
    r, g, b = state.rgb()
    brightness = state.brightness()
    colour_temp = 255
    mode = state.mode()

    if mode == 'white':
        device.set_white(brightness, colour_temp)
    else:
        device.set_colour(r, g, b)
        device.set_brightness(brightness)

def run():
    # Obtain State
    state.update_state()

    print(state.rgb())

    if state.changed():
        start_time = time.time()
        print('State Updated')
        for dev_name in connections:
            try:
                set_bulb_colour(connections[dev_name])
                print(connections[dev_name].status())
            except Exception as e:
                print("Couldn't change bulb colour on", dev_name)
                print(e)

        # Pause the program while the loop catches up
        total_time = time.time() - start_time
        diff_time = UPDATE_INTERVAL - total_time
        if diff_time > 0:
            time.sleep(diff_time)

def load_devices():
    devices = {}
    connections = {}

    with open('devices.json') as f:
        devices = json.load(f)

    for dev_name in devices:
        d = devices[dev_name]
        try:
            connections[dev_name] = SmartBulb(d['id'], d['ip'], d['key'])
        except:
            print('Device', dev_name, 'could not be connected to!')

    return connections

if __name__ == "__main__":
    # get a connection on all devices in JSON
    connections = load_devices()
    while True:
        # Exec Program
        run()
