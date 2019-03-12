import pyaudio
import audioop
import struct
import numpy as np
import time
import scipy as sp
import matplotlib.pyplot as plt
from tkinter import TclError
from scipy import fftpack

settings = {}
devices = {}

max_interval = 0.100

from model.devices import Light_Device
import json
from threading import Thread

# Settings:
UPDATING = True

frequency_blocks = {
    ''
}

chunk = 1024 * 2
device_id = 17
p = pyaudio.PyAudio()
device = p.get_device_info_by_index(device_id)
rate = int(device['defaultSampleRate'])
x_fft = np.linspace(0, rate, chunk) # from 0..44100 max plots: 2048


stream = p.open(format=pyaudio.paInt16,
                channels=device['maxOutputChannels'],
                rate=rate,
                input=True,
                input_device_index = device_id,
                frames_per_buffer = chunk,
                as_loopback = True)

# Audio definitions in hz
sub_base = lambda fr: fr > 20 and fr <= 60
base = lambda fr: fr > 60 and fr <= 250
low_mid = lambda fr: fr > 250 and fr <= 500
mid = lambda fr: fr > 500 and fr <= 2000
upper_mid = lambda fr: fr > 2000 and fr <= 4000
presence = lambda fr: fr > 4000 and fr <= 6000
brilliance = lambda fr: fr > 6000 and fr <= 20000

def normalise(value, min, max):
    return (value - min) / (max - min)

def set_bulb_colour(device, hsv_colour):
    device.set_hsv_colour(hsv_colour)

def score_frequencies(x_fft, fft):
    score = {
        'base': {
            'peak': 0,
            'average': 0,
            'count': 0,
            'total': 0
        },
        'mid': {
            'peak': 0,
            'average': 0,
            'count': 0,
            'total': 0
        },
        'treb': {
            'peak': 0,
            'average': 0,
            'count': 0,
            'total': 0
        }
    }

    max_value = np.max(fft)
    min_value = np.min(fft)

    if max_value == 0:
        max_value = 1
    if min_value == 0:
        min_value = 1 / max_value

    multiplier = 1 / max_value

    for index, freq in enumerate(x_fft):
        type = None
        if freq >= 20 and freq < 250:
            type = 'base'
        elif freq >= 250 and freq < 2400:
            type = 'mid'
        elif freq >= 2400 and freq < 9600:
            type = 'treb'
        if type and fft[index]*multiplier > 0.01:

            score[type]['count'] += 1
            score[type]['total'] += fft[index]
            if fft[index] > score[type]['peak']:
                score[type]['peak'] = fft[index]

    total = score['base']['peak'] + score['mid']['peak'] + score['treb']['peak']
    if total == 0:
        total = 1
    score['base']['peak_score'] = score['base']['peak'] / total
    score['mid']['peak_score'] = score['mid']['peak'] / total
    score['treb']['peak_score'] = score['treb']['peak'] / total
    #print('Base: {:03f}, Mid: {:03f}, Treble: {:03f}'.format(score['base']['peak_score'], score['mid']['peak_score'], score['treb']['peak_score']))
    for type in score:
        if score[type]['count'] == 0:
            score[type]['count'] = 1
        score[type]['average'] = score[type]['total'] / score[type]['count']
    total = score['base']['average'] + score['mid']['average'] + score['treb']['average']
    if total == 0:
        total = 1
    score['base']['average_score']  = score['base']['average'] / total
    score['mid']['average_score'] = score['mid']['average'] / total
    score['treb']['average_score'] = score['treb']['average'] / total
    #print('ABase: {:03f}, AMid: {:03f}, ATreble: {:03f}'.format(score['base']['average_score'], score['mid']['average_score'], score['treb']['average_score']))

    return score

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

last_update = time.time()
last_update_colour = (0,0,0)
if __name__ == "__main__":
    # get a connection on all devices in JSON
    load_config()

    while True:
        data = stream.read(chunk)
        #data_int = struct.unpack(str(4*chunk) + 'B', data)
        data = np.frombuffer(data, dtype='h') # Size = 2048
        data = np.array(data, dtype='h')/140 + 255
        #data_int = np.array(data, dtype='h')/140 + 255
        fft = fftpack.fft(np.array(data, dtype='int8') -128)
        fft = np.abs(fft[0:int(len(fft)/2)])

        fs = score_frequencies(x_fft, fft)

        hue1 = 360 # 360 = 0
        hue2 = 300
        hue_gap = hue1 - hue2

        hue_multiplier = fs['base']['peak_score']

        final_hue = (hue_gap * hue_multiplier) + hue2
        final_hue = round(final_hue, -1)

        hsv = (final_hue, 1, 50)

        if(UPDATING and (time.time() - last_update) >= max_interval) and hsv != last_update_colour:

            print('Setting colour to HSV: {}'.format(hsv))
            threads = []
            for dev_name in devices:
                try:
                    thr = Thread(target = set_bulb_colour, args =[devices[dev_name], hsv])
                    thr.start()
                    threads.append(thr)
                except Exception as e:
                    print(e)

            # Wait for the leds to update
            for th in threads:
                th.join()
            last_update = time.time()
            last_update_colour = hsv
