
import copy
import mmap
import os.path
import logging

from wayround_org.utils.format.elf_enum import *

from wayround_org.utils.format.elf_bin import (
    read_e_ident,
    is_elf,
    e_ident_bitness,
    e_ident_endianness,
    e_ident_to_dict,

    read_elf_ehdr_x,
    read_elf_ehdr,

    elf32_ehdr_to_dict,
    elf64_ehdr_to_dict,
    elf_ehdr_to_dict,

    read_elf_shdr_x,
    read_elf_shdr,

    read_elf_phdr_x,
    read_elf_phdr,


    read_elf_section_header_table,
    read_elf_section_header_table_names,

    read_elf_program_header_table,

    read_dynamic_section,

    get_dynamic_libs_names,
    get_dynamic_runpath_values,
    convert_virtual_to_file
    )


def dict_byte_to_ints(elf_ehdr_dict, only_keys=None, endianness='little'):

    ret = copy.copy(elf_ehdr_dict)

    for i in ret.keys():
        work_it = False

        if isinstance(only_keys, (list, set)):
            if i in only_keys:
                work_it = True
        else:
            work_it = True

        if work_it:
            ret[i] = int.from_bytes(ret[i], endianness)

    return ret


def e_ident_text(e_ident_dict):

    ret = """\
Class:       {e_i_s_class}
Data:        {e_i_s_data}
Version:     {e_i_s_version}
OS ABI:      {e_i_s_osabi}
ABI Version: {e_i_s_abiversion}
""".format_map(e_ident_dict)

    return ret


