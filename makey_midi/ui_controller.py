#!/usr/bin/env python3
#
# Copyright (c)2022 Brian T. Smith <flatpick@gmail.com>
#
# UI event handlers.
#


class TkController:

    def __init__(self, app, view, model, skin):
        self.app = app
        self.view = view
        self.model = model
        self.skin = skin
        self.key_map = {}

    def start(self):
        self.view.create(self.skin)
        self.wire()
        self.model.start()
        self.view.update(self.model)
        self.view.start()

    def wire_button(self, button, click, key_down, handler):
        button.bind('<Button-1>', click)
        key = button.defn.key
        if len(key) > 1:
            bkey = '<{}>'.format(key)
        else:
            bkey = key
        self.view.root.bind(bkey, key_down)
        button.handler = handler
        if button.defn.key in self.key_map:
            raise ValueError('key {} already bound'.format(button.defn.key))
        self.key_map[button.defn.key] = {
            'widget' : button,
        }

    def wire(self):
        self.view.root.protocol('WM_DELETE_WINDOW', self.terminate)
        [ self.wire_button(b, self.button_hit, self.key_hit, self._pad_hit) for b in self.view.pads]
        [ self.wire_button(b, self.button_hit, self.key_hit, self._octave_hit) for b in self.view.octaves]
        [ self.wire_button(b, self.button_hit, self.key_hit, self._tonic_hit) for b in self.view.tonics]
        [ self.wire_button(b, self.button_hit, self.key_hit, self._pattern_hit) for b in self.view.patterns]

    def terminate(self):
        self.view.destroy()
        self.model.stop()
        self.key_map = None
        self.view = None
        self.model = None

    def key_hit(self, event):
        if event.keysym in self.key_map:
            b = self.key_map[event.keysym]
            b['widget'].handler(event, b['widget'])

    def _pad_hit(self, event, pad):
        self.model.play_note(pad.defn.index)
        self.view.set_active_pad(pad)

    def _octave_hit(self, event, button):
        self.view.set_active_octave(button)
        self.model.octave = button.defn.index

    def _tonic_hit(self, event, button):
        self.view.set_active_tonic(button)
        self.model.tonic = button.defn.index

    def _pattern_hit(self, event, button):
        self.view.set_active_pattern(button)
        self.model.set_pattern(button.defn.index)

    def button_hit(self, event):
        event.widget.handler(event, event.widget)

if __name__ == '__main__':
    pass
