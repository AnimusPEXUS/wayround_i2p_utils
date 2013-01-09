
import copy
import mmap
import os.path
import sys

from org.wayround.utils.format.elf_enum import *

#def is_elf(bytes_data):
#    return org.wayround.utils.format.elf_bin.is_elf(bytes_data[0:4])

#import org.wayround.utils.format.elf_bin
#
#
#
#read_e_ident = elf_bin.read_e_ident
#is_elf = elf_bin.is_elf
#e_ident_bitness = elf_bin.e_ident_bitness
#e_ident_to_dict = elf_bin.e_ident_to_dict
#
#read_elf_ehdr_x = elf_bin.read_elf_ehdr_x
#read_elf_ehdr = elf_bin.read_elf_ehdr
#
#elf32_ehdr_to_dict = elf_bin.elf32_ehdr_to_dict
#elf64_ehdr_to_dict = elf_bin.elf64_ehdr_to_dict
#elf_ehdr_to_dict = elf_bin.elf_ehdr_to_dict
#
#read_elf_shdr_x = elf_bin.read_elf_shdr_x
#read_elf_shdr = elf_bin.read_elf_shdr
#
#read_elf_phdr_x = elf_bin.read_elf_phdr_x
#read_elf_phdr = elf_bin.read_elf_phdr
#
#
#read_elf_section_header_table = elf_bin.read_elf_section_header_table
#read_elf_section_header_table_names = elf_bin.read_elf_section_header_table_names
#
#read_elf_program_header_table = elf_bin.read_elf_program_header_table
#
#read_dynamic_section = elf_bin.read_dynamic_section
#
#get_dynamic_libs_names = elf_bin.get_dynamic_libs_names

from org.wayround.utils.format.elf_bin import (
    read_e_ident,
    is_elf,
    e_ident_bitness,
    e_ident_to_dict ,

    read_elf_ehdr_x ,
    read_elf_ehdr ,

    elf32_ehdr_to_dict,
    elf64_ehdr_to_dict,
    elf_ehdr_to_dict ,

    read_elf_shdr_x,
    read_elf_shdr ,

    read_elf_phdr_x ,
    read_elf_phdr ,


    read_elf_section_header_table ,
    read_elf_section_header_table_names ,

    read_elf_program_header_table ,

    read_dynamic_section ,

    get_dynamic_libs_names
    )

def e_ident_format(e_ident_dict):

    ret = """\
Class:       {e_i_s_class}
Data:        {e_i_s_data}
Version:     {e_i_s_version}
OS ABI:      {e_i_s_osabi}
ABI Version: {e_i_s_abiversion}
""".format_map(e_ident_dict)

    return ret


def dict_byte_to_ints(elf_ehdr_dict, only_keys=None):

    ret = copy.copy(elf_ehdr_dict)

    for i in ret.keys():
        work_it = False

        if isinstance(only_keys, (list, set)):
            if i in only_keys:
                work_it = True
        else:
            work_it = True

        if work_it:
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


