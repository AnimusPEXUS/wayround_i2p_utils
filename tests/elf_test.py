#!/usr/bin/python3

import mmap
import pprint

import org.wayround.utils.format.elf as elf

f = open('/bin/cp', 'rb')


m = mmap.mmap(f.fileno(), 0, flags=mmap.MAP_PRIVATE, prot=mmap.PROT_READ)

e_ident = elf.read_e_ident(m)

print("is elf?:   {}".format(elf.is_elf(m)))

print("e_ident:   {}".format(repr(e_ident)))
print("Elfx_Ehdr: {}".format(repr(elf.read_Elfx_Ehdr(m))))

elf.e_ident_print(e_ident)

m.close()
f.close()
