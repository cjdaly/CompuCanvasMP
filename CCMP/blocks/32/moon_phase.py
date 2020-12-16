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
import math
import json
# import board
# import busio
import displayio
# from rtc import RTC

from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect

import cc_util

# CONFIGURABLE SETTINGS ----------------------------------------------------

#TWELVE_HOUR = True # If set, use 12-hour time vs 24-hour (e.g. 3:00 vs 15:00)
#COUNTDOWN = False  # If set, show time to (vs time of) next rise/set event
#BITPLANES = 6      # Ideally 6, but can set lower if RAM is tight


# SOME UTILITY FUNCTIONS AND CLASSES ---------------------------------------



# pylint: disable=too-few-public-methods
class MoonData():
    """ Class holding lunar data for a given day (00:00:00 to 23:59:59).
        App uses two of these -- one for the current day, and one for the
        following day -- then some interpolations and such can be made.
        Elements include:
        age      : Moon phase 'age' at midnight (start of period)
                   expressed from 0.0 (new moon) through 0.5 (full moon)
                   to 1.0 (next new moon).
        midnight : Epoch time in seconds @ midnight (start of period).
        rise     : Epoch time of moon rise within this 24-hour period.
        set      : Epoch time of moon set within this 24-hour period.
    """
    def __init__(self, datetime, hours_ahead, utc_offset, cc_state, lat, lon):
        """ Initialize MoonData object elements (see above) from a
            time.struct_time, hours to skip ahead (typically 0 or 24),
            and a UTC offset (as a string) and a query to the MET Norway
            Sunrise API (also provides lunar data), documented at:
            https://api.met.no/weatherapi/sunrise/2.0/documentation
        """
        if hours_ahead:
            # Can't change attribute in datetime struct, need to create
            # a new one which will roll the date ahead as needed. Convert
            # to epoch seconds and back for the offset to work
            datetime = time.localtime(time.mktime(time.struct_time(
                datetime.tm_year,
                datetime.tm_mon,
                datetime.tm_mday,
                datetime.tm_hour + hours_ahead,
                datetime.tm_min,
                datetime.tm_sec,
                -1, -1, -1)))
        # strftime() not available here

        url = ('https://api.met.no/weatherapi/sunrise/2.0/.json?lat=' +
               str(lat) + '&lon=' + str(lon) +
               '&date=' + str(datetime.tm_year) + '-' +
               '{0:0>2}'.format(datetime.tm_mon) + '-' +
               '{0:0>2}'.format(datetime.tm_mday) +
               '&offset=' + utc_offset)
        print('Fetching moon data via', url)
        # pylint: disable=bare-except
        for _ in range(5): # Retries
            try:
                full_data = json.loads(cc_state['network'].fetch_data(url))
                moon_data = full_data['location']['time'][0]
                print(moon_data)
                # Reconstitute JSON data into the elements we need
                self.age = float(moon_data['moonphase']['value']) / 100
                self.midnight = time.mktime(parse_time(
                    moon_data['moonphase']['time']))
                if 'moonrise' in moon_data:
                    self.rise = time.mktime(
                        parse_time(moon_data['moonrise']['time']))
                else:
                    self.rise = None
                if 'moonset' in moon_data:
                    self.set = time.mktime(
                        parse_time(moon_data['moonset']['time']))
                else:
                    self.set = None
                return # Success!
            except:
                # Moon server error (maybe), try again after 15 seconds.
                # (Might be a memory error, that should be handled different)
                print("MoonData fetch error!")
                time.sleep(15)
                print("MoonData fetch retry....")

CC_blockID = ""
CC_blockData = {
}

