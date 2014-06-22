

"""
Based on ISO 8601-2004
Partially supported truncated dates and times
"""

import datetime
import re

# FIXME: Year expansions are not supported due to python datetime limitations


DATE_EXPRESSION = \
    re.compile(
        r'^'
        r'(?P<year>((\d{4})|(\d{2})))'
        r'(?P<not_year>(?P<sep1>\-)?(?P<month>\d{2})((?P<sep2>\-)?'
        r'(?P<day>\d{2}))?)?'
        r'$'
        )

DATE_TRUNCATED_EXPRESSION = \
    re.compile(
        r'^'
        r'--'
        r'((?P<number1>\d{2})|-)(?P<sep>-)?(?P<number2>\d{2})?'
        r'$'
        )

DATE_ORDINAL_EXPRESSION = \
    re.compile(
        r'^'
        r'(?P<year>\d{4})(?P<sep>\-)?(?P<day>\d{3})'
        r'$'
        )

DATE_WEEK_EXPRESSION = \
    re.compile(
        r'^'
        r'(?P<year>\d{4})(?P<sep1>\-)?'
        r'W(?P<week>\d{2})((?P<sep2>\-)?(?P<day>\d{1}))?'
        r'$'
        )

TIME_EXPRESSION = \
    re.compile(
        r'^'
        r'(?P<T>T)?(?P<hour>\d{2})((?P<sep1>\:)?(?P<min>\d{2})((?P<sep2>\:)?'
        r'(?P<sec>\d{2}))?)?'
        r'((?P<fract_sep>[\.\,])(?P<fract>\d+))?'
        r'(?P<tz>'
        r'((?P<Z>Z)|(?P<tz_sign>[+-])(?P<tz_hour>\d{2})(?P<sep3>\:)?'
        r'(?P<tz_min>\d{2})))?'
        r'$'
        )


TIME_TRUNCATED_EXPRESSION = \
    re.compile(
        r'^'
        r'-'
        r'((?P<number1>\d{2})|-)(?P<sep>:)?(?P<number2>\d{2})?'
        r'$'
        )

DATE_ATTRIBUTES = {
    '-', 'year', 'century', 'week', 'ordinal', 'day', 'month', 'truncated_date'
    }
TIME_ATTRIBUTES = {
    'hour', 'min', 'sec', 'fract', 'tz_hour', 'tz_min', 'fract_sep',
    'T', ':', 'local', 'utc', ',', '.', 'Z', 'truncated_time'
    }


def _date_attrs_check(arr):
    for i in arr:
        if not i in DATE_ATTRIBUTES:
            raise ValueError("invalid date attribute `{}'".format(i))
    return


def _time_attrs_check(arr):
    for i in arr:
        if not i in TIME_ATTRIBUTES:
            raise ValueError("invalid time attribute `{}'".format(i))
    return


def str_to_date(value):

    res, attr = date_truncated_str_to_dict(value)
    if res != None:
        ret = res, attr
    else:
        res, attr = date_ordinal_str_to_date(value)
        if res != None:
            ret = res, attr
        else:
            res, attr = date_week_str_to_date(value)
            if res != None:
                ret = res, attr
            else:
                res, attr = date_normal_str_to_date(value)
                if res != None:
                    ret = res, attr
                else:
                    ret = None, None

    return ret


