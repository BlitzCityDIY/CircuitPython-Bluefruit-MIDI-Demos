# SPDX-FileCopyrightText: 2026 Liz Clark
#
# SPDX-License-Identifier: MIT

# Send Pitch Bend Message with the Accelerometer

import time
import board
import busio
import adafruit_lis3dh
import usb_midi
import adafruit_midi
from adafruit_midi.pitch_bend import PitchBend

#  midi setup
midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

i2c = busio.I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA)
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, address=0x19)
lis3dh.range = adafruit_lis3dh.RANGE_2_G

no_bend = 8192 # center pitch bend value for no bend
last_bend = 8192
debounce = 0.1

while True:
    x, y, z = (value / adafruit_lis3dh.STANDARD_GRAVITY for value in lis3dh.acceleration)

    if abs(y) < debounce: # if basically level on y axis, no pitch bend
        bend = no_bend
    else:
        bend = no_bend + int(y * (8191 if y > 0 else 8192)) 

    bend = min(16383, max(0, bend)) # clamp values to pitchbend range

    if abs(bend - last_bend) > 75 or (bend == no_bend and last_bend != no_bend):
        last_bend = bend
        midi.send(PitchBend(bend))
    # print(y) # debugging
    # time.sleep(0.1)
