# The MIT License (MIT)
#
# Copyright (c) 2020 Chris J Daly (github user cjdaly)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import board, displayio, terminalio, time
from adafruit_matrixportal.matrix import Matrix
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label

try:
    from secrets import secrets
except ImportError:
    print('Missing secrets.py!')
    raise

try:
    from cc_config import cc_config
except ImportError:
    print('Missing cc_config.py!')
    raise

cc_state = {
    'secrets' : secrets,
    'config' : cc_config,
    'blocks' : {},
    'groups' : {}
}

def init(cc_state):
    CCMP_model = cc_state['config']['CCMP_model']
    width = 32 ; height = 32
    if CCMP_model == '64x':
        width = 64 ; height = 64
        cc_state['width'] = 64 ; cc_state['height'] = 64
    elif CCMP_model == '64h':
        width = 64 ; height = 32
        cc_state['width'] = 64 ; cc_state['height'] = 32
    elif CCMP_model == '64v':
        width = 64 ; height = 32
        cc_state['width'] = 32 ; cc_state['height'] = 64
    else:
        cc_state['width'] = 32 ; cc_state['height'] = 32
    #
    matrix = Matrix(width=width, height=height, bit_depth=6)
    cc_state['matrix'] = matrix
    matrix.display.rotation = cc_state['config']['rotation']
    #
    root_group = displayio.Group(max_size=8)
    root_group.append(
        Rect(0,0,cc_state['width'],cc_state['height'],
                fill=0x001020, outline=0x444444)
    ) ; cc_state['groups']['root'] = root_group
    #
    matrix.display.show(root_group)

def load(cc_state):
    pass

def update(cc_state):
    pass

def delay(cc_state):
    time.sleep(0.2)

init(cc_state)
load(cc_state)

while True:
    update(cc_state)
    delay(cc_state)
