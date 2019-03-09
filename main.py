from model.devices import Light_Device
import json
from model.state import State
import time

devices = {}
state = State()
UPDATE_INTERVAL = 0.010 # Updates no faster than 30ms
last_update_time = -1
amt_updates = 0

def set_bulb_colour(device):
    # Seperate colours
    rgb = state.rgb()
    device.set_colour(rgb)

def run():

    # Handle on globals
    global amt_updates
    global last_update_time

    # Obtain State
    state.update_state()

    # Main check
    if state.changed() and UPDATE_INTERVAL <= (time.time() - last_update_time):
        amt_updates = amt_updates + 1
        r, g, b = state.rgb()
        print('State Updated {0:03d} times with RGB values: ({1:03d}, {2:03d}, {3:03d})'.format(amt_updates, r, b, g), end='\r')

        for dev_name in devices:
            try:
                set_bulb_colour(devices[dev_name])
                last_update_time = time.time()
            except Exception as e:
                pass

def load_config():
    config = {}
    connections = {}

    with open('config.json') as f:
        config = json.load(f)

    for dev_name in config['devices']:
        device = config['devices'][dev_name]
        device['name'] = dev_name
        connections[dev_name] = Light_Device(device)

    return connections

if __name__ == "__main__":
    # get a connection on all devices in JSON
    devices = load_config()
    while True:
        # Exec Program
        run()
