
import datetime
import wayround_org.utils.datetime_iso8601

TIMESTAMP_STR_FORMAT_PATTERN = \
    '{year:04d}{month:02d}{day:02d}.' \
    '{hour:02d}{minute:02d}{second:02d}.' \
    '{micro:07d}'


TIMESTAMP_RE_PATTERN = \
    r'(?Pyear\d{4})(?Pmonth\d{2})(?Pday\d{2})' \
    r'\.(?Phour\d{2})(?Pminute\d{2})(?Psecond\d{2})\.(?Pmicro\d{7})'


TIMESTAMP2_STR_FORMAT_PATTERN = \
    '{year:04d}{month:02d}{day:02d}' \
    '{hour:02d}{minute:02d}{second:02d}' \
    '{micro:07d}'

TIMESTAMP2_RE_PATTERN = \
    r'(?Pyear\d{4})(?Pmonth\d{2})(?Pday\d{2})' \
    r'(?Phour\d{2})(?Pminute\d{2})(?Psecond\d{2})(?Pmicro\d{7})'


def currenttime_stamp():
    d = datetime.datetime.now()
    return time_stamp(d)


current_timestamp = currenttime_stamp


def time_stamp(dt):
    return TIMESTAMP_STR_FORMAT_PATTERN.format_map(
        {
            'year': dt.year,
            'month': dt.month,
            'day': dt.day,
            'hour': dt.hour,
            'minute': dt.minute,
            'second': dt.second,
            'micro': dt.microsecond
            }
        )


def currenttime_stamp_iso8601():
    d = datetime.datetime.now()
    return time_stamp_iso8601(d)


def currenttime_stamp_iso8601_utc():
    d = datetime.datetime.utcnow()
    return time_stamp_iso8601(d)


def time_stamp_iso8601(dt):
    return wayround_org.utils.datetime_iso8601.datetime_to_str(dt)
