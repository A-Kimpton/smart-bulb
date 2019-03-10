import requests

class Device():

    def __init__(self, device, DEBUG=False):

        base_url = 'http://' + device['ip'] + '/cm?'
        if device['username'] != None and device['password'] != None:
            base_url += '&user={0}&password={1}&'.format(device['username'],
             device['password'])
        base_url += 'cmnd='

        self._device_url = base_url
        self._name = device['name']
        self._ip = device['ip']
        self._debug = DEBUG

    def exec_command(self, cmnd):
        if self._debug:
            print('Sending command "{}" to {}'.format(cmnd, self._name))
        url = self._device_url + self.command_sanitiser(cmnd)
        response = requests.get(url)

        resp_code = response.status_code

        if response.status_code == 200:
            resp_json = response.json()

            if self._debug:
                print(resp_json)

            return resp_json
        else:
            if self._debug:
                print('Device {} returned http code: {}'.format(self._name,
             resp_code))
            return resp_code


    @staticmethod
    def command_sanitiser(cmnd):
        return cmnd.replace(' ', '%20').replace(';', '%3B')

    def set_power_state(self, ps):
        ps = str(ps)
        accepted_args = ['0', '1', 'on', 'off', 'toggle']

        command = 'Power '
        if ps.lower() in accepted_args:
            command += str(ps)

            return self.exec_command(command)

        return None

    def get_power_state(self):
        command = 'Power'
        return self.exec_command(command)

    def set_option_x(self, x, value):
        x = str(x)
        value = str(value)

        command = 'SetOption' + x + ' ' + value

        return self.exec_command(command)


class Light_Device(Device):

    def __init__(self, device):
        super().__init__(device)
        super().set_option_x(17, 1) # (0..255, 0..255, 0..255)
        self._mode = 'rgb'

        super().exec_command('Fade 1')

    def mode(self):
        return self._mode

    def set_color_mode(self, mode):
        self._mode = mode

    def set_colour(self, rgb, mode=None, ww=0, cw=0):
        return set_colour_and_brightness(rgb=rgb, mode=mode, ww=ww, cw=cw)

    def set_brightness(self, value):
        return set_colour_and_brightness(brightness=value)

    def set_colour_and_brightness(self, rgb=None, mode=None, ww=0, cw=0, brightness=None):
        command = ''
        if rgb and brightness > -1:
            command += 'Backlog '

        if rgb:
            command = 'Color '
            if not mode:
                mode = self._mode

            if mode == 'rgb':
                # Expecting (125, 120, 13)
                r, g, b = rgb
                command += str(r) + str(g) + str(b)
            elif mode == 'RRGGBBWW':
                # Expecting FF00FF..
                command += rgb + ww
            elif mode == 'RRGGBBWWCW':
                # Expecting FF00FF..
                command += rgb + ww + wc + ';'

        if brightness > -1:
            if value >= 0 and value <=100:
                command = 'Dimmer ' + str(value)

        return self.exec_command(command)
