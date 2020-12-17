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

COMPU = [
  ['C', 0, 0, 0x445500],
  ['o', 0, 0, 0x335511],
  ['m', 0, 0, 0x225522],
  ['p', 0, 0, 0x115533],
  ['u', 0, 0, 0x005544],
]

CANVAS = [
  ['C', 0, 0, 0x445500],
  ['a', 0, 0, 0x335511],
  ['n', 0, 0, 0x225522],
  ['v', 0, 0, 0x115533],
  ['a', -1, 0, 0x005544],
  ['s', 0, 0, 0x006655],
]

MP = [
  ['M', 0, 0, 0x664422],
  ['P', 0, 0, 0x664422],
]

import displayio
from adafruit_display_shapes.rect import Rect
import cc_util

def cycle_colors(grp, grp_arr, index):
    ln = len(grp_arr)
    for i in range(ln):
        grp[i].color = grp_arr[(i+index)%ln][3]

CC_blockID = ""

def cc_init(cc_state):
    grp_ccmp = displayio.Group(max_size=4)
    rect = Rect(0,0,32,32,fill=0x000020, outline=0x444444)
    grp_ccmp.append(rect)
    #
    grp_compu = cc_util.layout_group(COMPU)
    grp_ccmp.append(grp_compu)
    #
    grp_canvas = cc_util.layout_group(CANVAS, 0, 10)
    grp_ccmp.append(grp_canvas)
    #
    grp_mp = cc_util.layout_group(MP, 0, 20, 6, 0)
    grp_ccmp.append(grp_mp)
    #
    return grp_ccmp

def cc_update(cc_state):
    t = cc_util.tick4(cc_state)
    grp = cc_state['groups'][CC_blockID]
    #
    if t == 0:
      i = cc_util.ticks(cc_state) // 4
      cycle_colors(grp[1], COMPU, i)
      cycle_colors(grp[2], CANVAS, i)
