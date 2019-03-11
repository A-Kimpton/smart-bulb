from PIL import ImageGrab, ImageStat
import time
from model.sound_processor import AudioReader
import model.utils as utils
import math

# Custom Model Imports
import model.image_processor as imProc

class State():
    _rgb = (0, 0, 0)
    _brightness = 255
    _image = 0

    _prev_rgb = (0, 0, 0)
    _prev_brightness = 255

    _changed = False

    def __init__(self, audio_device_id=17):
        self._audio_device = AudioReader(device_id=17)

    def update_state(self):

        # Move old values to prev state
        self._move_to_prev()

        # Obtain new values
        self._update_image()
        self._update_rgb()
        self._update_brightness()

        # Update the changed field
        self._update_changed()

    def rgb(self):
        return self._rgb
    def brightness(self):
        return self._brightness
    def mode(self):
        return self._mode
    def changed(self):
        return self._changed
    def hsv(self):
        r, g, b = self._rgb

        h, s, v = utils.rgb2hsv(r, g, b)

        v = self._brightness

        return (h, s, v)

    def _update_image(self):
        # Take a screenshot
        image = ImageGrab.grab()

        # Update State
        self._image = image

    def _update_rgb(self):
        image = self._image

        start_time = time.time()

        #self._rgb = imProc.most_frequent_colour(image)
        #self._rgb = imProc.scored_frequent_colour(image)
        #self._rgb = imProc.kmeans_colour(image) # Obtains 3 clusters

        self._rgb = imProc.image_bloom_colour(image) # Calc from bloom
        
        #print('total loop time was', total_time)

    def _update_brightness(self):
        # Updating brightness based on sound:
        brightness = 20



        rms = self._audio_device.get_audio_rms()

        #scaled_rms = self._rms_by_scale(15000, 100-brightness, rms)
        scaled_rms = self._rms_by_range(100-brightness, rms)


        self._brightness = brightness + scaled_rms

    def _rms_by_scale(self, max_rms, max_scale, rms):
        min_rms = 0     # Audio = 0 means off
        max_rms = max_rms # Audio >= 20000 likely to be maxing volume meter

        min_scaled = 0  # Add to brightness by 0
        max_scaled = max_scale # Add to brightness by 90

        if rms > max_rms:
            rms = max_rms # Sometimes rms is greater than whats set

        scaled_rms = (90 * (rms / max_rms))
        scaled_rms = int(round(scaled_rms, -1)) #Rounds to nearest 10

        return scaled_rms

    def _rms_by_range(self, max_scale, rms):

        if rms < 1000:
            return 0
        elif rms < 3000:
            return 0
        elif rms < 5000:
            return 30
        elif rms < 10000:
            return 50
        elif rms < 12000:
            return 60
        elif rms < 15000:
            return 70
        else:
            return max_scale

    def _update_changed(self):
        rgb = self._rgb
        bright = self._brightness

        old_rgb = self._prev_rgb
        old_bright = self._prev_brightness

        changed = self._changed

        if old_rgb != rgb or old_bright != bright:
            changed = True
        else:
            changed = False

        self._changed = changed

    def _move_to_prev(self):
        self._prev_rgb = self._rgb
        self._prev_brightness = self._brightness
