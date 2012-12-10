
import mmap
import struct
import sys



E_IDENT = (

    # /* Fields in the e_ident array.  The EI_* macros are indices into the
    # array.  The macros under each EI_* macro are the values the byte
    # may have.  */

    '1s'  # EI_MAG0
    '1s'  # EI_MAG1
    '1s'  # EI_MAG2
    '1s'  # EI_MAG3


    # #define EI_CLASS        4               /* File class byte index */
    # #define ELFCLASSNONE    0               /* Invalid class */
    # #define ELFCLASS32      1               /* 32-bit objects */
    # #define ELFCLASS64      2               /* 64-bit objects */
    # #define ELFCLASSNUM     3

    '1s'  # EI_CLASS

    #    #define EI_DATA         5               /* Data encoding byte index */
    #    #define ELFDATANONE     0               /* Invalid data encoding */
    #    #define ELFDATA2LSB     1               /* 2's complement, little endian */
    #    #define ELFDATA2MSB     2               /* 2's complement, big endian */
    #    #define ELFDATANUM      3

    '1s'  # EI_DATA

    #    #define EI_VERSION      6               /* File version byte index */

    '1s'  # EI_VERSION

    #    #define EI_OSABI        7               /* OS ABI identification */
    #    #define ELFOSABI_NONE           0       /* UNIX System V ABI */
    #    #define ELFOSABI_SYSV           0       /* Alias.  */
    #    #define ELFOSABI_HPUX           1       /* HP-UX */
    #    #define ELFOSABI_NETBSD         2       /* NetBSD.  */
    #    #define ELFOSABI_GNU            3       /* Object uses GNU ELF extensions.  */
    #    #define ELFOSABI_LINUX          ELFOSABI_GNU /* Compatibility alias.  */
    #    #define ELFOSABI_SOLARIS        6       /* Sun Solaris.  */
    #    #define ELFOSABI_AIX            7       /* IBM AIX.  */
    #    #define ELFOSABI_IRIX           8       /* SGI Irix.  */
    #    #define ELFOSABI_FREEBSD        9       /* FreeBSD.  */
    #    #define ELFOSABI_TRU64          10      /* Compaq TRU64 UNIX.  */
    #    #define ELFOSABI_MODESTO        11      /* Novell Modesto.  */
    #    #define ELFOSABI_OPENBSD        12      /* OpenBSD.  */
    #    #define ELFOSABI_ARM_AEABI      64      /* ARM EABI */
    #    #define ELFOSABI_ARM            97      /* ARM */
    #    #define ELFOSABI_STANDALONE     255     /* Standalone (embedded) application */

    '1s'  # EI_OSABI

    #    #define EI_ABIVERSION   8               /* ABI version */

    '1s'

    #    #define EI_PAD          9               /* Byte index of padding bytes */

    '1s'

    '6s'  # TODO: unknown
    )


class NotElf(Exception): pass
class ElfReadError(Exception): pass

def read_elf(in_bytes):

    ret = {}
    try:
        ret = {
            'e_ident':read_e_ident(in_bytes)
            }
    except:
        raise ElfReadError("Error reading data")

    if not (ret['e_ident']['EI_MAG0'] == b'\x7f'
            and ret['e_ident']['EI_MAG1'] == b'E'
            and ret['e_ident']['EI_MAG2'] == b'L'
            and ret['e_ident']['EI_MAG3'] == b'F'
            ):
        raise NotElf("Not an ELF")

    return ret

def read_e_ident(in_bytes):

    d = in_bytes[0:struct.calcsize(E_IDENT)]

    dd = struct.unpack(E_IDENT, d)

    ret = {
        'EI_MAG0'        : dd[0],
        'EI_MAG1'        : dd[1],
        'EI_MAG2'        : dd[2],
        'EI_MAG3'        : dd[3],
        'EI_CLASS'       : int.from_bytes(dd[4], sys.byteorder),
        'EI_DATA'        : int.from_bytes(dd[5], sys.byteorder),
        'EI_VERSION'     : int.from_bytes(dd[6], sys.byteorder),
        'EI_OSABI'       : int.from_bytes(dd[7], sys.byteorder),
        'EI_ABIVERSION'  : int.from_bytes(dd[8], sys.byteorder),
        'EI_PAD'         : int.from_bytes(dd[9], sys.byteorder),
        'REST'           : dd[10],
        }

    return ret

def legend(elf_struct):

    m = {}

#    m['c1'] = elf_struct['e_ident']['EI_CLASS']
#    m['c2'] =
#
#    print("""\
#Class:        {c1} ({c2})
#Encoding:     {e1} ({e2})
#File Version: {f1} ({f2})
#OS ABI:       {o1} ({o2})
#ABI Version:  {a1} ({a2})
#Padding:      {p}
#""".format_map(m))