def str_to_time(value):

    if value[0] == '-':
        # TODO: separate this
        ret, ret_attributes = time_truncated_str_to_dict(value)
    else:

        _debug = False

        ret = None
        ret_attributes = set()

        res = TIME_EXPRESSION.match(value)

        if res == None:
            pass
        else:
            groupdict = res.groupdict()
            separator_error = False
            separator = groupdict['sep1']
            microseconds = 0

            if groupdict['T'] == 'T':
                ret_attributes.add('T')

            if separator == ':':
                ret_attributes.add(':')

            if (groupdict['sec'] != None
                and groupdict['sep2'] != separator):
                separator_error = True

            if (groupdict['tz_min'] != None
                and groupdict['sep3'] != separator):
                separator_error = True

            if groupdict['fract_sep'] != None:
                ret_attributes.add(groupdict['fract_sep'])

            for i in ['hour', 'min', 'sec', 'fract', 'tz_hour', 'tz_min']:
                if groupdict[i] != None:
                    ret_attributes.add(i)

            if groupdict['fract'] != None:
                fract = int(groupdict['fract'])

                if groupdict['min'] == None:
                    minute = float(60 * float('0.{}'.format(fract)))
                    groupdict['min'] = str(int(minute))
                    fract = int(str(minute).split('.')[1])

                if groupdict['sec'] == None:
                    second = float(60 * float('0.{}'.format(fract)))
                    groupdict['sec'] = str(int(second))
                    fract = int(str(second).split('.')[1])

                microseconds = round(1000000 * float('0.{}'.format(fract)))

                if _debug:
                    print("After fract translations:\n{}".format(groupdict))
                    print("microseconds = {}".format(microseconds))

            for i in ['hour', 'min', 'sec', 'fract', 'tz_hour', 'tz_min']:
                if groupdict[i] == None:
                    groupdict[i] = '00'

            if groupdict['tz_sign'] == None:
                groupdict['tz_sign'] = '+'

            if separator_error:
                pass
            else:
                z = None
                if groupdict['tz'] == None:
                    ret_attributes.add('local')
                    z = None
                elif groupdict['tz'] == 'Z':
                    ret_attributes.add('Z')
                    ret_attributes.add('utc')
                    z = datetime.timezone.utc
                else:
                    ret_attributes.add('utc')
                    z = gen_tz(
                        int(groupdict['tz_hour']),
                        int(groupdict['tz_min']),
                        groupdict['tz_sign'] == '+'
                        )

                if _debug:
                    print("Setting tz to {}".format(z))

                ret = datetime.time(
                    int(groupdict['hour']),
                    int(groupdict['min']),
                    int(groupdict['sec']),
                    microseconds,
                    tzinfo=z
                    )

                _time_attrs_check(ret_attributes)

    return ret, ret_attributes


def str_to_datetime(value):
    _debug = False
    ret = None
    ret_attributes = set()
    t_index = value.find('T')
    if t_index != -1:
        date_str = value[:t_index]
        time_str = value[t_index:]

        if _debug:
            print(
                "date part: '{}', time part: '{}'".format(date_str, time_str)
                )

        date, d_attrs = str_to_date(date_str)
        time, t_attrs = str_to_time(time_str)

        if _debug:
            if date == None:
                print("Date not parsed")
            if time == None:
                print("Time not parsed")

        if date != None and time != None:

            date_can_have_separators = (
                'month' in d_attrs
                or 'day' in d_attrs
                or 'week' in d_attrs
                )

            time_can_have_separators = (
                'min' in t_attrs
                or 'tz_min' in t_attrs
                )

            separator_error = False

            if date_can_have_separators and time_can_have_separators:
                if '-' in d_attrs and ':' in t_attrs:
                    pass
                else:
                    separator_error = True

            if not separator_error:
                ret = datetime.datetime.combine(date, time)
                ret_attributes = d_attrs | t_attrs

    #else:
    #    res, attr = str_to_date(value)
    #
    #    if res != None:
    #        ret = res

    return ret, ret_attributes


def date_to_str(date, attr=None):

    if attr == None:
        attr = {'year', 'month', 'day'}

    if 'truncated_date' in attr:

        ret = dict_to_truncated_date_str(date, attr)

    elif 'ordinal' in attr:

        cop = datetime.date(date.year, 1, 1)

        year = '{:04d}'.format(date.year)
        day = ''
        sep = ''

        if 'day' in attr and '-' in attr:
            sep = '-'

        if 'day' in attr:
            day = '{:03d}'.format((date - cop).days)

        ret = '{year}{sep}{day}'.format(
            year=year,
            sep=sep,
            day=day
            )

    elif 'week' in attr:

        cop = datetime.date(date.year, 1, 1)
        delta = date - cop
        weeks = int(delta.days / 7)
        days = delta.days - (weeks * 7)