def elf_x_ehdr_text(elf_ehdr_dict, endianness):

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
""".format_map(dict_byte_to_ints(elf_ehdr_dict, endianness=endianness))

    return ret


def get_section_header_type_name(value):

    ret = None

    names = {
        SHT_NULL: 'NULL',
        SHT_PROGBITS: 'PROGBITS',
        SHT_SYMTAB: 'SYMTAB',
        SHT_STRTAB: 'STRTAB',
        SHT_RELA: 'RELA',
        SHT_HASH: 'HASH',
        SHT_DYNAMIC: 'DYNAMIC',
        SHT_NOTE: 'NOTE',
        SHT_NOBITS: 'NOBITS',
        SHT_REL: 'REL',
        SHT_SHLIB: 'SHLIB',
        SHT_DYNSYM: 'DYNSYM',
        SHT_INIT_ARRAY: 'INIT_ARRAY',
        SHT_FINI_ARRAY: 'FINI_ARRAY',
        SHT_PREINIT_ARRAY: 'PREINIT_ARRAY',
        SHT_GROUP: 'GROUP',
        SHT_SYMTAB_SHNDX: 'SYMTAB_SHNDX',
        SHT_NUM: 'NUM',
        SHT_LOOS: 'LOOS',
        SHT_GNU_ATTRIBUTES: 'GNU_ATTRIBUTES',
        SHT_GNU_HASH: 'GNU_HASH',
        SHT_GNU_LIBLIST: 'GNU_LIBLIST',
        SHT_CHECKSUM: 'CHECKSUM',
        SHT_LOSUNW: 'LOSUNW',
        SHT_SUNW_move: 'SUNW_move',
        SHT_SUNW_COMDAT: 'SUNW_COMDAT',
        SHT_SUNW_syminfo: 'SUNW_syminfo',
        SHT_GNU_verdef: 'GNU_verdef',
        SHT_GNU_verneed: 'GNU_verneed',
        SHT_GNU_versym: 'GNU_versym',
        SHT_HISUNW: 'HISUNW',
        SHT_HIOS: 'HIOS',
        SHT_LOPROC: 'LOPROC',
        SHT_HIPROC: 'HIPROC',
        SHT_LOUSER: 'LOUSER',
        SHT_HIUSER: 'HIUSER'
        }

    if value in names:
        ret = names[value]
    else:
        ret = '0x{:x}'.format(value)

    return ret


def get_program_header_type_name(value):

    ret = None

    names = {
        PT_NULL: 'NULL',
        PT_LOAD: 'LOAD',
        PT_DYNAMIC: 'DYNAMIC',
        PT_INTERP: 'INTERP',
        PT_NOTE: 'NOTE',
        PT_SHLIB: 'SHLIB',
        PT_PHDR: 'PHDR',
        PT_TLS: 'TLS',
        PT_NUM: 'NUM',
        PT_LOOS: 'LOOS',
        PT_GNU_EH_FRAME: 'GNU_EH_FRAME',
        PT_GNU_STACK: 'GNU_STACK',
        PT_GNU_RELRO: 'GNU_RELRO',
        PT_LOSUNW: 'LOSUNW',
        PT_SUNWBSS: 'SUNWBSS',
        PT_SUNWSTACK: 'SUNWSTACK',
        PT_HISUNW: 'HISUNW',
        PT_HIOS: 'HIOS',
        PT_LOPROC: 'LOPROC',
        PT_HIPROC: 'HIPROC'
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


def section_header_table_text(
        data,
        elf_section_header_table,
        ehdr_dict,
        endianness
        ):

    ret = ''

    names = read_elf_section_header_table_names(
        data, elf_section_header_table, ehdr_dict, endianness
        )

    section_header_table2 = []
    for i in elf_section_header_table:
        section_header_table2.append(
            dict_byte_to_ints(
                i,
                endianness=endianness
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
            get_section_header_type_name(
                elf_section_header_table[i]['sh_type'])
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


def program_header_table_text(program_header_table, endianness):

    ret = ''

    program_header_table2 = []
    for i in program_header_table:
        program_header_table2.append(
            dict_byte_to_ints(
                i,
                endianness=endianness
                )
            )

    program_header_table = program_header_table2

    types = []
    for i in range(len(program_header_table)):
        types.append(
            get_program_header_type_name(
                program_header_table[i]['p_type']))

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


def dynamic_section_text(dinamics_table, endianness):

    ret = ''

    names = []

    for i in range(len(dinamics_table)):
        names.append(get_dynamic_type_name(dinamics_table[i]['d_tag']))

    longest_t = 0
    for i in names:
        if len(i) > longest_t:
            longest_t = len(i)

    for i in dinamics_table:
        number = 0
        if get_dynamic_type_name(i['d_tag']) == 'DT_NEEDED':
            number = i['d_ptr']
        else:
            number = i['d_val']
        ret += "{}  {:08x}\n".format(
            get_dynamic_type_name(i['d_tag']).ljust(longest_t),
            number
            )

    return ret


class ELF:

    def __init__(self, filename, verbose=False, debug=False, mute=False):

        if debug or verbose:
            print("File `{}'".format(filename))

        self.debug = debug

        self.verbose = verbose

        self.mute = mute

        self.opened = False

        self.filename = filename

        self.is_elf = False
        self.e_ident = None
        self.bitness = None
        self.elf_type_name = None
        self.endianness = None
        self.e_ident_dict = None
        self.e_ident_text = None
        self.elf_ehdr = None
        self.elf_ehdr_dict = None
        self.elf_x_ehdr_text = None
        self.section_table = None
        self.section_names = None
        self.program_table = None
        self.section_header_table_text = None
        self.program_header_table_text = None
        self.dynamic_section = None
        self.dynamic_section_text = None
        self.needed_libs_list = None
        self.runpath_values = None
        self.libs_list_text = None

        if not os.path.isfile(filename):
            if not mute:
                logging.error("Not a file: `{}'".format(filename))
        else:

            if os.stat(filename).st_size == 0:
                if not mute and verbose:
                    logging.info("File size is 0: {}".format(filename))
            else:

                try:
                    f = open(filename, 'rb')
                except KeyboardInterrupt:
                    raise
                except:
                    if not mute:
                        logging.exception(
                            "Couldn't open file for read: `{}'".format(
                                filename)
                            )
                else:

                    try:
                        m = mmap.mmap(
                            f.fileno(),
                            0,
                            flags=mmap.MAP_PRIVATE,
                            prot=mmap.PROT_READ
                            )
                    except KeyboardInterrupt:
                        raise
                    except:
                        if not mute:
                            logging.exception(
                                "Couldn't map file: `{}'".format(filename)
                                )
                    else:
                        try:
                            self.opened = True

                            self.is_elf = is_elf(m)

                            if self.is_elf:

                                self.e_ident = read_e_ident(m)

                                if debug:
                                    print(
                                        "e_ident == {}".format(self.e_ident)
                                        )

                                if self.e_ident:
                                    self.bitness = e_ident_bitness(
                                        self.e_ident)

                                if debug:
                                    print("bitness == {}".format(self.bitness))

                                if self.e_ident:
                                    self.endianness = e_ident_endianness(
                                        self.e_ident
                                        )

                                if debug:
                                    print(
                                        "endianness == {}".format(
                                            self.endianness))

                                if self.e_ident:
                                    self.e_ident_dict = e_ident_to_dict(
                                        self.e_ident)

                                if debug:
                                    print(
                                        "e_ident_dict == {}".format(
                                            self.e_ident_dict))

                                if self.e_ident_dict:
                                    self.e_ident_text = e_ident_text(
                                        self.e_ident_dict
                                        )

                                if debug:
                                    print(
                                        "e_ident_text == {}".format(
                                            self.e_ident_text))

                                if self.e_ident_dict:
                                    self.elf_ehdr = read_elf_ehdr(
                                        m,
                                        0,
                                        self.e_ident_dict
                                        )

                                if debug:
                                    print(
                                        "elf_ehdr == {}".format(
                                            self.elf_ehdr))

                                if self.e_ident_dict:
                                    self.elf_ehdr_dict = elf_ehdr_to_dict(
                                        m,
                                        0,
                                        self.e_ident_dict
                                        )

                                if debug:
                                    print(
                                        "elf_ehdr_dict == {}".format(
                                            self.elf_ehdr_dict))

                                if self.elf_ehdr_dict and self.endianness:
                                    self.elf_x_ehdr_text = elf_x_ehdr_text(
                                        self.elf_ehdr_dict,
                                        self.endianness
                                        )

                                if debug:
                                    print(
                                        "elf_x_ehdr_text == {}".format(
                                            self.elf_x_ehdr_text))

                                if self.elf_ehdr_dict and self.endianness:
                                    self.elf_type_name = int.from_bytes(
                                        self.elf_ehdr_dict['e_type'],
                                        self.endianness
                                        )

                                    for i in [
                                            'ET_NONE',
                                            'ET_REL',
                                            'ET_EXEC',
                                            'ET_DYN',
                                            'ET_CORE',
                                            'ET_NUM',
                                            'ET_LOOS',
                                            'ET_HIOS',
                                            'ET_LOPROC',
                                            'ET_HIPROC'
                                            ]:

                                        if self.elf_type_name == eval(i):
                                            self.elf_type_name = i
                                            break

                                if debug:
                                    print(
                                        "elf_type_name == {}".format(
                                            self.elf_type_name))

                                if self.e_ident_dict and self.elf_ehdr_dict:
                                    self.section_table = read_elf_section_header_table(
                                        m,
                                        self.e_ident_dict,
                                        self.elf_ehdr_dict
                                        )

                                if debug:
                                    print(
                                        "section_table == {}".format(
                                            self.section_table))

                                if (self.section_table
                                        and self.elf_ehdr_dict
                                        and self.endianness):
                                    self.section_names = (
                                        read_elf_section_header_table_names(
                                            m,
                                            self.section_table,
                                            self.elf_ehdr_dict,
                                            self.endianness
                                            )
                                        )

                                if debug:
                                    print(
                                        "section_names == {}".format(
                                            self.section_names))

                                if self.e_ident_dict and self.elf_ehdr_dict:
                                    self.program_table = read_elf_program_header_table(
                                        m,
                                        self.e_ident_dict,
                                        self.elf_ehdr_dict
                                        )

                                if debug:
                                    print(
                                        "program_table == {}".format(
                                            self.program_table))

                                if (self.section_table
                                        and self.elf_ehdr_dict
                                        and self.endianness):
                                    self.section_header_table_text = (
                                        section_header_table_text(
                                            m,
                                            self.section_table,
                                            self.elf_ehdr_dict,
                                            self.endianness
                                            )
                                        )

                                if debug:
                                    print(
                                        "section_header_table_text == {}".format(
                                            self.section_header_table_text))

                                if self.program_table and self.endianness:
                                    self.program_header_table_text = (
                                        program_header_table_text(
                                            self.program_table,
                                            self.endianness
                                            )
                                        )

                                if debug:
                                    print(
                                        "program_header_table_text == {}".format(
                                            self.program_header_table_text))

                                dyn_sect_index = None
                                if (
                                        self.section_names
                                        and '.dynamic' in self.section_names
                                        and self.section_table
                                        and int.from_bytes(
                                            self.section_table[
                                                self.section_names.index('.dynamic')]['sh_type'],
                                            self.endianness,
                                            signed=False
                                            ) == SHT_DYNAMIC
                                        ):
                                    dyn_sect_index = self.section_names.index(
                                        '.dynamic')

                                if debug:
                                    print(
                                        "dyn_sect_index == {}".format(dyn_sect_index))

                                dyn_sect_offset = None
                                if (self.section_table
                                        and dyn_sect_index
                                        and self.endianness
                                        and 'sh_offset' in self.section_table[dyn_sect_index]):
                                    dyn_sect_offset = int.from_bytes(
                                        self.section_table[
                                            dyn_sect_index]['sh_offset'],
                                        self.endianness
                                        )

                                if debug:
                                    print(
                                        "dyn_sect_offset == {}".format(dyn_sect_offset))

                                if dyn_sect_offset and self.bitness and self.endianness:
                                    self.dynamic_section = read_dynamic_section(
                                        m,
                                        dyn_sect_offset,
                                        self.bitness,
                                        self.endianness
                                        )

                                if debug:
                                    print(
                                        "dynamic_section == {}".format(
                                            self.dynamic_section))

                                if self.dynamic_section and self.endianness:
                                    self.dynamic_section_text = dynamic_section_text(
                                        self.dynamic_section,
                                        self.endianness
                                        )

                                if debug:
                                    print(
                                        "dynamic_section_text == {}".format(
                                            self.dynamic_section_text))

                                if (self.program_table
                                        and self.dynamic_section
                                        and self.section_table
                                        and self.endianness):

                                    self.needed_libs_list = get_dynamic_libs_names(
                                        m,
                                        self.program_table,
                                        self.dynamic_section,
                                        self.section_table,
                                        self.endianness
                                        )

                                    self.runpath_values = get_dynamic_runpath_values(
                                        m,
                                        self.program_table,
                                        self.dynamic_section,
                                        self.section_table,
                                        self.endianness
                                        )

                                if debug:
                                    print(
                                        "needed_libs_list == {}".format(
                                            self.needed_libs_list))
                                    print(
                                        "runpath_values == {}".format(
                                            self.runpath_values))

                                if self.needed_libs_list:
                                    self.libs_list_text = "{}.".format(
                                        ', '.join(self.needed_libs_list)
                                        )

                                if debug:
                                    print(
                                        "libs_list_text == {}".format(
                                            self.libs_list_text))

                        except KeyboardInterrupt:
                            raise
                        except:
                            if debug or verbose:
                                logging.exception(
                                    "Some error while populating instance")

                        finally:
                            m.close()
                    finally:
                        f.close()
        return

    def return_text(self):
        ret = """\
file: {filename}

is elf?: {is_elf}

({bitness}-bit)
({endianness}-byteorder)

{e_ident_text}

{elf_x_ehdr_text}

Section table:
{section_header_table_text}

Program table:
{program_header_table_text}

Dynamic section:
{dynamic_section_text}

Needed libs list:
{libs_list_text}
""".format(
            filename=self.filename,
            is_elf=self.is_elf,
            bitness=self.bitness,
            endianness=self.endianness,
            e_ident_text=self.e_ident_text,
            elf_x_ehdr_text=self.elf_x_ehdr_text,
            section_header_table_text=self.section_header_table_text,
            program_header_table_text=self.program_header_table_text,
            dynamic_section_text=self.dynamic_section_text,
            libs_list_text=self.libs_list_text
            )

        return ret
