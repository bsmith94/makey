#!/usr/bin/env python3
#
# Copyright (c)2022 Brian T. Smith <flatpick@gmail.com>
#
# UI event handlers.
#

class TkController:

    def __init__(self, app, view, model):
        self.app = app
        self.view = view
        self.model = model
        self.key_map = {}

    def wire(self):
        self.view.root.protocol('WM_DELETE_WINDOW', self.terminate)
        for p in self.view.pads:
            p.bind('<Button-1>', self.pad_hit)
            self.view.root.bind('<{}>'.format(p.defn.key), self.key_hit)
            self.key_map[p.defn.key] = {
                'widget' : p,
                'handler' : self._pad_hit
            }

    def terminate(self):
        self.view.destroy()
        self.model.terminate()

    def key_hit(self, event):
        if event.keysym in self.key_map:
            b = self.key_map[event.keysym]
            b['handler'](event, b['widget'])

    def _pad_hit(self, event, pad):
        self.model.play_note(60 + pad.defn.index, 127, 0.1, 0)

    def pad_hit(self, event):
        self._pad_hit(event, event.widget)

if __name__ == '__main__':
    pass
