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

def ticks(cc_state):
    return cc_state['ticks']

def tickM(cc_state, mod):
    return cc_state['ticks'] % mod

def tick4(cc_state):
    return cc_state['ticks'] % 4

import displayio, terminalio
from adafruit_display_text import label

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