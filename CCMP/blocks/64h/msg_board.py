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

import board, displayio
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
import cc_util

CC_blockID = ""

def cc_init(cc_state):
    conf = cc_state['config']['blocks'][CC_blockID]
    #
    grp_msg = displayio.Group(max_size=len(conf['lines'])+1)
    rect = Rect(0,0,64,32,fill=conf['bg'], outline=conf['ol'])
    grp_msg.append(rect)
    #
    for li in conf['lines']:
        font = cc_state['fonts'][li[3]]
        lbl = label.Label(
            font, text=li[0], x=li[1], y=li[2], color=li[4])
        grp_msg.append(lbl)
    #
    return grp_msg


def cc_update(cc_state):
    pass