#        days = 7 * float('0.{}'.format(int(str(weeks).split('.')[1])))

        year = '{:04d}'.format(date.year)
        week = '{:02d}'.format(weeks)
        day = ''
        sep1 = ''
        sep2 = ''

        if 'day' in attr:
            day = '{:01d}'.format(int(days))

        if '-' in attr:
            sep1 = '-'

        if 'day' in attr and '-' in attr:
            sep2 = '-'

        ret = '{year}{sep1}W{week}{sep2}{day}'.format(
            year=year,
            week=week,
            day=day,
            sep1=sep1,
            sep2=sep2
            )

    else:

        year = '{:04d}'.format(date.year)
        month = ''
        day = ''
        sep1 = ''
        sep2 = ''

        if 'century' in attr:
            year = year[:-2]

        if 'month' in attr and '-' in attr:
            sep1 = '-'

        if 'month' in attr:
            month = '{:02d}'.format(date.month)

        if 'day' in attr and '-' in attr:
            sep2 = '-'

        if 'day' in attr:
            day = '{:02d}'.format(date.day)

        ret = '{year}{sep1}{month}{sep2}{day}'.format(
            year=year,
            month=month,
            day=day,
            sep1=sep1,
            sep2=sep2
            )

    return ret


def time_to_str(time, attr=None):

    if 'truncated_time' in attr:
        ret = dict_to_truncated_time_str(time, attr)
    else:

        if attr == None:
            attr = {'-', 'hour', 'min', 'sec'}

        t = ''
        if 'T' in attr:
            t = 'T'

        hour = '{:02d}'.format(time.hour)

        fract = 0
        if time.microsecond != 0:
            fract = time.microsecond / 1000000

        second = 0
        if 'sec' in attr:
            second = '{:02d}'.format(time.second)
        else:
    #        second = float('{}.{}'.format(time.second, fract))
            second = float(time.second + fract)
            fract = second / 60
            second = ''

        minute = 0
        if 'min' in attr:
            minute = '{:02d}'.format(time.minute)
        else:
    #        minute = float('{}.{}'.format(time.minute, fract))
            minute = float(time.minute + fract)
            fract = minute / 60
            minute = ''

        fract_sep = ''
        for i in [',', '.']:
            if i in attr:
                fract_sep = i
                break

        sep1 = ''
        if 'min' in attr and ':' in attr:
            sep1 = ':'

        sep2 = ''
        if 'sec' in attr and ':' in attr:
            sep2 = ':'

        if not 'fract' in attr:
            fract = ''
        else:
            fract = '{}'.format(str(fract).split('.')[1])

        tz = format_tz(
            time.tzinfo,
            sep=':' in attr,
            minu='tz_min' in attr,
            zed='Z' in attr
            )

        ret = \
            '{T}{hour}{sep1}{min}{sep2}' \
            '{sec}{fract_sep}{fract}{tz}'.format(
                T=t,
                sep1=sep1,
                sep2=sep2,
                fract_sep=fract_sep,
                hour=hour,
                min=minute,
                sec=second,
                fract=fract,
                tz=tz
                )

    return ret


def datetime_to_str(value, attr):

    date = value.date()
    time = value.timetz()

    date_str = date_to_str(date, attr)
    time_str = time_to_str(time, attr)

    t = ''
    if not time_str[0] == 'T':
        t = 'T'

    ret = '{date}{t}{time}'.format(
        date=date_str,
        time=time_str,
        t=t
        )

    return ret


def date_truncated_str_to_dict(value):

    _debug = False

    ret = None
    ret_attributes = set()

    res = DATE_TRUNCATED_EXPRESSION.match(value)

    if res == None:
        if _debug:
            print("no match")
    else:

        ret = {'month': None, 'day': None}

        ret_attributes.add('truncated_date')
        groupdict = res.groupdict()

        if groupdict['number1'] not in [None, '-']:
            ret_attributes.add('month')
            ret['month'] = int(groupdict['number1'])

        if groupdict['number2'] not in [None]:
            ret_attributes.add('day')
            ret['day'] = int(groupdict['number2'])

        if groupdict['sep'] == '-':
            ret_attributes.add('-')

    return ret, ret_attributes


