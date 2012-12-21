
from libc.stdint cimport * 

from org.wayround.utils.format.elf_enum cimport * 

cdef extern from "elf.h":

    ctypedef uint16_t Elf32_Half
    ctypedef uint16_t Elf64_Half
    
    ctypedef uint32_t Elf32_Word
    ctypedef int32_t  Elf32_Sword
    ctypedef uint32_t Elf64_Word
    ctypedef int32_t  Elf64_Sword
    
    ctypedef uint64_t Elf32_Xword
    ctypedef int64_t  Elf32_Sxword
    ctypedef uint64_t Elf64_Xword
    ctypedef int64_t  Elf64_Sxword
    
    ctypedef uint32_t Elf32_Addr
    ctypedef uint64_t Elf64_Addr
    
    ctypedef uint32_t Elf32_Off
    ctypedef uint64_t Elf64_Off
    
    ctypedef uint16_t Elf32_Section
    ctypedef uint16_t Elf64_Section
    
    ctypedef Elf32_Half Elf32_Versym
    ctypedef Elf64_Half Elf64_Versym
    
    # The ELF file header.  This appears at the start of every ELF file.
    
    ctypedef struct Elf32_Ehdr:
        unsigned char e_ident[EI_NIDENT] #  Magic number and other info 
        Elf32_Half    e_type             #  Object file type 
        Elf32_Half    e_machine          #  Architecture 
        Elf32_Word    e_version          #  Object file version  
        Elf32_Addr    e_entry            #  Entry point virtual address 
        Elf32_Off     e_phoff            #  Program header table file offset    
        Elf32_Off     e_shoff            #  Section header table file offset 
        Elf32_Word    e_flags            #  Processor-specific flags 
        Elf32_Half    e_ehsize           #  ELF header size in bytes 
        Elf32_Half    e_phentsize        #  Program header table entry size 
        Elf32_Half    e_phnum            #  Program header table entry count 
        Elf32_Half    e_shentsize        #  Section header table entry size 
        Elf32_Half    e_shnum            #  Section header table entry count 
        Elf32_Half    e_shstrndx         #  Section header string table index 
    
    
    ctypedef struct Elf64_Ehdr:
        unsigned char e_ident[EI_NIDENT]
        Elf64_Half    e_type
        Elf64_Half    e_machine
        Elf64_Word    e_version
        Elf64_Addr    e_entry
        Elf64_Off     e_phoff
        Elf64_Off     e_shoff
        Elf64_Word    e_flags
        Elf64_Half    e_ehsize
        Elf64_Half    e_phentsize
        Elf64_Half    e_phnum
        Elf64_Half    e_shentsize
        Elf64_Half    e_shnum
        Elf64_Half    e_shstrndx
    

    # Section header

    ctypedef struct Elf32_Shdr:
        Elf32_Word    sh_name         # Section name (string tbl index) 
        Elf32_Word    sh_type         # Section type 
        Elf32_Word    sh_flags        # Section flags 
        Elf32_Addr    sh_addr         # Section virtual addr at execution 
        Elf32_Off     sh_offset       # Section file offset 
        Elf32_Word    sh_size         # Section size in bytes 
        Elf32_Word    sh_link         # Link to another section 
        Elf32_Word    sh_info         # Additional section information 
        Elf32_Word    sh_addralign    # Section alignment 
        Elf32_Word    sh_entsize      # Entry size if section holds table 
    
    
    ctypedef struct Elf64_Shdr:
        Elf64_Word    sh_name
        Elf64_Word    sh_type
        Elf64_Xword   sh_flags
        Elf64_Addr    sh_addr
        Elf64_Off     sh_offset
        Elf64_Xword   sh_size
        Elf64_Word    sh_link
        Elf64_Word    sh_info
        Elf64_Xword   sh_addralign
        Elf64_Xword   sh_entsize


    # Symbol table entry

    ctypedef struct Elf32_Sym:
        Elf32_Word    st_name         # Symbol name (string tbl index)
        Elf32_Addr    st_value        # Symbol value
        Elf32_Word    st_size         # Symbol size
        unsigned char st_info         # Symbol type and binding
        unsigned char st_other        # Symbol visibility
        Elf32_Section st_shndx        # Section index
        
    ctypedef struct Elf64_Sym:
        Elf64_Word    st_name
        unsigned char st_info
        unsigned char st_other
        Elf64_Section st_shndx
        Elf64_Addr    st_value
        Elf64_Xword   st_size


    # Symbol table entry.
    
    ctypedef struct Elf32_Sym:
        Elf32_Word    st_name       # Symbol name (string tbl index) 
        Elf32_Addr    st_value      # Symbol value 
        Elf32_Word    st_size       # Symbol size 
        unsigned char st_info       # Symbol type and binding 
        unsigned char st_other      # Symbol visibility 
        Elf32_Section st_shndx      # Section index
    
    ctypedef struct Elf64_Sym:
        Elf64_Word    st_name
        unsigned char st_info
        unsigned char st_other
        Elf64_Section st_shndx
        Elf64_Addr    st_value
        Elf64_Xword   st_size


    
    # The syminfo section if available contains additional information about
    # every dynamic symbol.

    ctypedef struct Elf32_Syminfo:
        Elf32_Half    si_boundto         # Direct bindings, symbol bound to
        Elf32_Half    si_flags           # Per symbol flags
    
    ctypedef struct Elf64_Syminfo:
        Elf64_Half    si_boundto
        Elf64_Half    si_flags




    # Relocation table entry without addend (in section of type SHT_REL).  

    ctypedef struct Elf32_Rel:
        Elf32_Addr    r_offset             # Address 
        Elf32_Word    r_info               # Relocation type and symbol index 
    
    #    /* I have seen two different definitions of the Elf64_Rel and
    #       Elf64_Rela structures, so we'll leave them out until Novell (or
    #       whoever) gets their act together.  */
    #    /* The following, at least, is used on Sparc v9, MIPS, and Alpha.  */
    
    ctypedef struct Elf64_Rel:
        Elf64_Addr    r_offset        
        Elf64_Xword   r_info          
    
    # Relocation table entry with addend (in section of type SHT_RELA).  
    
    ctypedef struct Elf32_Rela:
        Elf32_Addr    r_offset
        Elf32_Word    r_info
        Elf32_Sword   r_addend
    
    ctypedef struct Elf64_Rela:
        Elf64_Addr    r_offset
        Elf64_Xword   r_info
        Elf64_Sxword  r_addend

    # Program segment header.  

    ctypedef struct Elf32_Phdr:
        Elf32_Word    p_type          # Segment type 
        Elf32_Off     p_offset        # Segment file offset 
        Elf32_Addr    p_vaddr         # Segment virtual address 
        Elf32_Addr    p_paddr         # Segment physical address 
        Elf32_Word    p_filesz        # Segment size in file 
        Elf32_Word    p_memsz         # Segment size in memory 
        Elf32_Word    p_flags         # Segment flags 
        Elf32_Word    p_align         # Segment alignment 
    
    ctypedef struct Elf64_Phdr:
        Elf64_Word    p_type
        Elf64_Word    p_flags
        Elf64_Off     p_offset
        Elf64_Addr    p_vaddr
        Elf64_Addr    p_paddr
        Elf64_Xword   p_filesz
        Elf64_Xword   p_memsz
        Elf64_Xword   p_align



    # Dynamic section entry.  

