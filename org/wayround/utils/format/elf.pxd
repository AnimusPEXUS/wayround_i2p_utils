
from libc.stdint cimport *
    
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
    
        
    cdef enum:
        EI_NIDENT= 16
    
    ctypedef struct Elf32_Ehdr:

        unsigned char    e_ident[EI_NIDENT]
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
    
        unsigned char    e_ident[EI_NIDENT]
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
        
            
    cdef enum:    
        EI_MAG0   =     0    
        ELFMAG0   =   0x7f  
    
        EI_MAG1   =     1    
        
    cdef char ELFMAG1   =    'E'  
    
    cdef enum:    
        EI_MAG2   =     2    
    
    cdef char ELFMAG2   =     'L' 
    
    cdef enum:    
        EI_MAG3   =     3     

    cdef char ELFMAG3 =     'F'   
        
    cdef char ELFMAG =   {ELFMAG0,EI_MAG1,EI_MAG2,EI_MAG3}
    
    cdef enum:    
        SELFMAG    =    4
        
        EI_CLASS      =  4      
        ELFCLASSNONE  =  0   
        ELFCLASS32    =  1   
        ELFCLASS64    =  2   
        ELFCLASSNUM   =  3
        
        EI_DATA       =  5   
        ELFDATANONE   =  0   
        ELFDATA2LSB   =  1   
        ELFDATA2MSB   =  2  
        ELFDATANUM    =  3
        
        EI_VERSION  =  6
                         
        
        EI_OSABI    =  7  
        ELFOSABI_NONE   =     0 
        ELFOSABI_SYSV   =     0 
        ELFOSABI_HPUX   =     1  
        ELFOSABI_NETBSD   =     2  
        ELFOSABI_GNU    =    3 
        ELFOSABI_LINUX   =     ELFOSABI_GNU
        ELFOSABI_SOLARIS  =  6    
        ELFOSABI_AIX   =     7 
        ELFOSABI_IRIX    =    8    
        ELFOSABI_FREEBSD  =  9  
        ELFOSABI_TRU64    =    10   
        ELFOSABI_MODESTO  =  11  
        ELFOSABI_OPENBSD  =  12 
        ELFOSABI_ARM_AEABI =   64 
        ELFOSABI_ARM  =     97
        ELFOSABI_STANDALONE  =  255  
        
        EI_ABIVERSION =   8    
        
        EI_PAD   =     9     
            
 