def get_dynamic_type_name(value):
    ret = None

    names = {
        DT_NULL: 'DT_NULL',
        DT_NEEDED: 'DT_NEEDED',
        DT_PLTRELSZ: 'DT_PLTRELSZ',
        DT_PLTGOT: 'DT_PLTGOT',
        DT_HASH: 'DT_HASH',
        DT_STRTAB: 'DT_STRTAB',
        DT_SYMTAB: 'DT_SYMTAB',
        DT_RELA: 'DT_RELA',
        DT_RELASZ: 'DT_RELASZ',
        DT_RELAENT: 'DT_RELAENT',
        DT_STRSZ: 'DT_STRSZ',
        DT_SYMENT: 'DT_SYMENT',
        DT_INIT: 'DT_INIT',
        DT_FINI: 'DT_FINI',
        DT_SONAME: 'DT_SONAME',
        DT_RPATH: 'DT_RPATH',
        DT_SYMBOLIC: 'DT_SYMBOLIC',
        DT_REL: 'DT_REL',
        DT_RELSZ: 'DT_RELSZ',
        DT_RELENT: 'DT_RELENT',
        DT_PLTREL: 'DT_PLTREL',
        DT_DEBUG: 'DT_DEBUG',
        DT_TEXTREL: 'DT_TEXTREL',
        DT_JMPREL: 'DT_JMPREL',
        DT_BIND_NOW: 'DT_BIND_NOW',
        DT_INIT_ARRAY: 'DT_INIT_ARRAY',
        DT_FINI_ARRAY: 'DT_FINI_ARRAY',
        DT_INIT_ARRAYSZ: 'DT_INIT_ARRAYSZ',
        DT_FINI_ARRAYSZ: 'DT_FINI_ARRAYSZ',
        DT_RUNPATH: 'DT_RUNPATH',
        DT_FLAGS: 'DT_FLAGS',
        DT_ENCODING: 'DT_ENCODING',
        DT_PREINIT_ARRAY: 'DT_PREINIT_ARRAY',
        DT_PREINIT_ARRAYSZ: 'DT_PREINIT_ARRAYSZ',
        DT_NUM: 'DT_NUM',
        DT_LOOS: 'DT_LOOS',
        DT_HIOS: 'DT_HIOS',
        DT_LOPROC: 'DT_LOPROC',
        DT_HIPROC: 'DT_HIPROC',
        DT_PROCNUM: 'DT_PROCNUM',
        DT_VALRNGLO: 'DT_VALRNGLO',
        DT_GNU_PRELINKED: 'DT_GNU_PRELINKED',
        DT_GNU_CONFLICTSZ: 'DT_GNU_CONFLICTSZ',
        DT_GNU_LIBLISTSZ: 'DT_GNU_LIBLISTSZ',
        DT_CHECKSUM: 'DT_CHECKSUM',
        DT_PLTPADSZ: 'DT_PLTPADSZ',
        DT_MOVEENT: 'DT_MOVEENT',
        DT_MOVESZ: 'DT_MOVESZ',
        DT_FEATURE_1: 'DT_FEATURE_1',
        DT_POSFLAG_1: 'DT_POSFLAG_1',
        DT_SYMINSZ: 'DT_SYMINSZ',
        DT_SYMINENT: 'DT_SYMINENT',
        DT_VALRNGHI: 'DT_VALRNGHI',
        DT_VALNUM: 'DT_VALNUM',
        DT_ADDRRNGLO: 'DT_ADDRRNGLO',
        DT_GNU_HASH: 'DT_GNU_HASH',
        DT_TLSDESC_PLT: 'DT_TLSDESC_PLT',
        DT_TLSDESC_GOT: 'DT_TLSDESC_GOT',
        DT_GNU_CONFLICT: 'DT_GNU_CONFLICT',
        DT_GNU_LIBLIST: 'DT_GNU_LIBLIST',
        DT_CONFIG: 'DT_CONFIG',
        DT_DEPAUDIT: 'DT_DEPAUDIT',
        DT_AUDIT: 'DT_AUDIT',
        DT_PLTPAD: 'DT_PLTPAD',
        DT_MOVETAB: 'DT_MOVETAB',
        DT_SYMINFO: 'DT_SYMINFO',
        DT_ADDRRNGHI: 'DT_ADDRRNGHI',
        DT_ADDRNUM: 'DT_ADDRNUM',
        DT_VERSYM: 'DT_VERSYM',
        DT_RELACOUNT: 'DT_RELACOUNT',
        DT_RELCOUNT: 'DT_RELCOUNT',
        DT_FLAGS_1: 'DT_FLAGS_1',
        DT_VERDEF: 'DT_VERDEF',
        DT_VERDEFNUM: 'DT_VERDEFNUM',
        DT_VERNEED: 'DT_VERNEED',
        DT_VERNEEDNUM: 'DT_VERNEEDNUM',
        DT_VERSIONTAGNUM: 'DT_VERSIONTAGNUM',
        DT_AUXILIARY: 'DT_AUXILIARY',
        DT_FILTER: 'DT_FILTER',
        DT_EXTRANUM: 'DT_EXTRANUM',
        }

    if value in names:
        ret = names[value]
    else:
        ret = '0x{:x}'.format(value)

    return ret


def convert_virtual_to_file(program_section_table, value):

    ret = None

    for i in program_section_table:
        if value >= i['p_vaddr'] and value < (i['p_vaddr'] + i['p_memsz']):
            ret = i
            break

    return ret

