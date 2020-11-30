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
# import gc
import time
#import math
import json
#import board
#import busio
import displayio
from rtc import RTC
#from adafruit_bitmap_font import bitmap_font
#import adafruit_display_text.label
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect

import cc_util


# CONFIGURABLE SETTINGS ----------------------------------------------------

TWELVE_HOUR = True # If set, use 12-hour time vs 24-hour (e.g. 3:00 vs 15:00)
# COUNTDOWN = False  # If set, show time to (vs time of) next rise/set event
# BITPLANES = 6      # Ideally 6, but can set lower if RAM is tight


# SOME UTILITY FUNCTIONS AND CLASSES ---------------------------------------

def parse_time(timestring, is_dst=-1):
    """ Given a string of the format YYYY-MM-DDTHH:MM:SS.SS-HH:MM (and
        optionally a DST flag), convert to and return an equivalent
        time.struct_time (strptime() isn't available here). Calling function
        can use time.mktime() on result if epoch seconds is needed instead.
        Time string is assumed local time; UTC offset is ignored. If seconds
        value includes a decimal fraction it's ignored.
    """
    date_time = timestring.split('T')        # Separate into date and time
    year_month_day = date_time[0].split('-') # Separate time into Y/M/D
    hour_minute_second = date_time[1].split('+')[0].split('-')[0].split(':')
    return time.struct_time(int(year_month_day[0]),
                            int(year_month_day[1]),
                            int(year_month_day[2]),
                            int(hour_minute_second[0]),
                            int(hour_minute_second[1]),
                            int(hour_minute_second[2].split('.')[0]),
                            -1, -1, is_dst)


def update_time(network, timezone=None):
    """ Update system date/time from WorldTimeAPI public server;
        no account required. Pass in time zone string
        (http://worldtimeapi.org/api/timezone for list)
        or None to use IP geolocation. Returns current local time as a
        time.struct_time and UTC offset as string. This may throw an
        exception on fetch_data() - it is NOT CAUGHT HERE, should be
        handled in the calling code because different behaviors may be
        needed in different situations (e.g. reschedule for later).
    """
    if timezone: # Use timezone api
        time_url = 'http://worldtimeapi.org/api/timezone/' + timezone
    else: # Use IP geolocation
        time_url = 'http://worldtimeapi.org/api/ip'
    print("time URL: ", time_url)
    #
    time_data = network.fetch_data(time_url,
                                   json_path=[['datetime'], ['dst'],
                                              ['utc_offset']])
    print("time data: ", time_data)
    time_struct = parse_time(time_data[0], time_data[1])
    RTC().datetime = time_struct
    return time_struct, time_data[2]


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
    'time' : None,
    'date' : None,
    'last_sync' : None,
}

# ONE-TIME INITIALIZATION --------------------------------------------------
def cc_init(cc_state):
    #MATRIX = Matrix(bit_depth=BITPLANES)
    #DISPLAY = MATRIX.display
    #LARGE_FONT = bitmap_font.load_font('/fonts/helvB12.bdf')
    #SMALL_FONT = bitmap_font.load_font('/fonts/helvR10.bdf')
    fontL = cc_state['fonts']['helvB12']
    fontS = cc_state['fonts']['helvR10']
    #LARGE_FONT.load_glyphs('0123456789:')
    #SMALL_FONT.load_glyphs('0123456789:/.%')
    # Display group is set up once, then we just shuffle items around later.
    # Order of creation here determines their stacking order.
    # GROUP = displayio.Group(max_size=10)
    grp_clock = displayio.Group(max_size=4)
    rect = Rect(0,0,32,32,fill=0x000020, outline=0x444444)
    grp_clock.append(rect)
    #
    # Element 6 is the current time
    #
    lbl_time = label.Label(fontL, color=0x808080, text='00:00', x=4, y=7)
    grp_clock.append(lbl_time)
    # Element 7 is the current date
    lbl_date = label.Label(fontS, color=0x808080, text='13/33', x=4, y=16)
    grp_clock.append(lbl_date)
    # Element 8 is a symbol indicating next rise or set
    #GROUP.append(adafruit_display_text.label.Label(SYMBOL_FONT, color=0x00FF00,
    #                                             text='x', y=-99))
    # Element 9 is the time of (or time to) next rise/set event
    lbl_rise = label.Label(fontL, color=0x808080, text='00:00', x=16, y=26)
    grp_clock.append(lbl_rise)
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
    except KeyError:
        if net:
            geo = net.fetch_data('http://www.geoplugin.net/csv.gp')
            geo = geo.splitlines()
            for line in geo:
                if line.startswith('geoplugin_latitude'):
                    lat = line.split(',')[1].strip()
                elif line.startswith('geoplugin_longitude'):
                    lon = line.split(',')[1].strip()
                elif line.startswith('geoplugin_timezone'):
                    tz = line.split(',')[1].strip()
            print('Using IP geolocation: ', lat, lon)
        else:
            print('Geolocation fail!')
    CC_blockData['lat'] = lat ; CC_blockData['lon'] = lon
    #
    # Load time zone string from secrets.py, else IP geolocation for this too
    # (http://worldtimeapi.org/api/timezone for list).
    try:
        tz = cc_state['secrets']['timezone'] # e.g. 'America/New_York'
    except:
        pass
        # tz = None # IP geolocation
    CC_blockData['tz'] = tz
    #
    # Set initial clock time, also fetch initial UTC offset while
    # here (NOT stored in secrets.py as it may change with DST).
    # pylint: disable=bare-except
    # datetime = None ;  utc_off = None
    try:
        datetime, utc_off = update_time(net, tz)
    except:
        datetime, utc_off = time.localtime(), '+00:00'
    print("datetime: " + str(datetime))
    print("UTC offset: " + utc_off)
    #
    CC_blockData['datetime'] = datetime
    CC_blockData['utc_off'] = utc_off
    CC_blockData['last_sync'] = time.mktime(datetime)
    #
    return grp_clock

MONTHS = [
    "~~~",
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

# MAIN LOOP ----------------------------------------------------------------
def cc_update(cc_state):
    # gc.collect()
    now = time.time() # Current epoch time in seconds
    net = cc_state['network'] ; tz = CC_blockData['tz']
    # Sync with time server every ~2 hours
    if now - CC_blockData['last_sync'] > 2 * 60 * 60:
        try:
            CC_blockData['datetime'], CC_blockData['utc_off'] = update_time(net, tz)
            CC_blockData['last_sync'] = time.mktime(CC_blockData['datetime'])
            # continue # Time may have changed; refresh NOW value
        except:
            # update_time() can throw an exception if time server doesn't
            # respond. That's OK, keep running with our current time, and
            # push sync time ahead to retry in 30 minutes (don't overwhelm
            # the server with repeated queries).
            CC_blockData['last_sync'] += 30 * 60 # 30 minutes -> seconds
    #
    grp = cc_state['groups'][CC_blockID]
    lt = time.localtime()
    #
    grp[1].text = hh_mm(lt)
    #GROUP[6].x = CENTER_X - GROUP[6].bounding_box[2] // 2
    #GROUP[6].y = TIME_Y
    grp[2].text =  MONTHS[lt.tm_mon]
    #GROUP[7].x = CENTER_X - GROUP[7].bounding_box[2] // 2
    #GROUP[7].y = TIME_Y + 10
    #
    grp[3].text = str(lt.tm_mday)
