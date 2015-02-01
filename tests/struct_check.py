
from wayround_org.utils.types import struct_check
from lxml.etree import Element, _Element


for i in [
        ('', {'t': str}),
        (1, {'t': str}),
        (1, {'t': int}),
        ([], {'t': list}),
        ([1, 2, 3, 4], {'t': list, '.': {'t': str}}),
        ([1, 2, 3, 4], {'t': list, '.': {'t': int}}),
        (['1', '2', '3', '4'], {'t': list, '.': {'t': str}}),
        (['1', 2, '3', '4'], {'t': list, '.': {'t': str}}),
        ([Element('a'), Element('b')], {'t': list, '.': {'t': _Element}}),
        ([dict('')], {'t': dict, '{}':{'name':{'t':list, '.': {'t':str}}, 'value': {'t': list, '.': {'t': int}}}}),
        ({'name':['1', '2', '3', '4'], 'value': [1, 2, 3, 4]},
         {'t': dict, '{}':{'name':{'t':list, '.': {'t':str}}, 'value': {'t': list, '.': {'t': int}}}}),
        ({'name':['1', 2, '3', '4'], 'value': [1, 2, 3, 4]},
         {'t': dict, '{}':{'name':{'t':list, '.': {'t':str}}, 'value': {'t': list, '.': {'t': int}}}}),
        ([1, '2', '3'], {'t':'Sequence', '.': {'t': str}}),
        (['1', '2', '3'], {'t':'Sequence', '.': {'t': str}}),
]:
    print(repr(i))
    print(struct_check(i[0], i[1]))
    print('')
