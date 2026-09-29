# SPDX-FileCopyrightText: 2026 Liz Clark
#
# SPDX-License-Identifier: MIT

# Send Modulation Message with the Light Sensor

import board
import usb_midi
import adafruit_midi
import simpleio
from analogio import AnalogIn
from adafruit_midi.control_change import ControlChange

#  midi setup
midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

light = AnalogIn(board.LIGHT)

previous_modulation = 0

while True:
    mod_val = simpleio.map_range(light.value, 0, 65535, 0, 127)
    if abs(mod_val - previous_modulation) > 2:
        #  update mod_val2
        previous_modulation = mod_val
        #  create integer
        modulation = int(mod_val)
        #  create CC message
        modWheel = ControlChange(1, modulation)
        #  send CC message
        midi.send(modWheel)
