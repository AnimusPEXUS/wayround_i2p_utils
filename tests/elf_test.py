#!/usr/bin/python3

import mmap

import org.wayround.utils.format.elf as elf

f = open('/bin/cp', 'rb')


m = mmap.mmap(f.fileno(), 0, flags=mmap.MAP_PRIVATE, prot=mmap.PROT_READ)

e_ident = elf.read_e_ident(m)

print("is elf?:   {}".format(elf.is_elf(m)))

print("e_ident:   {}".format(repr(e_ident)))

print(elf.e_ident_format(e_ident))

elfx_ehdr = elf.read_Elfx_Ehdr(m, e_ident)

print(elf.elf_x_ehdr_format(elfx_ehdr))

section_header_table = elf.read_section_header_table(m, e_ident, elfx_ehdr)
program_header_table = elf.read_program_header_table(m, e_ident, elfx_ehdr)
dynamic_section = elf.read_dynamic_section(data, e_ident, elfx_ehdr, section_header_table)

print("Section header table:\n{}".format(elf.section_header_table_format(section_header_table, m, elfx_ehdr)))
print("Program header table:\n{}".format(elf.program_header_table_format(program_header_table)))
print(repr(dynamic_section))


m.close()
f.close()