def time_truncated_str_to_dict(value):

    _debug = False

    ret = None
    ret_attributes = set()

    res = TIME_TRUNCATED_EXPRESSION.match(value)

    if res == None:
        if _debug:
            print("no match")
    else:

        ret = {'min': None, 'sec': None}

        ret_attributes.add('truncated_time')
        groupdict = res.groupdict()

        if groupdict['number1'] not in [None, '-']:
            ret_attributes.add('min')
            ret['min'] = int(groupdict['number1'])

        if groupdict['number2'] not in [None]:
            ret_attributes.add('sec')
            ret['sec'] = int(groupdict['number2'])

        if groupdict['sep'] == ':':
            ret_attributes.add(':')

    return ret, ret_attributes


def date_ordinal_str_to_date(value):

    _debug = False

    ret = None
    ret_attributes = set()

    res = DATE_ORDINAL_EXPRESSION.match(value)

    if res == None:
        if _debug:
            print("no match")
    else:

        groupdict = res.groupdict()
        if _debug:
            print(repr(groupdict))
        separator_error = False
        separator = groupdict['sep']

        for i in ['year', 'day']:
            if groupdict[i] == None:
                groupdict[i] = 1
            else:
                ret_attributes.add(i)

        if separator_error:
            if _debug:
                print("separator error")
        else:

            if separator == '-':
                ret_attributes.add(separator)

            ret_attributes.add('ordinal')

            ret = datetime.date(
                int(groupdict['year']),
                1,
                1
                ) + datetime.timedelta(days=int(groupdict['day']))

            _date_attrs_check(ret_attributes)

    return ret, ret_attributes


def date_week_str_to_date(value):

    _debug = False

    ret = None
    ret_attributes = set()

    res = DATE_WEEK_EXPRESSION.match(value)

    if res == None:
        if _debug:
            print("no match")
    else:

        groupdict = res.groupdict()
        if _debug:
            print(repr(groupdict))
        separator_error = False
        separator = groupdict['sep1']

        if (groupdict['day'] != None
            and groupdict['sep2'] != separator):
            separator_error = True

        for i in ['week', 'day']:
            if groupdict[i] == None:
                groupdict[i] = '01'
            else:
                ret_attributes.add(i)

        for i in ['year']:
            if groupdict[i] == None:
                groupdict[i] = '0001'
            else:
                ret_attributes.add(i)

        if separator_error:
            if _debug:
                print("separator error")
        else:

            ret_attributes.add('week')

            if separator == '-':
                ret_attributes.add(separator)

            ret = datetime.date(
                int(groupdict['year']),
                1,
                1
                ) + datetime.timedelta(
                    days=int(groupdict['day']),
                    weeks=int(groupdict['week'])
                    )
            _date_attrs_check(ret_attributes)

    return ret, ret_attributes


def date_normal_str_to_date(value):

    _debug = False

    ret = None
    ret_attributes = set()

    res = DATE_EXPRESSION.match(value)

    if res == None:
        if _debug:
            print("no match")
    else:

        groupdict = res.groupdict()
        if _debug:
            print(repr(groupdict))
        separator_error = False
        separator = groupdict['sep1']

        if (groupdict['day'] != None
            and groupdict['sep2'] != separator):
            separator_error = True

        if len(groupdict['year']) == 2 and groupdict['not_year'] == None:
            groupdict['year'] += '00'
            ret_attributes.add('century')
        else:
            ret_attributes.add('year')

        for i in ['month', 'day']:
            if groupdict[i] == None:
                groupdict[i] = '01'
            else:
                ret_attributes.add(i)

        if separator_error:
            if _debug:
                print("separator error")
        else:

            if separator == '-':
                ret_attributes.add(separator)

            ret = datetime.date(
                int(groupdict['year']),
                int(groupdict['month']),
                int(groupdict['day'])
                )

            _date_attrs_check(ret_attributes)

    return ret, ret_attributes