#    ctypedef union d_un32_uni:
#        Elf32_Word      d_val          # Integer value
#        Elf32_Addr      d_ptr          # Address value
#
#    ctypedef struct Elf32_Dyn:
#        Elf32_Sword     d_tag          # Dynamic entry type
#        d_un32_uni      d_un
#
#    ctypedef union d_un64_uni:
#        Elf64_Xword     d_val
#        Elf64_Addr      d_ptr
#
#    ctypedef struct Elf64_Dyn:
#        Elf64_Sxword    d_tag
#        d_un64_uni      d_un


    # Version definition sections.

    ctypedef struct Elf32_Verdef:
        Elf32_Half    vd_version        # Version revision 
        Elf32_Half    vd_flags          # Version information 
        Elf32_Half    vd_ndx            # Version Index 
        Elf32_Half    vd_cnt            # Number of associated aux entries 
        Elf32_Word    vd_hash           # Version name hash value 
        Elf32_Word    vd_aux            # Offset in bytes to verdaux array 
        Elf32_Word    vd_next           # Offset in bytes to next verdef entry 
    
    ctypedef struct Elf64_Verdef:
        Elf64_Half    vd_version
        Elf64_Half    vd_flags
        Elf64_Half    vd_ndx
        Elf64_Half    vd_cnt
        Elf64_Word    vd_hash
        Elf64_Word    vd_aux
        Elf64_Word    vd_next



    # Auxialiary version information.
    
    ctypedef struct Elf32_Verdaux:
        Elf32_Word    vda_name         # Version or dependency names 
        Elf32_Word    vda_next         # Offset in bytes to next verdaux entry
                          
    
    ctypedef struct Elf64_Verdaux:
        Elf64_Word    vda_name
        Elf64_Word    vda_next