def section_header_table_format(data, elf_section_header_table, ehdr_dict):


    ret = ''

    names = read_elf_section_header_table_names(
        data, elf_section_header_table, ehdr_dict
        )

    section_header_table2 = []
    for i in elf_section_header_table:
        section_header_table2.append(
            dict_byte_to_ints(
                i
                )
            )

    elf_section_header_table = section_header_table2

    longest = 0
    for i in names:
        if len(i) > longest:
            longest = len(i)

    types = []
    for i in range(len(elf_section_header_table)):
        types.append(
            get_section_header_type_name(elf_section_header_table[i]['sh_type'])
            )

    longest_t = 0
    for i in types:
        if len(i) > longest_t:
            longest_t = len(i)

    ret += "  [{index:2}] {name}(sto:{name_addr:5}) {typ} {addr:8} {off:8} {size:8} {es:2} {flg:10} {lk:3} {inf:3} {al:3}\n".format(
        index='No',
        name='Name'.ljust(longest),
        name_addr='',
        typ='Type'.ljust(longest_t),
        flg='Flags',
        addr='Address',
        off='Offset',
        size='Size',
        lk='Lnk',
        inf='Inf',
        al='Al',
        es='SZ'
        )


    for i in range(len(elf_section_header_table)):
        ret += "  [{index:2}] {name}(sto:{name_addr:5x}) {typ} {addr:08x} {off:08x} {size:08x} {es:02x} {flg:010b} {lk:03x} {inf:03x} {al:03x}\n".format(
            index=i,
            name=names[i].ljust(longest),
            name_addr=elf_section_header_table[i]['sh_name'],
            typ=types[i].ljust(longest_t),
            flg=elf_section_header_table[i]['sh_flags'],
            addr=elf_section_header_table[i]['sh_addr'],
            off=elf_section_header_table[i]['sh_offset'],
            size=elf_section_header_table[i]['sh_size'],
            lk=elf_section_header_table[i]['sh_link'],
            inf=elf_section_header_table[i]['sh_info'],
            al=elf_section_header_table[i]['sh_addralign'],
            es=elf_section_header_table[i]['sh_entsize']
            )

    ret += '\n'
    ret += 'sto - string table offset\n'

    return ret


def program_header_table_format(program_header_table):

    ret = ''

    program_header_table2 = []
    for i in program_header_table:
        program_header_table2.append(
            dict_byte_to_ints(
                i
                )
            )

    program_header_table = program_header_table2

    types = []
    for i in range(len(program_header_table)):
        types.append(get_program_header_type_name(program_header_table[i]['p_type']))

    longest_t = 0
    for i in types:
        if len(i) > longest_t:
            longest_t = len(i)

    ret += "  {typ} {offset:8} {virtaddr:8} {physaddr:8} {filesize:8} {memsize:8} {flag:10} {align:8}\n".format(
        typ='Type'.ljust(longest_t),
        flag='Flags',
        offset='F Offset',
        virtaddr='VirtAddr',
        physaddr='PhisAddr',
        filesize='FileSize',
        memsize='MemSize',
        align='Align'
        )

    for i in range(len(program_header_table)):
        ret += "  {typ} {offset:08x} {virtaddr:08x} {physaddr:08x} {filesize:08x} {memsize:08x} {flag:010b} {align:08x}\n".format(
            typ=types[i].ljust(longest_t),
            flag=program_header_table[i]['p_flags'],
            offset=program_header_table[i]['p_offset'],
            virtaddr=program_header_table[i]['p_vaddr'],
            physaddr=program_header_table[i]['p_paddr'],
            filesize=program_header_table[i]['p_filesz'],
            memsize=program_header_table[i]['p_memsz'],
            align=program_header_table[i]['p_align']
            )

    return ret


def dynamics_format(dinamics_table):

    ret = ''

    names = []

    for i in range(len(dinamics_table)):
        names.append(get_dynamic_type_name(dinamics_table[i]['d_tag']))

    longest_t = 0
    for i in names:
        if len(i) > longest_t:
            longest_t = len(i)

    for i in dinamics_table:
        ret += "{}  {:08x}\n".format(get_dynamic_type_name(i['d_tag']).ljust(longest_t), i['d_val'])

    return ret



