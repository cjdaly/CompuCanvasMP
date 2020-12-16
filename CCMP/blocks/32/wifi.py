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
from adafruit_matrixportal.network import Network
import cc_util

CC_blockID = ""

def cc_init(cc_state):
    grp_wifi = displayio.Group(max_size=2)
    rect = Rect(0,0,32,32,fill=0x000020, outline=0x444444)
    grp_wifi.append(rect)
    #
    font = cc_state['fonts']['helvB12']
    lbl = label.Label(font, max_glyphs=4, color=0x800000)
    lbl.text = "WiFi" ; lbl.x = 4 ; lbl.y = 14
    grp_wifi.append(lbl)
    #
    net = Network(status_neopixel=board.NEOPIXEL, debug=True)
    cc_state['network'] = net
    net.connect()
    #
    return grp_wifi

def cc_update(cc_state):
    if cc_util.tickM(cc_state, 1024) == 0:
        net = cc_state['network']
        grp = cc_state['groups'][CC_blockID]
        try:
            ip = net.ip_address
            if ip == "0.0.0.0":
                grp[1].color = 0x800000
            else:
                grp[1].color = 0x008000
        except:
            grp[1].color = 0x800000
