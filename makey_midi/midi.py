#!/usr/bin/env python3
#
# Copyright (c)2022 Brian T. Smith <flatpick@gmail.com>
#
# MIDI interface.
#

import pygame.midi

class MidiController:

    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.midi.init()
        self.instrument_id = 0
        self.channel = 0
        self.output = pygame.midi.get_default_output_id()
        self.player = pygame.midi.Output(self.output)
        self.player.set_instrument(self.instrument_id, self.channel)
        self.note = None

    def silence(self):
        if self.note:
            self.player.note_off(self.note, 127, self.channel)

    def playNote(self, note):
        self.silence()
        self.note = note
        self.player.note_on(note, 127, self.channel)

    def terminate(self):
        self.silence()

if __name__ == '__main__':
    pass
