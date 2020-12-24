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

cc_config = {
    'CCMP_model' : '32', # 32, 64h, 64v, 64x
    'rotation' : 0,      # 0, 90, 180, 270 (degrees)
    'activeBlocks' : ["32/wifi", "32/moon_clock"],
    'blocks' : {
        "32/moon_clock" : {"x":0, "y":0},
        "32/wifi" : {"x":0, "y":32},
        "32/mem_info" : {"x":32, "y":0},
        "32/ccmp_splash" : {"x":32, "y":32},
        "64h/msg_board" : {"x":0, "y":32,
            "bg" : 0x00_08_10, "ol" : 0x33_33_33, "lines" : [
                # text , x, y, font, color
                ["Happy", 5, 8, 'helvR10', 0x00_80_00],
                ["Holidays", 9, 20, 'helvR10', 0x80_00_00],
            ],
        },
    }
}