def dict_to_truncated_date_str(value, attr):

    day = ''
    if 'day' in attr and value['day'] != None:
        day = '{:02d}'.format(int(value['day']))

    month = ''
    if 'month' in attr and value['month'] != None or value['month'] == '-':
        month = '{:02d}'.format(int(value['month']))

    if not 'month' in attr:
        month = '-'

    sep = ''
    if '-' in attr and day != '' and not month in ['', '-']:
        sep = '-'

    ret = \
        '--{month}{sep}{day}'.format(
            month=month,
            sep=sep,
            day=day
            )

    return ret


def dict_to_truncated_time_str(value, attr):

    sec = ''
    if 'sec' in attr and value['sec'] != None:
        sec = '{:02d}'.format(int(value['sec']))

    minu = ''
    if 'min' in attr and value['min'] != None or value['min'] == '-':
        minu = '{:02d}'.format(int(value['min']))

    if not 'min' in attr:
        minu = '-'

    sep = ''
    if ':' in attr and sec != '' and not minu in ['', '-']:
        sep = ':'

    ret = \
        '-{minu}{sep}{sec}'.format(
            minu=minu,
            sep=sep,
            sec=sec
            )

    return ret


def gen_tz(h, m, plus=True):

    td = datetime.timedelta(hours=h, minutes=m)
    if not plus:
        td = -td

    tz = datetime.timezone(td)

    return tz


def format_tz(value, sep=True, minu=True, zed=False):

    ret = None

    if value == None:
        ret = ''
    else:
        a = value.utcoffset(None)

        if (value == datetime.timezone.utc or a.seconds == 0) and zed == True:
            ret = 'Z'
        else:

            sign = '+'

            if a < datetime.timedelta():
                sign = '-'
                a = -a

            separator = ''
            if sep and minu:
                separator = ':'

            hours = int(a.seconds / 60 / 60)

            minutes = ''
            if minu:
                minutes = int((a.seconds - (hours * 60 * 60)) / 60 / 60)

            ret = '{sign}{hour}{sep}{minute}'.format(
                sign=sign,
                hour='{:02d}'.format(hours),
                sep=separator,
                minute='{:02d}'.format(minutes)
                )

    return ret


def _test(variants, callab, callab2):

    for i in variants:

        print(i)

        res = callab(i)

        if res[0] == None:
            print("'{}' not matches".format(i))
        else:
            print("forward result {}".format(repr(res)))

            res = callab2(res[0], res[1])

            if res == None:
                print("'{}' not matches".format(i))
            else:
                print("reverse result\n{}".format(res))

        print()

    return


def test_date():

    variants = [
        '19850412',
        '1985-04-12',
        '1985-04',
        '1985',
        '19',
        '1985102',
        '-1985102',
        '1985-102',
        '1985W155',
        '1985-W15-5',
        '1985W15',
        '1985-W15',
        '2007-01-25',
        '--0412',
        '--04-12',
        '--04',
        '---12'
        ]

    _test(variants, str_to_date, date_to_str)

    return


def test_time():

    variants = [
        '232050',
        '23:20:50',
        '2320',
        '23:20',
        '23',
        '02:56:15Z',
        '21:56:15-05:00',
        '02:56:15,66Z',
        '21:56:15.99-05:00',
        '215615.99-0500',
        '02:56:15,66Z',
        '02:56,66Z',
        '02,66Z',
        '232050,5',
        '23:20:50,5',
        '2320,8',
        '23:20,8',
        '23,3',
        '12:00:00Z',
        '-2050',
        '-20:50',
        '-20',
        '--50'
        ]

    _test(variants, str_to_time, time_to_str)

    return


def test_datetime():

    variants = [
        '2007-01-25T12:00:00Z'
        ]

    _test(variants, str_to_datetime, datetime_to_str)

    return
