"""
MOON PHASE CLOCK for Adafruit Matrix Portal: displays current time, lunar
phase and time of next moonrise or moonset. Requires WiFi internet access.

Written by Phil 'PaintYourDragon' Burgess for Adafruit Industries.
MIT license, all text above must be included in any redistribution.

BDF fonts from the X.Org project. Startup 'splash' images should not be
included in derivative projects, thanks. Tall splash images licensed from
123RF.com, wide splash images used with permission of artist Lew Lashmit
(viergacht@gmail.com). Rawr!
"""

# pylint: disable=import-error
import time
import json
import displayio
import terminalio
from rtc import RTC
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect

import cc_util


# CONFIGURABLE SETTINGS ----------------------------------------------------

TWELVE_HOUR = True # If set, use 12-hour time vs 24-hour (e.g. 3:00 vs 15:00)
SYNC_TIME = 4 * 60 * 60

# SOME UTILITY FUNCTIONS AND CLASSES ---------------------------------------

def update_time(network, utc_offset = 0):
    time_url = "https://io.adafruit.com/api/v2/time/seconds"
    time_data = network.fetch_data(time_url)
    # print("time data: " + time_data)
    time_int = int(time_data) + utc_offset * 60 * 60
    time_struct = time.localtime(time_int)
    RTC().datetime = time_struct
    return time_struct

def hh_mm(time_struct):
    """ Given a time.struct_time, return a string as H:MM or HH:MM, either
        12- or 24-hour style depending on global TWELVE_HOUR setting.
        This is ONLY for 'clock time,' NOT for countdown time, which is
        handled separately in the one spot where it's needed.
    """
    if TWELVE_HOUR:
        if time_struct.tm_hour > 12:
            hour_string = str(time_struct.tm_hour - 12) # 13-23 -> 1-11 (pm)
        elif time_struct.tm_hour > 0:
            hour_string = str(time_struct.tm_hour) # 1-12
        else:
            hour_string = '12' # 0 -> 12 (am)
    else:
        hour_string = '{0:0>2}'.format(time_struct.tm_hour)
    return hour_string + ':' + '{0:0>2}'.format(time_struct.tm_min)


CC_blockID = ""
CC_blockData = {
    'last_sync' : None,
    'lat': None,
    'lon': None,
    'tz' : None
}

# ONE-TIME INITIALIZATION --------------------------------------------------
def cc_init(cc_state):
    fontL = cc_state['fonts']['helvB12']
    fontS = cc_state['fonts']['helvR10']
    #
    grp_clock = displayio.Group(max_size=6)
    #
    grp_clock.append(Rect(0,0, 32,32, fill=0x000020, outline=0x202020))
    grp_clock.append(Rect(1,10, 30,11, fill=0x080030))
    #
    lbl_time = label.Label(fontL, color=0x808080, text='00:00', x=4, y=16)
    grp_clock.append(lbl_time)
    #
    lbl_month = label.Label(fontS, color=0x804000, text='Jan', x=1, y=25)
    grp_clock.append(lbl_month)
    #
    lbl_day_num = label.Label(fontS, color=0x804000, text='33', x=17, y=26)
    grp_clock.append(lbl_day_num)
    #
    lbl_day_wk = label.Label(fontS, color=0x804000, text='Fri', x=8, y=6)
    grp_clock.append(lbl_day_wk)
    #
    # LATITUDE, LONGITUDE, TIMEZONE are set up once, constant over app lifetime
    # Fetch latitude/longitude from secrets.py. If not present, use
    # IP geolocation. This only needs to be done once, at startup!
    lat = None ; lon = None ; tz = None
    net = cc_state['network']
    try:
        lat = cc_state['secrets']['latitude']
        lon = cc_state['secrets']['longitude']
        print('Using stored geolocation: ', lat, lon)
        CC_blockData['lat'] = lat ; CC_blockData['lon'] = lon
    except KeyError:
        pass
    #
    # Load time zone string from secrets.py, else IP geolocation for this too
    # (http://worldtimeapi.org/api/timezone for list).
    try:
        tz = cc_state['secrets']['timezone'] # e.g. 'America/New_York'
        CC_blockData['tz'] = tz
    except KeyError:
        pass
    #
    try:
        utc_offset = cc_state['secrets']['utc_offset']
        CC_blockData['utc_offset'] = utc_offset
    except KeyError:
        CC_blockData['utc_offset'] = 0
    #
    #
    # Set initial last_sync time to update time right away in cc_update
    CC_blockData['last_sync'] = time.time() - SYNC_TIME
    #
    return grp_clock

MONTHS = [
    "~~~",
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

DAYS = [
    "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"
]

# MAIN LOOP ----------------------------------------------------------------
def cc_update(cc_state):
    now = time.time() # Current epoch time in seconds
    net = cc_state['network'] ; utc_offset = CC_blockData['utc_offset']
    # Sync with time server every ~4 hours
    if now - CC_blockData['last_sync'] > SYNC_TIME:
        try:
            datetime = update_time(net, utc_offset)
            CC_blockData['last_sync'] = time.mktime(datetime)
            return
        except:
            # update_time() can throw an exception if time server doesn't
            # respond. That's OK, keep running with our current time, and
            # push sync time ahead to retry in 10 minutes (don't overwhelm
            # the server with repeated queries).
            CC_blockData['last_sync'] += 15 * 60 # 15 minutes
    #
    grp = cc_state['groups'][CC_blockID]
    button_adjust = cc_state['buttons']['counter']
    lt = time.localtime(time.time() + button_adjust*60*60)
    #
    grp[2].text = hh_mm(lt)
    grp[2].x = 16 - (grp[2].bounding_box[2] // 2)
    #
    grp[3].text =  MONTHS[lt.tm_mon]
    if lt.tm_mon == 11:
        if lt.tm_mday > 19:
            grp[3].x = 0; grp[3].y = 27
        else:
            grp[3].x = 0; grp[3].y = 26
    else:
        grp[3].x = 1; grp[3].y = 25
    #
    mday = str(lt.tm_mday)
    if len(mday) == 1:
        grp[4].x = 22
    else:
        grp[4].x = 19
    grp[4].text = mday
    #
    grp[5].text = DAYS[lt.tm_wday]
    grp[5].x = 16 - (grp[5].bounding_box[2] // 2)
    #