def read_elf(filename):

    f = open(filename, 'rb')


    m = mmap.mmap(f.fileno(), 0, flags=mmap.MAP_PRIVATE, prot=mmap.PROT_READ)

    print("is elf?: {}".format(is_elf(m)))

    e_ident = read_e_ident(m)

    bitness = e_ident_bitness(e_ident)

    print("({}-bit)".format(bitness))

    e_ident_dict = e_ident_to_dict(e_ident)

    print(e_ident_format(e_ident_dict))

    elf_ehdr = read_elf_ehdr(m, 0, e_ident_dict)

    elf_ehdr_dict = elf_ehdr_to_dict(m, 0, e_ident_dict)

    print(elf_x_ehdr_format(elf_ehdr_dict))

    section_table = read_elf_section_header_table(
        m, e_ident_dict, elf_ehdr_dict
        )

    print("section table:")
    print(
        section_header_table_format(m, section_table, elf_ehdr_dict)
        )

    section_names = read_elf_section_header_table_names(
        m, section_table, elf_ehdr_dict
        )

    program_table = read_elf_program_header_table(
        m, e_ident_dict, elf_ehdr_dict
        )

    print("program table:")
    print(
        program_header_table_format(program_table)
        )

    dyn_sect_index = section_names.index('.dynamic')

    dyn_sect_offset = int.from_bytes(section_table[dyn_sect_index]['sh_offset'], sys.byteorder)

    dyn_sect = read_dynamic_section(m, dyn_sect_offset, bitness)

    print("Dynamic section:")
    print(dynamics_format(dyn_sect))
    #print("names: \n{}".format(section_names))

    libs = get_dynamic_libs_names(
        m, program_table, dyn_sect, section_table, elf_ehdr_dict
        )

    print("libs:")
    print("{}.".format(', '.join(libs)))

    m.close()
    f.close()

def get_libs_list(filename):

    ret = 0

    f = open(filename, 'rb')

    m = None

    try:
        m = mmap.mmap(f.fileno(), 0, flags=mmap.MAP_PRIVATE, prot=mmap.PROT_READ)
    except:
        ret = 2
    else:

        if is_elf(m):

            e_ident = read_e_ident(m)

            bitness = e_ident_bitness(e_ident)

            e_ident_dict = e_ident_to_dict(e_ident)

            elf_ehdr_dict = elf_ehdr_to_dict(m, 0, e_ident_dict)

            section_table = read_elf_section_header_table(
                m, e_ident_dict, elf_ehdr_dict
                )

            section_names = read_elf_section_header_table_names(
                m, section_table, elf_ehdr_dict
                )

            program_table = read_elf_program_header_table(
                m, e_ident_dict, elf_ehdr_dict
                )

            if not '.dynamic' in section_names:
                ret = None
            else:
                dyn_sect_index = section_names.index('.dynamic')

                dyn_sect_offset = int.from_bytes(section_table[dyn_sect_index]['sh_offset'], sys.byteorder)

                dyn_sect = read_dynamic_section(m, dyn_sect_offset, bitness)

                libs = get_dynamic_libs_names(
                    m, program_table, dyn_sect, section_table, elf_ehdr_dict
                    )

                ret = copy.copy(libs)

        m.close()

    f.close()

    del(m)
    del(f)

    return ret

def is_elf_file(filename):

    if not os.path.isfile(filename) or not os.path.exists(filename):
        ret = False
    else:

        ret = 0

        f = open(filename, 'rb')

        m = None

        try:
            m = mmap.mmap(f.fileno(), 0, flags=mmap.MAP_PRIVATE, prot=mmap.PROT_READ)
        except:
            ret = 2
        else:

            ret = is_elf(m)

            m.close()

        f.close()

        del(m)
        del(f)

    return ret

def get_elf_file_type(filename):
    ret = None

    f = open(filename, 'rb')

    m = None

    try:
        m = mmap.mmap(f.fileno(), 0, flags=mmap.MAP_PRIVATE, prot=mmap.PROT_READ)
    except:
        ret = None
    else:

        if is_elf(m):
            e_ident = read_e_ident(m)

            e_ident_dict = e_ident_to_dict(e_ident)

            elf_ehdr_dict = elf_ehdr_to_dict(m, 0, e_ident_dict)

            ret = int.from_bytes(elf_ehdr_dict['e_type'], sys.byteorder)

        m.close()

    f.close()

    del(m)
    del(f)

    return ret

