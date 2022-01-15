#!/usr/bin/env python3
#
# Copyright (c)2022 Brian T. Smith <flatpick@gmail.com>
#
# Midi controller application.
#

import json
import os
from view import TkView
from midi import MidiController
from skin import Skin
from ui_controller import TkController
from util import *

class App:

    def __init__(self, cfg):
        self.cfg = cfg
        self.skin = Skin()
        self.midi = MidiController()
        self.view = TkView()
        self.ctl = TkController(self, self.view, self.midi)

    def start(self):
        self.skin.load(resolve_path(self.cfg.home, self.cfg['DEFAULT']['skin']))
        self.view.create(self.skin)
        self.ctl.wire()
        self.view.start()
    
if __name__ == '__main__':

    import argparse
    import configparser
    
    script_home = os.path.dirname(os.path.realpath(__file__))
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='{}/makey_midi.cfg'.format(script_home))
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read(args.config)
    if not 'version' in config['DEFAULT']:
        raise ValueError('Could not read {}'.format(args.config))

    cfg_dir = os.path.dirname(os.path.realpath(args.config))
    config.home = cfg_dir
    app = App(config)
    app.start()

