

"""
Based on ISO 8601-2004
"""

import datetime
import re

# FIXME: Year expansions are not supported due to python datetime limitations


DATE_EXPRESSION = \
    re.compile(
        r'(?P<year>((\d{4})|(\d{2})))'
        r'(?P<not_year>(?P<sep1>\-)?(?P<month>\d{2})((?P<sep2>\-)?'
        r'(?P<day>\d{2}))?)?$'
        )

DATE_ORDINAL_EXPRESSION = \
    re.compile(
        r'(?P<year>\d{4})(?P<sep>\-)?(?P<day>\d{3})$'
        )

DATE_WEEK_EXPRESSION = \
    re.compile(
        r'(?P<year>\d{4})(?P<sep1>\-)?'
        r'W(?P<week>\d{2})((?P<sep2>\-)?(?P<day>\d{1}))?$'
        )

TIME_EXPRESSION = \
    re.compile(
        r'^(?P<T>T)?(?P<hour>\d{2})((?P<sep1>\:)?(?P<min>\d{2})((?P<sep2>\:)?'
        r'(?P<sec>\d{2}))?)?'
        r'((?P<fract_del>[\.\,])(?P<fract>\d+))?'
        r'(?P<tz>'
        r'(Z|(?P<tz_sign>[+-])(?P<tz_h>\d{2})(?P<sep3>\:)?(?P<tz_m>\d{2})))?'
        r'$'
        )

DATE_ATTRIBUTES = {
    '-', 'year', 'century', 'week', 'ordinal', 'day', 'month'
    }
TIME_ATTRIBUTES = {
    'hour', 'min', 'sec', 'fract', 'tz_h', 'tz_m', 'fract_del',
    'T', ':', '+', '-', 'local', 'utc', ',', '.'
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


def time_str_to_time(value):

    _debug = True

    ret = None
    ret_attributes = set()

    res = TIME_EXPRESSION.match(value)

    if res == None:
        pass
    else:
        groupdict = res.groupdict()
        separator_error = False
        separator = groupdict['sep1']

        if groupdict['T'] == 'T':
            ret_attributes.add('T')

        if separator == ':':
            ret_attributes.add(':')

        if (groupdict['sec'] != None
            and groupdict['sep2'] != separator):
            separator_error = True

        if (groupdict['tz_m'] != None
            and groupdict['sep3'] != separator):
            separator_error = True

        if groupdict['fract_del'] != None:
            ret_attributes.add(groupdict['fract_del'])

        for i in ['hour', 'min', 'sec', 'fract', 'tz_h', 'tz_m']:
            if groupdict[i] != None:
                ret_attributes.add(i)

        if groupdict['fract'] != None:
            fract = int(groupdict['fract'])

            # TODO: simplification needed
            if groupdict['min'] == None:
                minute = float(60 * float('0.{}'.format(fract)))
                groupdict['min'] = str(int(minute))
                fract = int(str(minute).split('.')[1])
                second = float(60 * float('0.{}'.format(fract)))
                groupdict['sec'] = str(int(second))
                groupdict['fract'] = str(int(str(second).split('.')[1]))

            if groupdict['sec'] == None:
                second = float(60 * float('0.{}'.format(fract)))
                groupdict['sec'] = str(int(second))
                groupdict['fract'] = str(int(str(second).split('.')[1]))

            if _debug:
                print("After fract translations:\n{}".format(groupdict))

        for i in ['hour', 'min', 'sec', 'fract', 'tz_h', 'tz_m']:
            if groupdict[i] == None:
                groupdict[i] = '00'

        if groupdict['tz_sign'] == None:
            groupdict['tz_sign'] = '+'
        else:
            ret_attributes.add(groupdict['tz_sign'])

        if separator_error:
            pass
        else:
            z = None
            if groupdict['tz'] == None:
                ret_attributes.add('local')
                z = None
            elif groupdict['tz'] == 'Z':
                ret_attributes.add('utc')
                z = datetime.timezone.utc
            else:
                ret_attributes.add('utc')
                z = gen_tz(
                    int(groupdict['tz_h']),
                    int(groupdict['tz_m']),
                    groupdict['tz_sign'] == '+'
                    )

            ret = datetime.time(
                int(groupdict['hour']),
                int(groupdict['min']),
                int(groupdict['sec']),
                int(groupdict['fract']),
                z
                )

            _time_attrs_check(ret_attributes)

    return ret, ret_attributes


def gen_tz(h, m, plus=True):

    td = datetime.timedelta(hours=h, minutes=m)
    if not plus:
        td = -td

    tz = datetime.timezone(td)

    return tz


def test_date():

    for i in [
        '19850412',
        '1985-04-12',
        '1985-04',
        '1985',
        '19',
#        '+0019850412',
#        '+001985-04-12',
#        '+001985-04',
#        '+001985',
#        '+0019',
        '1985102',
        '-1985102',
        '1985-102',
        '1985W155',
        '1985-W15-5',
        '1985W15',
        '1985-W15',
#        '+001985W155',
#        '+001985-W15-5',
#        '+001985W15',
#        '+001985-W15'
        ]:

        print(i)

        res = str_to_date(i)

        if res == None:
            print("'{}' not matches".format(i))
        else:
            print(repr(res))

        print()

    return


def test_time():

    for i in [
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
        '23,3'
        ]:

        print(i)

        res = time_str_to_time(i)

        if res == None:
            print("'{}' not matches".format(i))
        else:
            print(repr(res))

        print()

    return
