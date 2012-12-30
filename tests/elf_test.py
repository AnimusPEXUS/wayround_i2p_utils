#!/usr/bin/python3

import mmap
import sys

import org.wayround.utils.format.elf as elf

f = open('/bin/cp', 'rb')


m = mmap.mmap(f.fileno(), 0, flags=mmap.MAP_PRIVATE, prot=mmap.PROT_READ)

print("is elf?: {}".format(elf.is_elf(m)))

e_ident = elf.read_e_ident(m)

bitness = elf.e_ident_bitness(e_ident)

print("({}-bit)".format(bitness))

e_ident_dict = elf.e_ident_to_dict(e_ident)

print(elf.e_ident_format(e_ident_dict))

elf_ehdr = elf.read_elf_ehdr(m, 0, e_ident)

elf_ehdr_dict = elf.elf_ehdr_to_dict(m, 0, e_ident)

print(elf.elf_x_ehdr_format(elf_ehdr_dict))

section_table = elf.read_elf_section_header_table(
    m, e_ident_dict, elf_ehdr_dict
    )

print("section table:")
print(
    elf.section_header_table_format(m, section_table, elf_ehdr_dict)
    )

section_names = elf.read_elf_section_header_table_names(
    m, section_table, elf_ehdr_dict
    )

program_table = elf.read_elf_program_header_table(
    m, e_ident_dict, elf_ehdr_dict
    )

print("program table:")
print(
    elf.program_header_table_format(program_table)
    )

dyn_sect_index = section_names.index('.dynamic')

dyn_sect_offset = int.from_bytes(section_table[dyn_sect_index]['sh_offset'], sys.byteorder)

dyn_sect = elf.read_dynamic_section(m, dyn_sect_offset, bitness)

print("dyn_sect")
print(elf.dynamics_format(dyn_sect))
#print("names: \n{}".format(section_names))

libs = elf.get_dynamic_libs_names(
    m, program_table, dyn_sect, section_table, elf_ehdr_dict
    )

print("libs:")
print(repr(libs))

#print("e_ident_dict:   {}".format(e_ident_dict))
#
#elfx_ehdr = elf.read_Elfx_Ehdr(m, e_ident)
#
#print(elf.elf_x_ehdr_format(elfx_ehdr))
#
#section_header_table = elf.read_section_header_table(m, e_ident, elfx_ehdr)
#program_header_table = elf.read_program_header_table(m, e_ident, elfx_ehdr)
#dynamic_section = elf.read_dynamic_section(data, e_ident, elfx_ehdr, section_header_table)
#
#print("Section header table:\n{}".format(elf.section_header_table_format(section_header_table, m, elfx_ehdr)))
#print("Program header table:\n{}".format(elf.program_header_table_format(program_header_table)))
#print(repr(dynamic_section))


m.close()
f.close()
