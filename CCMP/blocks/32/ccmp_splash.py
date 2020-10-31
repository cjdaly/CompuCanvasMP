
import board, displayio, terminalio, time
from adafruit_matrixportal.matrix import Matrix
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label

matrix = Matrix(width=32, height=32, bit_depth=6)
grp_ccmp = displayio.Group(max_size=4)
# matrix.display.rotation=270
matrix.display.show(grp_ccmp)

rect = Rect(0,0,32,32,fill=0x000020, outline=0x444444)
grp_ccmp.append(rect)

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

grp_compu = layout_group(COMPU)
grp_ccmp.append(grp_compu)

grp_canvas = layout_group(CANVAS, 0, 10)
grp_ccmp.append(grp_canvas)

grp_mp = layout_group(MP, 0, 20, 6, 0)
grp_ccmp.append(grp_mp)

counter=0
while True:
    cycle_colors(grp_compu, COMPU, counter)
    cycle_colors(grp_canvas, CANVAS, counter)
    counter += 1
    time.sleep(0.2)
