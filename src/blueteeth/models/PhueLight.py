import os
from phue import Bridge
from math import floor
from random import random
from webcolors import name_to_rgb
import colorsys

from src.blueteeth.models.ModelUtils import translate


class PhueLight:
    # TODO Move this to a config file
    speed = 700
    disco_iterations = 100
    off_deciseconds = 5

    def __init__(self):
        self.bridge = Bridge(os.environ['BRIDGE_IP'])
        self.bridge.connect()

    def disco_light(self):
        lights = self.bridge.lights
        for i in range(0, self.disco_iterations):
            for light in lights:
                light.on = True
                light.transitiontime = 1
                if floor(i / self.off_deciseconds) % 2 == 0:
                    light.hue = 0
                    light.sat = 0
                    light.brightness = 0
                else:
                    light.brightness = 254
                    light.hue = random() * 65535
                    light.sat = random() * 254

    @staticmethod
    def name_to_hs(color: str):
        rgb = name_to_rgb(color)
        h, s, v = colorsys.rgb_to_hls(rgb.red, rgb.green, rgb.blue)
        hue = int(translate(h, 0, 1, 0, 65535))
        sat = int(translate(s, 0, 1, 0, 254))
        return hue, sat

    def set_light(self, color: str, light_indices: [int] = []):
        hue, sat = self.name_to_hs(color)
        lights = self.bridge.lights
        for index in light_indices:
            light.on = True
            light = lights[index]
            light.hue = hue
            light.sat = sat



