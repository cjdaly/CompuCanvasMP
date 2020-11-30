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

import board, displayio, gc
from adafruit_display_shapes.rect import Rect
from adafruit_matrixportal.network import Network
import cc_util

IP_ADDR = [
  ["IP", -2, -1, 0x113377],
  ["Addr", 3, 2, 0x113377],
]

IP_TRIPLETS = [
  ["~~~", -8, 0, 0x331155],
  ["~~~", 0, 0, 0x442244],
  ["~~~", -30, 2, 0x552233],
  ["~~~", 0, 0, 0x663333],
]

CC_blockID = ""

def cc_init(cc_state):
    net = Network(status_neopixel=board.NEOPIXEL, debug=True)
    cc_state['network'] = net
    cc_state['network_IP'] = "0.0.0.0"
    net.connect()
    #
    grp_ipaddr = displayio.Group(max_size=3)
    rect = Rect(0,0,32,32,fill=0x000020, outline=0x444444)
    grp_ipaddr.append(rect)
    #
    grp_addr = cc_util.layout_group(IP_ADDR)
    grp_ipaddr.append(grp_addr)
    #
    grp_trip = cc_util.layout_group(IP_TRIPLETS, 0, 10, 15, 3)
    grp_ipaddr.append(grp_trip)
    #
    return grp_ipaddr

def update_ipaddr(cc_state):
    grp_trip = cc_state['groups'][CC_blockID][2]
    ip4 = cc_state['network_IP'].split('.')
    for i,lbl in enumerate(grp_trip):
        lbl.text = "{: 3d}".format(int(ip4[i]))

def cc_update(cc_state):
    net = cc_state['network']
    ip = cc_state['network_IP']
    try:
      ip = net.ip_address
    except:
      pass
    if ip != cc_state['network_IP']:
        cc_state['network_IP'] = ip
        update_ipaddr(cc_state)

