#!/usr/bin/python3

import mmap
import pprint

import org.wayround.utils.format.elf

f = open('/bin/cp', 'rb')


m = mmap.mmap(f.fileno(), 0, flags = mmap.MAP_PRIVATE, prot = mmap.PROT_READ)

r = org.wayround.utils.format.elf.read_elf(m)

m.close()
f.close()

pprint.pprint(r, indent = 4)

org.wayround.utils.format.elf.legend(r)

print("closed?: {}".format(f.closed))
