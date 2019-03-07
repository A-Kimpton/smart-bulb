from PIL import ImageGrab, ImageStat

# Custom Model Imports
import model.image_processor as imProc
from model.devices import SmartDevice, SmartBulb

class State():
    _rgb = (0, 0, 0)
    _brightness = 255
    _mode = 'colour'
    _image = 0

    _prev_rgb = (0, 0, 0)
    _prev_brightness = 255
    _prev_mode = 'colour'

    _changed = False

    def __init__(self):
        pass

    def update_state(self):

        # Move old values to prev state
        self._move_to_prev()

        # Obtain new values
        self._update_image()
        self._update_rgb()
        self._update_image_brightness()
        self._update_mode()

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

    def _update_image(self):
        # Take a screenshot
        image = ImageGrab.grab()

        # Update State
        self._image = image

    def _update_rgb(self):
        image = self._image
        self._rgb = imProc.most_frequent_colour(image)

    def _update_image_brightness(self):
        # Grayscale -> obtain image stats
        image = self._image
        im = image.convert('L')
        stat = ImageStat.Stat(im)

        # RMS pixel brightness
        self._brightness = int(stat.rms[0])

    def _update_mode(self):
        r, g, b = self._rgb
        if r == 255 and g == 255 and b == 255:
            mode = 'white'
        else:
            mode = 'colour'

        self._mode = mode

    def _update_changed(self):
        rgb = self._rgb
        bright = self._brightness
        mode = self._mode

        old_rgb = self._prev_rgb
        old_bright = self._prev_brightness
        old_mode = self._prev_mode

        changed = self._changed

        if mode == 'white':
            if old_mode != mode:
                changed = True
            else:
                changed = False
        else:
            if old_rgb != rgb or old_bright != bright or old_mode != mode:
                changed = True
            else:
                changed = False

        self._changed = changed

    def _move_to_prev(self):
        self._prev_rgb = self._rgb
        self._prev_brightness = self._brightness
        self._prev_mode = self._mode