# ONE-TIME INITIALIZATION --------------------------------------------------
def cc_init(cc_state):
    #MATRIX = Matrix(bit_depth=BITPLANES)
    #DISPLAY = MATRIX.display
    # LARGE_FONT = bitmap_font.load_font('/fonts/helvB12.bdf')
    # SMALL_FONT = bitmap_font.load_font('/fonts/helvR10.bdf')
    
    # LARGE_FONT.load_glyphs('0123456789:')
    # SMALL_FONT.load_glyphs('0123456789:/.%')

    grp_moon = displayio.Group(max_size=2)
    rect = Rect(0,0,32,32,fill=0x000010, outline=0x111111)
    grp_moon.append(rect)

    # Display group is set up once, then we just shuffle items around later.
    # Order of creation here determines their stacking order.
    # GROUP = displayio.Group(max_size=10)
    # Element 0 is a stand-in item, later replaced with the moon phase bitmap
    # pylint: disable=bare-except
    #rot = cc_state['config']['rotation']
    #try:
    #    FILENAME = 'BPMs/32/moon/splash-' + str(rot) + '.bmp'
    #    BITMAP = displayio.OnDiskBitmap(open(FILENAME, 'rb'))
    #    TILE_GRID = displayio.TileGrid(BITMAP,
    #                               pixel_shader=displayio.ColorConverter(),)
    #    GROUP.append(TILE_GRID)
    #except:
    #    GROUP.append(adafruit_display_text.label.Label(SMALL_FONT, color=0xFF0000,
    #                                               text='AWOO'))
    #    GROUP[0].x = (DISPLAY.width - GROUP[0].bounding_box[2] + 1) // 2
    #    GROUP[0].y = DISPLAY.height // 2 - 1
    # Elements 1-4 are an outline around the moon percentage -- text labels
    # offset by 1 pixel up/down/left/right. Initial position is off the matrix,
    # updated on first refresh. Initial text value must be long enough for
    # longest anticipated string later.
    #for i in range(4):
    #    GROUP.append(adafruit_display_text.label.Label(SMALL_FONT, color=0,
    #                                                   text='99.9%', y=-99))
    # Element 5 is the moon percentage (on top of the outline labels)
    #GROUP.append(adafruit_display_text.label.Label(SMALL_FONT, color=0xFFFF00,
    #                                               text='99.9%', y=-99))
    # Element 6 is the current time
    #GROUP.append(adafruit_display_text.label.Label(LARGE_FONT, color=0x808080,
    #                                                text='12:00', y=-99))
    # Element 7 is the current date
    #GROUP.append(adafruit_display_text.label.Label(SMALL_FONT, color=0x808080,
    #                                           text='12/31', y=-99))
    # Element 8 is a symbol indicating next rise or set
    #GROUP.append(adafruit_display_text.label.Label(SYMBOL_FONT, color=0x00FF00,
    #                                             text='x', y=-99))
    # Element 9 is the time of (or time to) next rise/set event
    #GROUP.append(adafruit_display_text.label.Label(SMALL_FONT, color=0x00FF00,
    #                                               text='12:00', y=-99))
    #DISPLAY.show(GROUP)

    #NETWORK = Network(status_neopixel=board.NEOPIXEL, debug=False)
    #NETWORK.connect()

    # LATITUDE, LONGITUDE, TIMEZONE are set up once, constant over app lifetime

    # Fetch latitude/longitude from secrets.py. If not present, use
    # IP geolocation. This only needs to be done once, at startup!
    #try:
    #    LATITUDE = secrets['latitude']
    #    LONGITUDE = secrets['longitude']
    #    print('Using stored geolocation: ', LATITUDE, LONGITUDE)
    #except KeyError:
    #    LATITUDE, LONGITUDE = (
    #        NETWORK.fetch_data('http://www.geoplugin.net/json.gp',
    #                           json_path=[['geoplugin_latitude'],
    #                                      ['geoplugin_longitude']]))
    #    print('Using IP geolocation: ', LATITUDE, LONGITUDE)

    # Load time zone string from secrets.py, else IP geolocation for this too
    # (http://worldtimeapi.org/api/timezone for list).
    #try:
    #    TIMEZONE = secrets['timezone'] # e.g. 'America/New_York'
    #except:
    #    TIMEZONE = None # IP geolocation

    # Set initial clock time, also fetch initial UTC offset while
    # here (NOT stored in secrets.py as it may change with DST).
    # pylint: disable=bare-except
    #try:
    #    DATETIME, UTC_OFFSET = update_time(TIMEZONE)
    #except:
    #    DATETIME, UTC_OFFSET = time.localtime(), '+00:00'
    #LAST_SYNC = time.mktime(DATETIME)

    # Poll server for moon data for current 24-hour period and +24 ahead
    #PERIOD = []
    #for DAY in range(2):
    #    PERIOD.append(MoonData(DATETIME, DAY * 24, UTC_OFFSET))
    # PERIOD[0] is the current 24-hour time period we're in. PERIOD[1] is the
    # following 24 hours. Data is shifted down and new data fetched as days
    # expire. Thought we might need a PERIOD[2] for certain circumstances but
    # it appears not, that's changed easily enough if needed.
    return grp_moon


