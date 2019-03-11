# Reactive Smart Devices Controlled via PC Audio and Visuals

Goal of the project:
 - Control smart RGB controllers and smart bulbs to be in sync with the PC's colours displayed on screen and PC audio.
 - Devices should be flashed with Tasmotto so that the HTTP requests to the bulbs work.
 
There is currently two ways to control the smart devices: statically or cued by either a "sound processor" or "image processor". This is set in config.json:
 - If `ENABLE_COLOUR` is set to `true`, it will ignore `DEFAULT_COLOUR` (RGB array from 0..255) and use the image processor to select a colour from the screen to be the desired colour displayed by the smart devices. Otherwise, if `ENABLE_COLOUR` is set to `false`, the `DEFAULT_COLOUR` is used.
 - If `ENABLE_SOUND` is set to `true`, it will ignore `DEFAULT_BRIGHTNESS` (value from 0..255) and use the sound processor to select a brightness based off the audio levels being outputted by the audio device set in `AUDIO_DEVICE_ID`. If `ENABLE_SOUND` is `false` then `DEFAULT_BRIGHTNESS` is used.
 
To use this project, simply edit the `config.json` to your liking, follow the same pattern I have in the example `config.json` and it should just work. I advise you disable the `ENABLE_COLOUR` as it introduced alot of latancy. The sound algorithm works really smooth however.
 
The equipment I'm using is:
 - Lumimans SmartBulb RGB: https://www.amazon.co.uk/dp/B07DW539RR/
 - RGB Controller: https://www.amazon.co.uk/dp/B078RQVNLK/
 - The smart bulb was flashed using `Tuya-Convert` and the RGB Controller was flashed via `Sonoff-Tasmota`
 
Tuya-Convert: https://github.com/ct-Open-Source/tuya-convert
Sonoff-Tasmota: https://github.com/arendst/Sonoff-Tasmota/

The image processor algorim is copied from the `Screenbloom` project for Phillips Hue bulbs. Its rather slow, even with image resizing: hopefully a newer algorithm can be implmented soon.

ScreenBloom: https://github.com/kershner/screenbloom


