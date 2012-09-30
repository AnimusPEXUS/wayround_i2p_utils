
import datetime

def currenttime_stamp():
    d = datetime.datetime.now()
    return time_stamp(d)

def time_stamp(dt):
    return '{year:04d}{month:02d}{day:02d}.{hour:02d}{minute:02d}{second:02d}.{micro:07d}'.format_map(
        {
            'year'      : dt.year,
            'month'     : dt.month,
            'day'       : dt.day,
            'hour'      : dt.hour,
            'minute'    : dt.minute,
            'second'    : dt.second,
            'micro'     : dt.microsecond
            }
        )

