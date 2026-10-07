# SPDX-FileCopyrightText: 2026 Liz Clark
#
# SPDX-License-Identifier: MIT

# Circuit Playground NeoPixel MIDI Listener

import board
import usb_midi
import adafruit_midi
import neopixel
from adafruit_midi.note_on          import NoteOn
from adafruit_midi.note_off         import NoteOff

#  midi setup
midi = adafruit_midi.MIDI(midi_in=usb_midi.ports[0], in_channel=0)

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.2, auto_write=True)

PINK = (255, 0, 50)
OFF = (0, 0, 0)

while True:
    #  receive midi messages
    msg = midi.receive()
    if msg is not None:
        if isinstance(msg, NoteOn):
            pixels.fill(PINK)
        if isinstance(msg, NoteOff):
            pixels.fill(OFF)
        print(msg)