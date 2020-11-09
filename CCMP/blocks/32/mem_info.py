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

MEM = [
  ['M', 0, 0, 0x445500],
  ['e', 0, 0, 0x335511],
  ['m', 0, 0, 0x225522],
  ['o', 0, 0, 0x115533],
  ['r', 0, 0, 0x005544],
  ['y', -2, 1, 0x006655],
]

FREE = [
  ['0', 0, 0, 0x445500],
  ['0', 0, 0, 0x335511],
  ['0', 0, 0, 0x225522],
  ['0', 0, 0, 0x115533],
  ['0', 0, 0, 0x005544],
  ['0', 0, 0, 0x006655],
]

import displayio, gc
from adafruit_display_shapes.rect import Rect
import cc_util

def cycle_colors(grp, grp_arr, index):
    ln = len(grp_arr)
    for i in range(ln):
        grp[i].color = grp_arr[(i+index)%ln][3]

def update_free(grp_free):
    gc.collect()
    m = gc.mem_free()
    ms = "{:06d}".format(m)
    for i,lbl in enumerate(grp_free):
        lbl.text=ms[i]

CC_blockID = ""

def cc_init(cc_state):
    grp_meminfo = displayio.Group(max_size=3)
    rect = Rect(0,0,32,32,fill=0x000020, outline=0x444444)
    grp_meminfo.append(rect)
    #
    grp_mem = cc_util.layout_group(MEM)
    grp_meminfo.append(grp_mem)
    #
    grp_free = cc_util.layout_group(FREE, -1, 14)
    grp_meminfo.append(grp_free)
    #
    return grp_meminfo

def cc_update(cc_state):
    t = cc_util.ticks(cc_state)
    grp = cc_state['groups'][CC_blockID]
    #
    cycle_colors(grp[1], MEM, t)
    update_free(grp[2])
    cycle_colors(grp[2], FREE, t)
