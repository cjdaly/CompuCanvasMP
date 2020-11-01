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

import board, displayio, terminalio, time, gc
from adafruit_matrixportal.matrix import Matrix
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label

matrix = Matrix(width=32, height=32, bit_depth=6)
grp_ccmp = displayio.Group(max_size=4)
# matrix.display.rotation=270
matrix.display.show(grp_ccmp)

rect = Rect(0,0,32,32,fill=0x000020, outline=0x444444)
grp_ccmp.append(rect)

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

def layout_group(grp_arr, gx=0, gy=0, lxi=5, lyi=1):
    grp = displayio.Group(max_size=len(grp_arr))
    grp.x=gx ; grp.y=gy
    #
    lx=2 ; ly=5
    for i in range(len(grp_arr)):
        lbl = label.Label(terminalio.FONT, max_glyphs=1, color=grp_arr[i][3])
        lbl.text=grp_arr[i][0] ; lbl.x=lx+grp_arr[i][1] ; lbl.y=ly+grp_arr[i][2]
        grp.append(lbl)
        lx+=(lxi+grp_arr[i][1]) ; ly+=(lyi+grp_arr[i][2])
    return grp

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

grp_mem = layout_group(MEM)
grp_ccmp.append(grp_mem)

grp_free = layout_group(FREE, -1, 14)
grp_ccmp.append(grp_free)

counter=0
while True:
    cycle_colors(grp_mem, MEM, counter)
    update_free(grp_free)
    cycle_colors(grp_free, FREE, counter)
    counter += 1
    time.sleep(0.2)
