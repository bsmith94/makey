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
            p.bind('<Button-1>', self.padHit)
            self.view.root.bind('<{}>'.format(p.defn.key), self.keyHit)
            self.key_map[p.defn.key] = {
                'widget' : p,
                'handler' : self._padHit
            }

    def terminate(self):
        self.view.destroy()
        self.model.terminate()

    def keyHit(self, event):
        if event.keysym in self.key_map:
            b = self.key_map[event.keysym]
            b['handler'](event, b['widget'])

    def _padHit(self, event, pad):
        self.model.play_note(60 + pad.defn.index, 127, 0)

    def padHit(self, event):
        self._padHit(event, event.widget)

if __name__ == '__main__':
    pass
