# Using a custom pyaudio library:
# https://github.com/intxcc/pyaudio_portaudio

import pyaudio
import audioop
import time

class AudioReader():

    def __init__(self, device_id=17, chunk=1024): # device 17 is default for me
        p = pyaudio.PyAudio()

        self._device_id = device_id
        self._chunk = chunk

        self._device = p.get_device_info_by_index(device_id)

        if self._device['maxOutputChannels'] > self._device['maxInputChannels']:
            self._device['channels'] = self._device['maxOutputChannels']
        else:
            self._device['channels'] = self._device['maxInputChannels']

        self._stream = p.open(format=pyaudio.paInt16,
                        channels=self._device['channels'],
                        rate=int(self._device['defaultSampleRate']),
                        input=True,
                        input_device_index = self._device_id,
                        frames_per_buffer = self._chunk,
                        as_loopback = True)

    def get_audio_rms(self):
        data = self._stream.read(self._chunk)
        rms = audioop.rms(data,2)

        return rms
