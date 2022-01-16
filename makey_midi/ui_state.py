#!/usr/bin/env python3
#
# Copyright (c)2022 Brian T. Smith <flatpick@gmail.com>
#
# UI state.
#

from midi import Note, MidiController

class UiState:

    def __init__(self, cfg):
        self.cfg = cfg
        self.octave = None
        self.tonic = None
        self.pattern = None
        self.channel = None
        self.instrument = None
        self.velocity = None
        self.durtion = None
        self.midi = None
        self.patterns = None

    def start(self):
        self.octave = 3
        self.tonic = 0
        self.pattern = 0
        self.channel = 0
        self.instrument = 0
        self.velocity = 127
        self.duration = None
        self.patterns = [
            {
                'name' : 'Ionian',
                'notes' : (0, 2, 4, 7, 9)
            },
            {
                'name' : 'Dorian',
                'notes' : (0, 2, 5, 7, 10)
            },
            {
                'name' : 'Phrygian',
                'notes' : (0, 3, 5, 8, 10)
            },
            {
                'name' : 'Mixolydian',
                'notes' : (0, 2, 5, 7, 9)
            },
            {
                'name' : 'Aeolian',
                'notes' : (0, 3, 5, 7, 10)
            }
        ]
        self.midi = MidiController(self.cfg)
        self.midi.start()
        self.midi.set_instrument(self.channel, self.instrument)

    def stop(self):
        self.midi.terminate()
        self.midi = None

    def set_pattern(self, index):
        pl = len(self.patterns)
        if 0 > index or index >= pl:
            index = 0
        self.pattern = index

    def note_value(self, index):
        return (self.octave + 1) * 12 + self.tonic + index

    def play_note(self, index):
        p = self.patterns[self.pattern]
        numbers = p['notes']
        if index < 0 or index >= len(numbers):
            index = 0
        nv = self.note_value(numbers[index])
        #print('play {}'.format(self.midi.midi_to_ansi_note(nv)))
        self.midi.play_note(nv, self.velocity, self.duration, self.channel)
