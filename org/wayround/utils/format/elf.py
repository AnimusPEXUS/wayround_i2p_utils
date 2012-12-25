
import copy
import sys

import org.wayround.utils.format.elf_bin as elf_bin

def read_e_ident(data):
    return elf_bin.read_e_ident(data)

def is_elf(data):
    return elf_bin.is_elf(data[0:4])

def e_ident_bitness(e_ident):
    return elf_bin.e_ident_bitness(e_ident)

def e_ident_to_dict(data):
    return elf_bin.e_ident_to_dict(data)

def e_ident_format(e_ident_dict):

    ret = """\
Class:       {e_i_s_class}
Data:        {e_i_s_data}
Version:     {e_i_s_version}
OS ABI:      {e_i_s_osabi}
ABI Version: {e_i_s_abiversion}
""".format_map(dict_byte_to_ints(e_ident_dict))

    return ret

def read_elf_ehdr_x(data, index, x):
    return elf_bin.read_elf_ehdr_x(data, index, x)

def read_elf_ehdr(data, index, e_ident):
    return elf_bin.read_elf_ehdr(data, index, e_ident)

def read_elf_shdr_x(data, index, x):
    return elf_bin.read_elf_shdr_x(data, index, x)

def read_elf_shdr(data, index, e_ident):
    return elf_bin.read_elf_shdr(data, index, e_ident)

def elf32_ehdr_to_dict(data, index):
    return elf_bin.elf32_ehdr_to_dict(data, index)

def elf64_ehdr_to_dict(data, index):
    return elf_bin.elf64_ehdr_to_dict(data, index)

def elf_ehdr_to_dict(data, index, e_ident):
    return elf_bin.elf_ehdr_to_dict(data, index, e_ident)

def dict_byte_to_ints(elf_ehdr_dict):

    ret = copy.copy(elf_ehdr_dict)

    for i in ret.keys():
        ret[i] = int.from_bytes(ret[i], sys.byteorder)

    return ret

def elf_x_ehdr_format(elf_ehdr_dict):

    ret = """\
Object file type                     0x{e_type:x}
Architecture                         0x{e_machine:x}
Object file version                  {e_version}
Entry point virtual address          0x{e_entry:08x}
Program header table file offset     0x{e_phoff:08x} ({e_phoff} B)
Section header table file offset     0x{e_shoff:08x} ({e_shoff} B)
Processor-specific flags             b{e_flags:b}
ELF header size in bytes             {e_ehsize} B
Program header table entry size      {e_phentsize} B
Program header table entry count     {e_phnum}
Section header table entry size      {e_shentsize} B
Section header table entry count     {e_shnum}
Section header string table index    {e_shstrndx}
""".format_map(dict_byte_to_ints(elf_ehdr_dict))

    return ret

def get_section_header_type_name(value):

    ret = None

    names = {
        SHT_NULL            :'NULL',
        SHT_PROGBITS        :'PROGBITS',
        SHT_SYMTAB          :'SYMTAB',
        SHT_STRTAB          :'STRTAB',
        SHT_RELA            :'RELA',
        SHT_HASH            :'HASH',
        SHT_DYNAMIC         :'DYNAMIC',
        SHT_NOTE            :'NOTE',
        SHT_NOBITS          :'NOBITS',
        SHT_REL             :'REL',
        SHT_SHLIB           :'SHLIB',
        SHT_DYNSYM          :'DYNSYM',
        SHT_INIT_ARRAY      :'INIT_ARRAY',
        SHT_FINI_ARRAY      :'FINI_ARRAY',
        SHT_PREINIT_ARRAY   :'PREINIT_ARRAY',
        SHT_GROUP           :'GROUP',
        SHT_SYMTAB_SHNDX    :'SYMTAB_SHNDX',
        SHT_NUM             :'NUM',
        SHT_LOOS            :'LOOS',
        SHT_GNU_ATTRIBUTES  :'GNU_ATTRIBUTES',
        SHT_GNU_HASH        :'GNU_HASH',
        SHT_GNU_LIBLIST     :'GNU_LIBLIST',
        SHT_CHECKSUM        :'CHECKSUM',
        SHT_LOSUNW          :'LOSUNW',
        SHT_SUNW_move       :'SUNW_move',
        SHT_SUNW_COMDAT     :'SUNW_COMDAT',
        SHT_SUNW_syminfo    :'SUNW_syminfo',
        SHT_GNU_verdef      :'GNU_verdef',
        SHT_GNU_verneed     :'GNU_verneed',
        SHT_GNU_versym      :'GNU_versym',
        SHT_HISUNW          :'HISUNW',
        SHT_HIOS            :'HIOS',
        SHT_LOPROC          :'LOPROC',
        SHT_HIPROC          :'HIPROC',
        SHT_LOUSER          :'LOUSER',
        SHT_HIUSER          :'HIUSER'
        }

    if value in names:
        ret = names[value]
    else:
        ret = '0x{:x}'.format(value)

    return ret

def get_program_header_type_name(value):

    ret = None

    names = {
        PT_NULL         :'NULL',
        PT_LOAD         :'LOAD',
        PT_DYNAMIC      :'DYNAMIC',
        PT_INTERP       :'INTERP',
        PT_NOTE         :'NOTE',
        PT_SHLIB        :'SHLIB',
        PT_PHDR         :'PHDR',
        PT_TLS          :'TLS',
        PT_NUM          :'NUM',
        PT_LOOS         :'LOOS',
        PT_GNU_EH_FRAME :'GNU_EH_FRAME',
        PT_GNU_STACK    :'GNU_STACK',
        PT_GNU_RELRO    :'GNU_RELRO',
        PT_LOSUNW       :'LOSUNW',
        PT_SUNWBSS      :'SUNWBSS',
        PT_SUNWSTACK    :'SUNWSTACK',
        PT_HISUNW       :'HISUNW',
        PT_HIOS         :'HIOS',
        PT_LOPROC       :'LOPROC',
        PT_HIPROC       :'HIPROC'
        }

    if value in names:
        ret = names[value]
    else:
        ret = '0x{:x}'.format(value)

    return ret
