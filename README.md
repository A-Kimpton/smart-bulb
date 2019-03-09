# smart-bulb
Code used to control my smart bulb (Lumiman RGB)

The Lumiman smart bulb has been flashed using https://github.com/ct-Open-Source/tuya-convert and I'm now also using a flashed WiFi rgb controller for controlling led strips

I've also written a few simple classes with some methods such as set_colour and exec_command. These act as a wrapper to the http requests for controlling the bulb + led strips.

The algorithm used for the rgb colour was taken from the Screen Bloom project found here: https://github.com/kershner/screenbloom

This application should work if you clone it, just make sure to edit the config.json for your smart light devices. At the moment, RGB lights are only supported currently.
