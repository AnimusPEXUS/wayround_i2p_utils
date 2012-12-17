
from libc.stdint cimport *

cimport org.wayround.utils.format.elf_enum as elf_enum
    
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
    
            
    ctypedef struct Elf32_Ehdr:

        unsigned char    e_ident[elf_enum.EI_NIDENT]
        Elf32_Half    e_type
        Elf32_Half    e_machine
        Elf32_Word    e_version
        Elf32_Addr    e_entry
        Elf32_Off    e_phoff
        Elf32_Off    e_shoff
        Elf32_Word    e_flags
        Elf32_Half    e_ehsize
        Elf32_Half    e_phentsize
        Elf32_Half    e_phnum
        Elf32_Half    e_shentsize
        Elf32_Half    e_shnum
        Elf32_Half    e_shstrndx
     
    
    ctypedef struct Elf64_Ehdr:
    
        unsigned char    e_ident[elf_enum.EI_NIDENT]
        Elf64_Half    e_type            
        Elf64_Half    e_machine        
        Elf64_Word    e_version       
        Elf64_Addr    e_entry        
        Elf64_Off    e_phoff        
        Elf64_Off    e_shoff        
        Elf64_Word    e_flags       
        Elf64_Half    e_ehsize       
        Elf64_Half    e_phentsize    
        Elf64_Half    e_phnum        
        Elf64_Half    e_shentsize    
        Elf64_Half    e_shnum        
        Elf64_Half    e_shstrndx    
        
                
