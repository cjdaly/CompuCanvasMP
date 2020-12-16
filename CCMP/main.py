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
from adafruit_bitmap_font import bitmap_font

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
    'CCMP_VERSION' : "0.0.1",
    'secrets' : secrets,
    'config' : cc_config,
    'ticks' : 0,
    'blocks' : {},
    'groups' : {},
    'fonts' : {},
    'network' : None,
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
    root_group = displayio.Group(max_size=12)
    root_group.append(
        Rect(0,0,cc_state['width'],cc_state['height'],
                fill=0x001020, outline=0x444444)
    )
    cc_state['groups']['ROOT'] = root_group
    #
    cc_state['fonts']['helvB12'] = bitmap_font.load_font('/fonts/helvB12.bdf')
    cc_state['fonts']['helvR10'] = bitmap_font.load_font('/fonts/helvR10.bdf')
    #
    matrix.display.show(root_group)

def import_block(cc_state, block_name):
    try:
        block = __import__("/blocks/" + block_name)
        cc_state['blocks'][block_name] = block
        block.CC_blockID = block_name
        return block
    except ImportError:
        print('Block not found:' + block_name)

def load(cc_state):
    grp_ROOT = cc_state['groups']['ROOT']
    for name in cc_state['config']['activeBlocks']:
        block = import_block(cc_state, name)
        grp = block.cc_init(cc_state)
        #
        block_conf = cc_state['config']['blocks'][name]
        grp.x = block_conf['x'] ; grp.y = block_conf['y']
        #
        cc_state['groups'][name] = grp
        grp_ROOT.append(grp)

def update(cc_state):
    for name in cc_state['config']['activeBlocks']:
        block = cc_state['blocks'][name]
        block.cc_update(cc_state)

def delay(cc_state):
    time.sleep(0.1)

init(cc_state)
load(cc_state)

while True:
    update(cc_state)
    delay(cc_state)
    cc_state['ticks'] += 1
