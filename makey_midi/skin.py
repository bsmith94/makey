#!/usr/bin/env python3
#
# Copyright (c)2022 Brian T. Smith <flatpick@gmail.com>
#
# UI definitions.
#

import os
import json
from util import *


class WidgetDef:

    def __init__(self, width = None, height = None, x = None, y = None,
                 key = None, image_path = None):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.key = key
        self.image_path = image_path

    def load(self, data):
        self.width = json_get(data, 'width')
        self.height = json_get(data, 'height')
        self.x = json_get(data, 'x')
        self.y = json_get(data, 'y')
        self.key = json_get(data, 'key', required = False )
        self.image_path = json_get(data, 'image', required = False)


class ButtonDef(WidgetDef):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load(self, data, width = None, height = None, y = None, image_path = None):
        self.width = json_get(data, 'width', def_val = width)
        self.height = json_get(data, 'height', def_val = height)
        self.x = json_get(data, 'x')
        self.y = json_get(data, 'y', def_val = y)
        self.key = json_get(data, 'key')
        self.image_path = json_get(data, self.image_key(), def_val = image_path)

    def image_key(self):
        return 'image'

class TwoStateButtonDef(ButtonDef):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.active_image_path = None

    def load(self, data, active_image_path = None, **kwargs):
        super().load(data, **kwargs)
        self.active_image_path = json_get(data, 'image-active', def_val = active_image_path)

    def image_path(self):
        return 'image-inactive'

class Skin:

    def __init__(self):
        self.resource_dir = None
        self.path = None
        self.height = None
        self.width = None
        self.background = None
        self.pads = []
        self.tonics = []
        self.octaves = []
        self.patterns = []

    def load(self, path):
        self.path = path
        self.resource_dir = os.path.dirname(os.path.realpath(path))
        with open(path) as f:
            d = json.load(f)
        self.load_root(d)
        self.load_pads(d)
        self.load_tonics(d)
        self.load_octaves(d)
        self.load_patterns(d)
        #self.channels = WidgetDef()
        #self.channels.load(json_get(json_get(d, 'controls'), 'channels'))

    def load_root(self, data):
        root = json_get(data, 'root')
        self.title = json_get(root, 'title')
        self.height = json_get(root, 'height')
        self.width = json_get(root, 'width')
        self.background = resolve_path(self.resource_dir, json_get(root, 'background'))

    def load_two_states(self, data):
        defs = []
        instances = json_get(data, 'instances')
        idx = 0
        width = json_get(data, 'width', required = False)
        height = json_get(data, 'height', required = False)
        y = json_get(data, 'y', required = False)
        img_inactive = json_get(data, 'image-inactive')
        img_active = json_get(data, 'image-active')
        for p in instances:
            d = TwoStateButtonDef()
            d.load(p, width = width, height = height, y = y,
                   image_path = img_inactive, active_image_path = img_active)
            d.index = idx
            idx += 1
            defs.append(d)
        return defs

    def load_pads(self, data):
        pads = json_get(json_get(data, 'controls'), 'pads')
        self.pads = self.load_two_states(pads)

    def load_tonics(self, data):
        tonics = json_get(json_get(data, 'controls'), 'tonics')
        self.tonics = self.load_two_states(tonics)

    def load_octaves(self, data):
        octaves = json_get(json_get(data, 'controls'), 'octaves')
        self.octaves = self.load_two_states(octaves)

    def load_patterns(self, data):
        patterns = json_get(json_get(data, 'controls'), 'patterns')
        self.patterns = self.load_two_states(patterns)

if __name__ == '__main__':
    pass
