
"""
Based on RFC5322 - Internet Message Format
Note the time line:
    rfc822
       v
    rfc2822
       v
    rfc5322
"""


import regex
import datetime
import pytz

import wayround_org.utils.datetime_iso8601


DATE_EXPRESSION = (
    r'\s*'
    r'(?P<day>\d+)'
    r'\s+'
    r'(?P<month>[a-zA-Z]{3})'
    r'\s+'
    r'(?P<year>\d+)'
    r'\s*'
    )

TIMEOFDAY_EXPRESSION = (
    r'\s*'
    r'(?P<hour>\d+)'
    r'\:(?P<minute>\d+)'
    r'(\:(?P<second>\d+))?'
    r'\s*'
    )

ZONE_EXPRESSION = (
    r'\s*'
    r'('
    r'('
    r'(?P<zone_sign>[+-]?)'
    r'(?P<zone_val>(?P<zone_hours>\d{2})(?P<zone_minutes>\d{2}))'
    r')'
    r'|'
    r'(?P<obs_zone>' +
    (r'UT|GMT|EST|EDT|CST|CDT|MST|MDT|PST|PDT' +
     r'|[\x{:x}-\x{:x}]'.format(65, 73) +
     r'|[\x{:x}-\x{:x}]'.format(75, 90) +
     r'|[\x{:x}-\x{:x}]'.format(97, 105) +
     r'|[\x{:x}-\x{:x}]'.format(107, 122)
     ) +
    r')'
    r')'
    r'\s*'
    )

TIME_EXPRESSION = (
    r'\s*'
    r'(?P<timeofday>{timeofday})'
    r'\s+'
    r'(?P<zone>{zone})'
    r'\s*'.format(
        timeofday=TIMEOFDAY_EXPRESSION,
        zone=ZONE_EXPRESSION
        )
    )

DATETIME_EXPRESSION = (
    r'\s*'
    r'((?P<dayofweek>[a-zA-Z]{{3}})\,)?'
    r'\s+'
    r'(?P<date>{date})'
    r'\s+'
    r'(?P<time>{time})'
    r'\s*'
    r'').format(
    date=DATE_EXPRESSION,
    time=TIME_EXPRESSION
    )


DATETIME_EXPRESSION_C = regex.compile(DATETIME_EXPRESSION)

MONTHES = [
    "Jan", "Feb", "Mar", "Apr",
    "May", "Jun", "Jul", "Aug",
    "Sep", "Oct", "Nov", "Dec"
    ]


DAYSOFWEEK = [
    "Mon", "Tue", "Wed", "Thu",
    "Fri", "Sat", "Sun"
    ]


def check_datetime_has_tzinfo(value):
    if not hasattr(value, 'tzinfo') or value.tzinfo is None:
        raise ValueError("supplied datetime must have time zone info")
    return


def match_DATETIME_EXPRESSION_C(value):
    return DATETIME_EXPRESSION_C.match(value)


def str_to_datetime(value, already_parsed=None):
    """
    Parse string and make datetime.datetime of it

    if already_parsed is not None - value is ignored.
    already_parsed - presumed to be result of match_DATETIME_EXPRESSION_C()
    """

    ret = None
    ret_attributes = set()

    if already_parsed is None:

        if not isinstance(value, str):
            raise TypeError("`value' must be inst of str")

        re_res = DATETIME_EXPRESSION_C.match(value)

    else:
        re_res = already_parsed

    if re_res:

        month = MONTHES.index(re_res.group('month')) + 1

        second = re_res.group('second')
        if second is None:
            second = 0
        else:
            second = int(second)
            ret_attributes.add('second')

        obs_zone = re_res.group('obs_zone')
        if obs_zone is not None:
            if obs_zone not in pytz.all_timezones:
                raise Exception(
                    "zone name `{}' not supported by pytz".format(obs_zone)
                    )
            tzinfo = pytz.timezone(obs_zone)
        else:

            zonesign = '+'
            if re_res.group('zone_sign') == '-':
                zonesign = '-'

            tzinfo = wayround_org.utils.datetime_iso8601.gen_tz(
                int(re_res.group('zone_hours')),
                int(re_res.group('zone_minutes')),
                plus=zonesign == '+'
                )

        result = datetime.datetime(
            year=int(re_res.group('year')),
            month=month,
            day=int(re_res.group('day')),
            hour=int(re_res.group('hour')),
            minute=int(re_res.group('minute')),
            second=second,
            tzinfo=tzinfo
            )

        if re_res.group('dayofweek') is not None:
            ret_attributes.add('dayofweek')

        ret = result

    return ret, ret_attributes


def datetime_to_str(value, attrs=None):

    if not isinstance(value, datetime.datetime):
        raise TypeError("`value' must be inst of datetime.datetime")

    check_datetime_has_tzinfo(value)

    if attrs is None:
        attrs = set(['dayofweek', 'second'])

    dayofweek = ''
    if 'dayofweek' in attrs:
        dayofweek = '{}, '.format(DAYSOFWEEK[value.date().weekday()])

    second = ''
    if 'second' in attrs:
        second = ':{:02d}'.format(value.second)

    month = MONTHES[value.month - 1]

    zone = wayround_org.utils.datetime_iso8601.format_tz(
        value.tzinfo,
        sep=False
        )

    ret = (
        '{dayofweek}'
        '{day:02d} {month} {year:04d} '
        '{hour:02d}:{minute:02d}{second} {zone}'
        ).format(
            dayofweek=dayofweek,
            day=value.day,
            month=month,
            year=value.year,
            hour=value.hour,
            minute=value.minute,
            second=second,
            zone=zone
            )

    return ret


def str_parse_test():
    """
    run tests if datetime string parser
    """

    tests = [
        'Fri, 29 Jan 2016 13:36:08 +0200',
        'Sun, 06 Nov 1994 08:49:37 GMT'  # from rfc7231
        ]

    for value in tests:

        print("test subject: {}".format(value))

        re_res = DATETIME_EXPRESSION_C.match(value)

        if re_res:

            for i in [
                    'dayofweek',
                    'day', 'month', 'year',
                    'hour', 'minute', 'second',
                    'zone_sign', 'zone_val',
                    'zone_hours', 'zone_minutes']:
                print("    {:20}: {}".format(i, re_res.group(i)))

            dt, attrs = str_to_datetime(value)

            print(
                "    {:20}: {}".format(
                    'iso8601',
                    wayround_org.utils.datetime_iso8601.datetime_to_str(
                        dt
                        )
                    )
                )

            print(
                "    {:20}: {}".format(
                    'rendered',
                    datetime_to_str(
                        dt
                        )
                    )
                )
        else:
            print("    parse error")
    return