# MAIN LOOP ----------------------------------------------------------------
def cc_update(cc_state):
    #gc.collect()
    now = time.time() # Current epoch time in seconds

    # Sync with time server every ~2 hours
    #if NOW - LAST_SYNC > 2 * 60 * 60:
    #    try:
    #        DATETIME, UTC_OFFSET = update_time(TIMEZONE)
    #        LAST_SYNC = time.mktime(DATETIME)
    #        continue # Time may have changed; refresh NOW value
    #    except:
            # update_time() can throw an exception if time server doesn't
            # respond. That's OK, keep running with our current time, and
            # push sync time ahead to retry in 30 minutes (don't overwhelm
            # the server with repeated queries).
    #        LAST_SYNC += 30 * 60 # 30 minutes -> seconds

    # If PERIOD has expired, move data down and fetch new +24-hour data
    if NOW >= PERIOD[1].midnight:
        PERIOD[0] = PERIOD[1]
        PERIOD[1] = MoonData(time.localtime(), 24, UTC_OFFSET)

    # Determine weighting of tomorrow's phase vs today's, using current time
    RATIO = ((NOW - PERIOD[0].midnight) /
             (PERIOD[1].midnight - PERIOD[0].midnight))
    # Determine moon phase 'age'
    # 0.0  = new moon
    # 0.25 = first quarter
    # 0.5  = full moon
    # 0.75 = last quarter
    # 1.0  = new moon
    if PERIOD[0].age < PERIOD[1].age:
        AGE = (PERIOD[0].age +
               (PERIOD[1].age - PERIOD[0].age) * RATIO) % 1.0
    else: # Handle age wraparound (1.0 -> 0.0)
        # If tomorrow's age is less than today's, it indicates a new moon
        # crossover. Add 1 to tomorrow's age when computing age delta.
        AGE = (PERIOD[0].age +
               (PERIOD[1].age + 1 - PERIOD[0].age) * RATIO) % 1.0

    # AGE can be used for direct lookup to moon bitmap (0 to 99) -- these
    # images are pre-rendered for a linear timescale (solar terminator moves
    # nonlinearly across sphere).
    FRAME = int(AGE * 100) % 100 # Bitmap 0 to 99

    # Then use some trig to get percentage lit
    if AGE <= 0.5: # New -> first quarter -> full
        PERCENT = (1 - math.cos(AGE * 2 * math.pi)) * 50
    else:          # Full -> last quarter -> new
        PERCENT = (1 + math.cos((AGE - 0.5) * 2 * math.pi)) * 50

    # Find next rise/set event, complicated by the fact that some 24-hour
    # periods might not have one or the other (but usually do) due to the
    # Moon rising ~50 mins later each day. This uses a brute force approach,
    # working backwards through the time periods to locate rise/set events
    # that A) exist in that 24-hour period (are not None), B) are still in
    # the future, and C) are closer than the last guess. What's left at the
    # end is the next rise or set (and the inverse of the event type tells
    # us whether Moon's currently risen or not).
    NEXT_EVENT = PERIOD[1].midnight + 100000 # Force first match
    for DAY in reversed(PERIOD):
        if DAY.rise and NEXT_EVENT >= DAY.rise >= NOW:
            NEXT_EVENT = DAY.rise
            RISEN = False
        if DAY.set and NEXT_EVENT >= DAY.set >= NOW:
            NEXT_EVENT = DAY.set
            RISEN = True

    if DISPLAY.rotation in (0, 180): # Horizontal 'landscape' orientation
        CENTER_X = 48      # Text along right
        MOON_Y = 0         # Moon at left
        TIME_Y = 6         # Time at top right
        EVENT_Y = 26       # Rise/set at bottom right
    else:                  # Vertical 'portrait' orientation
        CENTER_X = 16      # Text down center
        if RISEN:
            MOON_Y = 0     # Moon at top
            EVENT_Y = 38   # Rise/set in middle
            TIME_Y = 49    # Time/date at bottom
        else:
            TIME_Y = 6     # Time/date at top
            EVENT_Y = 26   # Rise/set in middle
            MOON_Y = 32    # Moon at bottom

    print()

    # Update moon image (GROUP[0])
    FILENAME = '/BMPs/32/moon/moon' + '{0:0>2}'.format(FRAME) + '.bmp'
    BITMAP = displayio.OnDiskBitmap(open(FILENAME, 'rb'))
    TILE_GRID = displayio.TileGrid(BITMAP,
                                   pixel_shader=displayio.ColorConverter(),)
    TILE_GRID.x = 0
    TILE_GRID.y = MOON_Y
    GROUP[0] = TILE_GRID

    # Update percent value (5 labels: GROUP[1-4] for outline, [5] for text)
    if PERCENT >= 99.95:
        STRING = '100%'
    else:
        STRING = '{:.1f}'.format(PERCENT + 0.05) + '%'
    print(NOW, STRING, 'full')
    # Set element 5 first, use its size and position for setting others
    GROUP[5].text = STRING
    GROUP[5].x = 16 - GROUP[5].bounding_box[2] // 2
    GROUP[5].y = MOON_Y + 16
    for _ in range(1, 5):
        GROUP[_].text = GROUP[5].text
    GROUP[1].x, GROUP[1].y = GROUP[5].x, GROUP[5].y - 1 # Up 1 pixel
    GROUP[2].x, GROUP[2].y = GROUP[5].x - 1, GROUP[5].y # Left
    GROUP[3].x, GROUP[3].y = GROUP[5].x + 1, GROUP[5].y # Right
    GROUP[4].x, GROUP[4].y = GROUP[5].x, GROUP[5].y + 1 # Down

    # Update next-event time (GROUP[8] and [9])
    # Do this before time because we need uncorrupted NOW value
    EVENT_TIME = time.localtime(NEXT_EVENT) # Convert to struct for later
    if COUNTDOWN: # Show NEXT_EVENT as countdown to event
        NEXT_EVENT -= NOW # Time until (vs time of) next rise/set
        MINUTES = NEXT_EVENT // 60
        STRING = str(MINUTES // 60) + ':' + '{0:0>2}'.format(MINUTES % 60)
    else: # Show NEXT_EVENT in clock time
        STRING = hh_mm(EVENT_TIME)
    GROUP[9].text = STRING
    XPOS = CENTER_X - (GROUP[9].bounding_box[2] + 6) // 2
    GROUP[8].x = XPOS
    if RISEN:                    # Next event is SET
        GROUP[8].text = '\u21A7' # Downwards arrow from bar
        GROUP[8].y = EVENT_Y - 2
        print('Sets:', STRING)
    else:                        # Next event is RISE
        GROUP[8].text = '\u21A5' # Upwards arrow from bar
        GROUP[8].y = EVENT_Y - 1
        print('Rises:', STRING)
    GROUP[9].x = XPOS + 6
    GROUP[9].y = EVENT_Y
    # Show event time in green if a.m., amber if p.m.
    GROUP[8].color = GROUP[9].color = (0x00FF00 if EVENT_TIME.tm_hour < 12
                                       else 0xC04000)

    # Update time (GROUP[6]) and date (GROUP[7])
    #NOW = time.localtime()
    #STRING = hh_mm(NOW)
    #GROUP[6].text = STRING
    #GROUP[6].x = CENTER_X - GROUP[6].bounding_box[2] // 2
    #GROUP[6].y = TIME_Y
    #STRING = str(NOW.tm_mon) + '/' + str(NOW.tm_mday)
    #GROUP[7].text = STRING
    #GROUP[7].x = CENTER_X - GROUP[7].bounding_box[2] // 2
    #GROUP[7].y = TIME_Y + 10

    #DISPLAY.refresh() # Force full repaint (splash screen sometimes sticks)
    # time.sleep(5)
