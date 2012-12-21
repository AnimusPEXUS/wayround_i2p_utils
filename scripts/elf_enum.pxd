#ELFMAG                                   = "\177ELF"             # 
#ELF_NOTE_SOLARIS                         = "SUNW Solaris"        # 
#ELF_NOTE_GNU                             = "GNU"                 # 

cdef extern from "elf.h":
    cdef enum:
        _ELF_H                            # 
        EI_NIDENT                         # 
        EI_MAG0                           #  File identification byte 0 index 
        ELFMAG0                           #  Magic number byte 0 
        EI_MAG1                           #  File identification byte 1 index 
        ELFMAG1                           #  Magic number byte 1 
        EI_MAG2                           #  File identification byte 2 index 
        ELFMAG2                           #  Magic number byte 2 
        EI_MAG3                           #  File identification byte 3 index 
        ELFMAG3                           #  Magic number byte 3 
        SELFMAG                           # 
        EI_CLASS                          #  File class byte index 
        ELFCLASSNONE                      #  Invalid class 
        ELFCLASS32                        #  32-bit objects 
        ELFCLASS64                        #  64-bit objects 
        ELFCLASSNUM                       # 
        EI_DATA                           #  Data encoding byte index 
        ELFDATANONE                       #  Invalid data encoding 
        ELFDATA2LSB                       #  2's complement, little endian 
        ELFDATA2MSB                       #  2's complement, big endian 
        ELFDATANUM                        # 
        EI_VERSION                        #  File version byte index 
        EI_OSABI                          #  OS ABI identification 
        ELFOSABI_NONE                     #  UNIX System V ABI 
        ELFOSABI_SYSV                     #  Alias.  
        ELFOSABI_HPUX                     #  HP-UX 
        ELFOSABI_NETBSD                   #  NetBSD.  
        ELFOSABI_GNU                      #  Object uses GNU ELF extensions.  
        ELFOSABI_LINUX                    #  Compatibility alias.  
        ELFOSABI_SOLARIS                  #  Sun Solaris.  
        ELFOSABI_AIX                      #  IBM AIX.  
        ELFOSABI_IRIX                     #  SGI Irix.  
        ELFOSABI_FREEBSD                  #  FreeBSD.  
        ELFOSABI_TRU64                    #  Compaq TRU64 UNIX.  
        ELFOSABI_MODESTO                  #  Novell Modesto.  
        ELFOSABI_OPENBSD                  #  OpenBSD.  
        ELFOSABI_ARM_AEABI                #  ARM EABI 
        ELFOSABI_ARM                      #  ARM 
        ELFOSABI_STANDALONE               #  Standalone (embedded) application 
        EI_ABIVERSION                     #  ABI version 
        EI_PAD                            #  Byte index of padding bytes 
        ET_NONE                           #  No file type 
        ET_REL                            #  Relocatable file 
        ET_EXEC                           #  Executable file 
        ET_DYN                            #  Shared object file 
        ET_CORE                           #  Core file 
        ET_NUM                            #  Number of defined types 
        ET_LOOS                           #  OS-specific range start 
        ET_HIOS                           #  OS-specific range end 
        ET_LOPROC                         #  Processor-specific range start 
        ET_HIPROC                         #  Processor-specific range end 
        EM_NONE                           #  No machine 
        EM_M32                            #  AT&T WE 32100 
        EM_SPARC                          #  SUN SPARC 
        EM_386                            #  Intel 80386 
        EM_68K                            #  Motorola m68k family 
        EM_88K                            #  Motorola m88k family 
        EM_860                            #  Intel 80860 
        EM_MIPS                           #  MIPS R3000 big-endian 
        EM_S370                           #  IBM System/370 
        EM_MIPS_RS3_LE                    #  MIPS R3000 little-endian 
        EM_PARISC                         #  HPPA 
        EM_VPP500                         #  Fujitsu VPP500 
        EM_SPARC32PLUS                    #  Sun's "v8plus" 
        EM_960                            #  Intel 80960 
        EM_PPC                            #  PowerPC 
        EM_PPC64                          #  PowerPC 64-bit 
        EM_S390                           #  IBM S390 
        EM_V800                           #  NEC V800 series 
        EM_FR20                           #  Fujitsu FR20 
        EM_RH32                           #  TRW RH-32 
        EM_RCE                            #  Motorola RCE 
        EM_ARM                            #  ARM 
        EM_FAKE_ALPHA                     #  Digital Alpha 
        EM_SH                             #  Hitachi SH 
        EM_SPARCV9                        #  SPARC v9 64-bit 
        EM_TRICORE                        #  Siemens Tricore 
        EM_ARC                            #  Argonaut RISC Core 
        EM_H8_300                         #  Hitachi H8/300 
        EM_H8_300H                        #  Hitachi H8/300H 
        EM_H8S                            #  Hitachi H8S 
        EM_H8_500                         #  Hitachi H8/500 
        EM_IA_64                          #  Intel Merced 
        EM_MIPS_X                         #  Stanford MIPS-X 
        EM_COLDFIRE                       #  Motorola Coldfire 
        EM_68HC12                         #  Motorola M68HC12 
        EM_MMA                            #  Fujitsu MMA Multimedia Accelerator
        EM_PCP                            #  Siemens PCP 
        EM_NCPU                           #  Sony nCPU embeeded RISC 
        EM_NDR1                           #  Denso NDR1 microprocessor 
        EM_STARCORE                       #  Motorola Start*Core processor 
        EM_ME16                           #  Toyota ME16 processor 
        EM_ST100                          #  STMicroelectronic ST100 processor 
        EM_TINYJ                          #  Advanced Logic Corp. Tinyj emb.fam
        EM_X86_64                         #  AMD x86-64 architecture 
        EM_PDSP                           #  Sony DSP Processor 
        EM_FX66                           #  Siemens FX66 microcontroller 
        EM_ST9PLUS                        #  STMicroelectronics ST9+ 8/16 mc 
        EM_ST7                            #  STmicroelectronics ST7 8 bit mc 
        EM_68HC16                         #  Motorola MC68HC16 microcontroller 
        EM_68HC11                         #  Motorola MC68HC11 microcontroller 
        EM_68HC08                         #  Motorola MC68HC08 microcontroller 
        EM_68HC05                         #  Motorola MC68HC05 microcontroller 
        EM_SVX                            #  Silicon Graphics SVx 
        EM_ST19                           #  STMicroelectronics ST19 8 bit mc 
        EM_VAX                            #  Digital VAX 
        EM_CRIS                           #  Axis Communications 32-bit embedded processor 
        EM_JAVELIN                        #  Infineon Technologies 32-bit embedded processor 
        EM_FIREPATH                       #  Element 14 64-bit DSP Processor 
        EM_ZSP                            #  LSI Logic 16-bit DSP Processor 
        EM_MMIX                           #  Donald Knuth's educational 64-bit processor 
        EM_HUANY                          #  Harvard University machine-independent object files 
        EM_PRISM                          #  SiTera Prism 
        EM_AVR                            #  Atmel AVR 8-bit microcontroller 
        EM_FR30                           #  Fujitsu FR30 
        EM_D10V                           #  Mitsubishi D10V 
        EM_D30V                           #  Mitsubishi D30V 
        EM_V850                           #  NEC v850 
        EM_M32R                           #  Mitsubishi M32R 
        EM_MN10300                        #  Matsushita MN10300 
        EM_MN10200                        #  Matsushita MN10200 
        EM_PJ                             #  picoJava 
        EM_OPENRISC                       #  OpenRISC 32-bit embedded processor 
        EM_ARC_A5                         #  ARC Cores Tangent-A5 
        EM_XTENSA                         #  Tensilica Xtensa Architecture 
        EM_TILEPRO                        #  Tilera TILEPro 
        EM_TILEGX                         #  Tilera TILE-Gx 
        EM_NUM                            # 
        EM_ALPHA                          # 
        EV_NONE                           #  Invalid ELF version 
        EV_CURRENT                        #  Current version 
        EV_NUM                            # 
        SHN_UNDEF                         #  Undefined section 
        SHN_LORESERVE                     #  Start of reserved indices 
        SHN_LOPROC                        #  Start of processor-specific 
        SHN_BEFORE                        #  Order section before all others
        SHN_AFTER                         #  Order section after all others
        SHN_HIPROC                        #  End of processor-specific 
        SHN_LOOS                          #  Start of OS-specific 
        SHN_HIOS                          #  End of OS-specific 
        SHN_ABS                           #  Associated symbol is absolute 
        SHN_COMMON                        #  Associated symbol is common 
        SHN_XINDEX                        #  Index is in extra table.  
        SHN_HIRESERVE                     #  End of reserved indices 
        SHT_NULL                          #  Section header table entry unused 
        SHT_PROGBITS                      #  Program data 
        SHT_SYMTAB                        #  Symbol table 
        SHT_STRTAB                        #  String table 
        SHT_RELA                          #  Relocation entries with addends 
        SHT_HASH                          #  Symbol hash table 
        SHT_DYNAMIC                       #  Dynamic linking information 
        SHT_NOTE                          #  Notes 
        SHT_NOBITS                        #  Program space with no data (bss) 
        SHT_REL                           #  Relocation entries, no addends 
        SHT_SHLIB                         #  Reserved 
        SHT_DYNSYM                        #  Dynamic linker symbol table 
        SHT_INIT_ARRAY                    #  Array of constructors 
        SHT_FINI_ARRAY                    #  Array of destructors 
        SHT_PREINIT_ARRAY                 #  Array of pre-constructors 
        SHT_GROUP                         #  Section group 
        SHT_SYMTAB_SHNDX                  #  Extended section indeces 
        SHT_NUM                           #  Number of defined types.  
        SHT_LOOS                          #  Start OS-specific.  
        SHT_GNU_ATTRIBUTES                #  Object attributes.  
        SHT_GNU_HASH                      #  GNU-style hash table.  
        SHT_GNU_LIBLIST                   #  Prelink library list 
        SHT_CHECKSUM                      #  Checksum for DSO content.  
        SHT_LOSUNW                        #  Sun-specific low bound.  
        SHT_SUNW_move                     # 
        SHT_SUNW_COMDAT                   # 
        SHT_SUNW_syminfo                  # 
        SHT_GNU_verdef                    #  Version definition section.  
        SHT_GNU_verneed                   #  Version needs section.  
        SHT_GNU_versym                    #  Version symbol table.  
        SHT_HISUNW                        #  Sun-specific high bound.  
        SHT_HIOS                          #  End OS-specific type 
        SHT_LOPROC                        #  Start of processor-specific 
        SHT_HIPROC                        #  End of processor-specific 
        SHT_LOUSER                        #  Start of application-specific 
        SHT_HIUSER                        #  End of application-specific 
        SHF_WRITE                         #  Writable 
        SHF_ALLOC                         #  Occupies memory during execution 
        SHF_EXECINSTR                     #  Executable 
        SHF_MERGE                         #  Might be merged 
        SHF_STRINGS                       #  Contains nul-terminated strings 
        SHF_INFO_LINK                     #  `sh_info' contains SHT index 
        SHF_LINK_ORDER                    #  Preserve order after combining 
        SHF_OS_NONCONFORMING              #  Non-standard OS specific handling
        SHF_GROUP                         #  Section is member of a group.  
        SHF_TLS                           #  Section hold thread-local data.  
        SHF_MASKOS                        #  OS-specific.  
        SHF_MASKPROC                      #  Processor-specific 
        SHF_ORDERED                       #  Special ordering requirement
        SHF_EXCLUDE                       #  Section is excluded unless
        GRP_COMDAT                        #  Mark group as COMDAT.  
        SYMINFO_BT_SELF                   #  Symbol bound to self 
        SYMINFO_BT_PARENT                 #  Symbol bound to parent 
        SYMINFO_BT_LOWRESERVE             #  Beginning of reserved entries 
        SYMINFO_FLG_DIRECT                #  Direct bound symbol 
        SYMINFO_FLG_PASSTHRU              #  Pass-thru symbol for translator 
        SYMINFO_FLG_COPY                  #  Symbol is a copy-reloc 
        SYMINFO_FLG_LAZYLOAD              #  Symbol bound to object to be lazy
        SYMINFO_NONE                      # 
        SYMINFO_CURRENT                   # 
        SYMINFO_NUM                       # 
        STB_LOCAL                         #  Local symbol 
        STB_GLOBAL                        #  Global symbol 
        STB_WEAK                          #  Weak symbol 
        STB_NUM                           #  Number of defined types.  
        STB_LOOS                          #  Start of OS-specific 
        STB_GNU_UNIQUE                    #  Unique symbol.  
        STB_HIOS                          #  End of OS-specific 
        STB_LOPROC                        #  Start of processor-specific 
        STB_HIPROC                        #  End of processor-specific 
        STT_NOTYPE                        #  Symbol type is unspecified 
        STT_OBJECT                        #  Symbol is a data object 
        STT_FUNC                          #  Symbol is a code object 
        STT_SECTION                       #  Symbol associated with a section 
        STT_FILE                          #  Symbol's name is file name 
        STT_COMMON                        #  Symbol is a common data object 
        STT_TLS                           #  Symbol is thread-local data object
        STT_NUM                           #  Number of defined types.  
        STT_LOOS                          #  Start of OS-specific 
        STT_GNU_IFUNC                     #  Symbol is indirect code object 
        STT_HIOS                          #  End of OS-specific 
        STT_LOPROC                        #  Start of processor-specific 
        STT_HIPROC                        #  End of processor-specific 
        STN_UNDEF                         #  End of a chain.  
        STV_DEFAULT                       #  Default symbol visibility rules 
        STV_INTERNAL                      #  Processor specific hidden class 
        STV_HIDDEN                        #  Sym unavailable in other modules 
        STV_PROTECTED                     #  Not preemptible, not exported 
        PN_XNUM                           # 
        PT_NULL                           #  Program header table entry unused 
        PT_LOAD                           #  Loadable program segment 
        PT_DYNAMIC                        #  Dynamic linking information 
        PT_INTERP                         #  Program interpreter 
        PT_NOTE                           #  Auxiliary information 
        PT_SHLIB                          #  Reserved 
        PT_PHDR                           #  Entry for header table itself 
        PT_TLS                            #  Thread-local storage segment 
        PT_NUM                            #  Number of defined types 
        PT_LOOS                           #  Start of OS-specific 
        PT_GNU_EH_FRAME                   #  GCC .eh_frame_hdr segment 
        PT_GNU_STACK                      #  Indicates stack executability 
        PT_GNU_RELRO                      #  Read-only after relocation 
        PT_LOSUNW                         # 
        PT_SUNWBSS                        #  Sun Specific segment 
        PT_SUNWSTACK                      #  Stack segment 
        PT_HISUNW                         # 
        PT_HIOS                           #  End of OS-specific 
        PT_LOPROC                         #  Start of processor-specific 
        PT_HIPROC                         #  End of processor-specific 
        PF_X                              #  Segment is executable 
        PF_W                              #  Segment is writable 
        PF_R                              #  Segment is readable 
        PF_MASKOS                         #  OS-specific 
        PF_MASKPROC                       #  Processor-specific 
        NT_PRSTATUS                       #  Contains copy of prstatus struct 
        NT_FPREGSET                       #  Contains copy of fpregset struct 
        NT_PRPSINFO                       #  Contains copy of prpsinfo struct 
        NT_PRXREG                         #  Contains copy of prxregset struct 
        NT_TASKSTRUCT                     #  Contains copy of task structure 
        NT_PLATFORM                       #  String from sysinfo(SI_PLATFORM) 
        NT_AUXV                           #  Contains copy of auxv array 
        NT_GWINDOWS                       #  Contains copy of gwindows struct 
        NT_ASRS                           #  Contains copy of asrset struct 
        NT_PSTATUS                        #  Contains copy of pstatus struct 
        NT_PSINFO                         #  Contains copy of psinfo struct 
        NT_PRCRED                         #  Contains copy of prcred struct 
        NT_UTSNAME                        #  Contains copy of utsname struct 
        NT_LWPSTATUS                      #  Contains copy of lwpstatus struct 
        NT_LWPSINFO                       #  Contains copy of lwpinfo struct 
        NT_PRFPXREG                       #  Contains copy of fprxregset struct 
        NT_PRXFPREG                       #  Contains copy of user_fxsr_struct 
        NT_PPC_VMX                        #  PowerPC Altivec/VMX registers 
        NT_PPC_SPE                        #  PowerPC SPE/EVR registers 
        NT_PPC_VSX                        #  PowerPC VSX registers 
        NT_386_TLS                        #  i386 TLS slots (struct user_desc) 
        NT_386_IOPERM                     #  x86 io permission bitmap (1=deny) 
        NT_X86_XSTATE                     #  x86 extended state using xsave 
        NT_VERSION                        #  Contains a version string.  
        DT_NULL                           #  Marks end of dynamic section 
        DT_NEEDED                         #  Name of needed library 
        DT_PLTRELSZ                       #  Size in bytes of PLT relocs 
        DT_PLTGOT                         #  Processor defined value 
        DT_HASH                           #  Address of symbol hash table 
        DT_STRTAB                         #  Address of string table 
        DT_SYMTAB                         #  Address of symbol table 
        DT_RELA                           #  Address of Rela relocs 
        DT_RELASZ                         #  Total size of Rela relocs 
        DT_RELAENT                        #  Size of one Rela reloc 
        DT_STRSZ                          #  Size of string table 
        DT_SYMENT                         #  Size of one symbol table entry 
        DT_INIT                           #  Address of init function 
        DT_FINI                           #  Address of termination function 
        DT_SONAME                         #  Name of shared object 
        DT_RPATH                          #  Library search path (deprecated) 
        DT_SYMBOLIC                       #  Start symbol search here 
        DT_REL                            #  Address of Rel relocs 
        DT_RELSZ                          #  Total size of Rel relocs 
        DT_RELENT                         #  Size of one Rel reloc 
        DT_PLTREL                         #  Type of reloc in PLT 
        DT_DEBUG                          #  For debugging; unspecified 
        DT_TEXTREL                        #  Reloc might modify .text 
        DT_JMPREL                         #  Address of PLT relocs 
        DT_BIND_NOW                       #  Process relocations of object 
        DT_INIT_ARRAY                     #  Array with addresses of init fct 
        DT_FINI_ARRAY                     #  Array with addresses of fini fct 
        DT_INIT_ARRAYSZ                   #  Size in bytes of DT_INIT_ARRAY 
        DT_FINI_ARRAYSZ                   #  Size in bytes of DT_FINI_ARRAY 
        DT_RUNPATH                        #  Library search path 
        DT_FLAGS                          #  Flags for the object being loaded 
        DT_ENCODING                       #  Start of encoded range 
        DT_PREINIT_ARRAY                  #  Array with addresses of preinit fct
        DT_PREINIT_ARRAYSZ                #  size in bytes of DT_PREINIT_ARRAY 
        DT_NUM                            #  Number used 
        DT_LOOS                           #  Start of OS-specific 
        DT_HIOS                           #  End of OS-specific 
        DT_LOPROC                         #  Start of processor-specific 
        DT_HIPROC                         #  End of processor-specific 
        DT_PROCNUM                        #  Most used by any processor 
        DT_VALRNGLO                       # 
        DT_GNU_PRELINKED                  #  Prelinking timestamp 
        DT_GNU_CONFLICTSZ                 #  Size of conflict section 
        DT_GNU_LIBLISTSZ                  #  Size of library list 
        DT_CHECKSUM                       # 
        DT_PLTPADSZ                       # 
        DT_MOVEENT                        # 
        DT_MOVESZ                         # 
        DT_FEATURE_1                      #  Feature selection (DTF_*).  
        DT_POSFLAG_1                      #  Flags for DT_* entries, effecting
        DT_SYMINSZ                        #  Size of syminfo table (in bytes) 
        DT_SYMINENT                       #  Entry size of syminfo 
        DT_VALRNGHI                       # 
        DT_VALNUM                         # 
        DT_ADDRRNGLO                      # 
        DT_GNU_HASH                       #  GNU-style hash table.  
        DT_TLSDESC_PLT                    # 
        DT_TLSDESC_GOT                    # 
        DT_GNU_CONFLICT                   #  Start of conflict section 
        DT_GNU_LIBLIST                    #  Library list 
        DT_CONFIG                         #  Configuration information.  
        DT_DEPAUDIT                       #  Dependency auditing.  
        DT_AUDIT                          #  Object auditing.  
        DT_PLTPAD                         #  PLT padding.  
        DT_MOVETAB                        #  Move table.  
        DT_SYMINFO                        #  Syminfo table.  
        DT_ADDRRNGHI                      # 
        DT_ADDRNUM                        # 
        DT_VERSYM                         # 
        DT_RELACOUNT                      # 
        DT_RELCOUNT                       # 
        DT_FLAGS_1                        #  State flags, see DF_1_* below.  
        DT_VERDEF                         #  Address of version definition
        DT_VERDEFNUM                      #  Number of version definitions 
        DT_VERNEED                        #  Address of table with needed
        DT_VERNEEDNUM                     #  Number of needed versions 
        DT_VERSIONTAGNUM                  # 
        DT_AUXILIARY                      #  Shared object to load before self 
        DT_FILTER                         #  Shared object to get values from 
        DT_EXTRANUM                       # 
        DF_ORIGIN                         #  Object may use DF_ORIGIN 
        DF_SYMBOLIC                       #  Symbol resolutions starts here 
        DF_TEXTREL                        #  Object contains text relocations 
        DF_BIND_NOW                       #  No lazy binding for this object 
        DF_STATIC_TLS                     #  Module uses the static TLS model 
        DF_1_NOW                          #  Set RTLD_NOW for this object.  
        DF_1_GLOBAL                       #  Set RTLD_GLOBAL for this object.  
        DF_1_GROUP                        #  Set RTLD_GROUP for this object.  
        DF_1_NODELETE                     #  Set RTLD_NODELETE for this object.
        DF_1_LOADFLTR                     #  Trigger filtee loading at runtime.
        DF_1_INITFIRST                    #  Set RTLD_INITFIRST for this object
        DF_1_NOOPEN                       #  Set RTLD_NOOPEN for this object.  
        DF_1_ORIGIN                       #  $ORIGIN must be handled.  
        DF_1_DIRECT                       #  Direct binding enabled.  
        DF_1_TRANS                        # 
        DF_1_INTERPOSE                    #  Object is used to interpose.  
        DF_1_NODEFLIB                     #  Ignore default lib search path.  
        DF_1_NODUMP                       #  Object can't be dldump'ed.  
        DF_1_CONFALT                      #  Configuration alternative created.
        DF_1_ENDFILTEE                    #  Filtee terminates filters search. 
        DF_1_DISPRELDNE                   #  Disp reloc applied at build time. 
        DF_1_DISPRELPND                   #  Disp reloc applied at run-time.  
        DTF_1_PARINIT                     # 
        DTF_1_CONFEXP                     # 
        DF_P1_LAZYLOAD                    #  Lazyload following object.  
        DF_P1_GROUPPERM                   #  Symbols from next object are not
        VER_DEF_NONE                      #  No version 
        VER_DEF_CURRENT                   #  Current version 
        VER_DEF_NUM                       #  Given version number 
        VER_FLG_BASE                      #  Version definition of file itself 
        VER_FLG_WEAK                      #  Weak version identifier 
        VER_NDX_LOCAL                     #  Symbol is local.  
        VER_NDX_GLOBAL                    #  Symbol is global.  
        VER_NDX_LORESERVE                 #  Beginning of reserved entries.  
        VER_NDX_ELIMINATE                 #  Symbol is to be eliminated.  
        VER_NEED_NONE                     #  No version 
        VER_NEED_CURRENT                  #  Current version 
        VER_NEED_NUM                      #  Given version number 
        VER_FLG_WEAK                      #  Weak version identifier 
        AT_NULL                           #  End of vector 
        AT_IGNORE                         #  Entry should be ignored 
        AT_EXECFD                         #  File descriptor of program 
        AT_PHDR                           #  Program headers for program 
        AT_PHENT                          #  Size of program header entry 
        AT_PHNUM                          #  Number of program headers 
        AT_PAGESZ                         #  System page size 
        AT_BASE                           #  Base address of interpreter 
        AT_FLAGS                          #  Flags 
        AT_ENTRY                          #  Entry point of program 
        AT_NOTELF                         #  Program is not ELF 
        AT_UID                            #  Real uid 
        AT_EUID                           #  Effective uid 
        AT_GID                            #  Real gid 
        AT_EGID                           #  Effective gid 
        AT_CLKTCK                         #  Frequency of times() 
        AT_PLATFORM                       #  String identifying platform.  
        AT_HWCAP                          #  Machine dependent hints about
        AT_FPUCW                          #  Used FPU control word.  
        AT_DCACHEBSIZE                    #  Data cache block size.  
        AT_ICACHEBSIZE                    #  Instruction cache block size.  
        AT_UCACHEBSIZE                    #  Unified cache block size.  
        AT_IGNOREPPC                      #  Entry should be ignored.  
        AT_SECURE                         #  Boolean, was exec setuid-like?  
        AT_BASE_PLATFORM                  #  String identifying real platforms.
        AT_RANDOM                         #  Address of 16 random bytes.  
        AT_EXECFN                         #  Filename of executable.  
        AT_SYSINFO                        # 
        AT_SYSINFO_EHDR                   # 
        AT_L1I_CACHESHAPE                 # 
        AT_L1D_CACHESHAPE                 # 
        AT_L2_CACHESHAPE                  # 
        AT_L3_CACHESHAPE                  # 
        ELF_NOTE_PAGESIZE_HINT            # 
        NT_GNU_ABI_TAG                    # 
        ELF_NOTE_ABI                      #  Old name.  
        ELF_NOTE_OS_LINUX                 # 
        ELF_NOTE_OS_GNU                   # 
        ELF_NOTE_OS_SOLARIS2              # 
        ELF_NOTE_OS_FREEBSD               # 
        NT_GNU_HWCAP                      # 
        NT_GNU_BUILD_ID                   # 
        NT_GNU_GOLD_VERSION               # 
        EF_CPU32                          # 
        R_68K_NONE                        #  No reloc 
        R_68K_32                          #  Direct 32 bit  
        R_68K_16                          #  Direct 16 bit  
        R_68K_8                           #  Direct 8 bit  
        R_68K_PC32                        #  PC relative 32 bit 
        R_68K_PC16                        #  PC relative 16 bit 
        R_68K_PC8                         #  PC relative 8 bit 
        R_68K_GOT32                       #  32 bit PC relative GOT entry 
        R_68K_GOT16                       #  16 bit PC relative GOT entry 
        R_68K_GOT8                        #  8 bit PC relative GOT entry 
        R_68K_GOT32O                      #  32 bit GOT offset 
        R_68K_GOT16O                      #  16 bit GOT offset 
        R_68K_GOT8O                       #  8 bit GOT offset 
        R_68K_PLT32                       #  32 bit PC relative PLT address 
        R_68K_PLT16                       #  16 bit PC relative PLT address 
        R_68K_PLT8                        #  8 bit PC relative PLT address 
        R_68K_PLT32O                      #  32 bit PLT offset 
        R_68K_PLT16O                      #  16 bit PLT offset 
        R_68K_PLT8O                       #  8 bit PLT offset 
        R_68K_COPY                        #  Copy symbol at runtime 
        R_68K_GLOB_DAT                    #  Create GOT entry 
        R_68K_JMP_SLOT                    #  Create PLT entry 
        R_68K_RELATIVE                    #  Adjust by program base 
        R_68K_TLS_GD32                    #  32 bit GOT offset for GD 
        R_68K_TLS_GD16                    #  16 bit GOT offset for GD 
        R_68K_TLS_GD8                     #  8 bit GOT offset for GD 
        R_68K_TLS_LDM32                   #  32 bit GOT offset for LDM 
        R_68K_TLS_LDM16                   #  16 bit GOT offset for LDM 
        R_68K_TLS_LDM8                    #  8 bit GOT offset for LDM 
        R_68K_TLS_LDO32                   #  32 bit module-relative offset 
        R_68K_TLS_LDO16                   #  16 bit module-relative offset 
        R_68K_TLS_LDO8                    #  8 bit module-relative offset 
        R_68K_TLS_IE32                    #  32 bit GOT offset for IE 
        R_68K_TLS_IE16                    #  16 bit GOT offset for IE 
        R_68K_TLS_IE8                     #  8 bit GOT offset for IE 
        R_68K_TLS_LE32                    #  32 bit offset relative to
        R_68K_TLS_LE16                    #  16 bit offset relative to
        R_68K_TLS_LE8                     #  8 bit offset relative to
        R_68K_TLS_DTPMOD32                #  32 bit module number 
        R_68K_TLS_DTPREL32                #  32 bit module-relative offset 
        R_68K_TLS_TPREL32                 #  32 bit TP-relative offset 
        R_68K_NUM                         # 
        R_386_NONE                        #  No reloc 
        R_386_32                          #  Direct 32 bit  
        R_386_PC32                        #  PC relative 32 bit 
        R_386_GOT32                       #  32 bit GOT entry 
        R_386_PLT32                       #  32 bit PLT address 
        R_386_COPY                        #  Copy symbol at runtime 
        R_386_GLOB_DAT                    #  Create GOT entry 
        R_386_JMP_SLOT                    #  Create PLT entry 
        R_386_RELATIVE                    #  Adjust by program base 
        R_386_GOTOFF                      #  32 bit offset to GOT 
        R_386_GOTPC                       #  32 bit PC relative offset to GOT 
        R_386_32PLT                       # 
        R_386_TLS_TPOFF                   #  Offset in static TLS block 
        R_386_TLS_IE                      #  Address of GOT entry for static TLS
        R_386_TLS_GOTIE                   #  GOT entry for static TLS block
        R_386_TLS_LE                      #  Offset relative to static TLS
        R_386_TLS_GD                      #  Direct 32 bit for GNU version of
        R_386_TLS_LDM                     #  Direct 32 bit for GNU version of
        R_386_16                          # 
        R_386_PC16                        # 
        R_386_8                           # 
        R_386_PC8                         # 
        R_386_TLS_GD_32                   #  Direct 32 bit for general dynamic
        R_386_TLS_GD_PUSH                 #  Tag for pushl in GD TLS code 
        R_386_TLS_GD_CALL                 #  Relocation for call to
        R_386_TLS_GD_POP                  #  Tag for popl in GD TLS code 
        R_386_TLS_LDM_32                  #  Direct 32 bit for local dynamic
        R_386_TLS_LDM_PUSH                #  Tag for pushl in LDM TLS code 
        R_386_TLS_LDM_CALL                #  Relocation for call to
        R_386_TLS_LDM_POP                 #  Tag for popl in LDM TLS code 
        R_386_TLS_LDO_32                  #  Offset relative to TLS block 
        R_386_TLS_IE_32                   #  GOT entry for negated static TLS
        R_386_TLS_LE_32                   #  Negated offset relative to static
        R_386_TLS_DTPMOD32                #  ID of module containing symbol 
        R_386_TLS_DTPOFF32                #  Offset in TLS block 
        R_386_TLS_TPOFF32                 #  Negated offset in static TLS block 
        R_386_TLS_GOTDESC                 #  GOT offset for TLS descriptor.  
        R_386_TLS_DESC_CALL               #  Marker of call through TLS
        R_386_TLS_DESC                    #  TLS descriptor containing
        R_386_IRELATIVE                   #  Adjust indirectly by program base 
        R_386_NUM                         # 
        STT_SPARC_REGISTER                #  Global register reserved to app. 
        EF_SPARCV9_MM                     # 
        EF_SPARCV9_TSO                    # 
        EF_SPARCV9_PSO                    # 
        EF_SPARCV9_RMO                    # 
        EF_SPARC_LEDATA                   #  little endian data 
        EF_SPARC_EXT_MASK                 # 
        EF_SPARC_32PLUS                   #  generic V8+ features 
        EF_SPARC_SUN_US1                  #  Sun UltraSPARC1 extensions 
        EF_SPARC_HAL_R1                   #  HAL R1 extensions 
        EF_SPARC_SUN_US3                  #  Sun UltraSPARCIII extensions 
        R_SPARC_NONE                      #  No reloc 
        R_SPARC_8                         #  Direct 8 bit 
        R_SPARC_16                        #  Direct 16 bit 
        R_SPARC_32                        #  Direct 32 bit 
        R_SPARC_DISP8                     #  PC relative 8 bit 
        R_SPARC_DISP16                    #  PC relative 16 bit 
        R_SPARC_DISP32                    #  PC relative 32 bit 
        R_SPARC_WDISP30                   #  PC relative 30 bit shifted 
        R_SPARC_WDISP22                   #  PC relative 22 bit shifted 
        R_SPARC_HI22                      #  High 22 bit 
        R_SPARC_22                        #  Direct 22 bit 
        R_SPARC_13                        #  Direct 13 bit 
        R_SPARC_LO10                      #  Truncated 10 bit 
        R_SPARC_GOT10                     #  Truncated 10 bit GOT entry 
        R_SPARC_GOT13                     #  13 bit GOT entry 
        R_SPARC_GOT22                     #  22 bit GOT entry shifted 
        R_SPARC_PC10                      #  PC relative 10 bit truncated 
        R_SPARC_PC22                      #  PC relative 22 bit shifted 
        R_SPARC_WPLT30                    #  30 bit PC relative PLT address 
        R_SPARC_COPY                      #  Copy symbol at runtime 
        R_SPARC_GLOB_DAT                  #  Create GOT entry 
        R_SPARC_JMP_SLOT                  #  Create PLT entry 
        R_SPARC_RELATIVE                  #  Adjust by program base 
        R_SPARC_UA32                      #  Direct 32 bit unaligned 
        R_SPARC_PLT32                     #  Direct 32 bit ref to PLT entry 
        R_SPARC_HIPLT22                   #  High 22 bit PLT entry 
        R_SPARC_LOPLT10                   #  Truncated 10 bit PLT entry 
        R_SPARC_PCPLT32                   #  PC rel 32 bit ref to PLT entry 
        R_SPARC_PCPLT22                   #  PC rel high 22 bit PLT entry 
        R_SPARC_PCPLT10                   #  PC rel trunc 10 bit PLT entry 
        R_SPARC_10                        #  Direct 10 bit 
        R_SPARC_11                        #  Direct 11 bit 
        R_SPARC_64                        #  Direct 64 bit 
        R_SPARC_OLO10                     #  10bit with secondary 13bit addend 
        R_SPARC_HH22                      #  Top 22 bits of direct 64 bit 
        R_SPARC_HM10                      #  High middle 10 bits of ... 
        R_SPARC_LM22                      #  Low middle 22 bits of ... 
        R_SPARC_PC_HH22                   #  Top 22 bits of pc rel 64 bit 
        R_SPARC_PC_HM10                   #  High middle 10 bit of ... 
        R_SPARC_PC_LM22                   #  Low miggle 22 bits of ... 
        R_SPARC_WDISP16                   #  PC relative 16 bit shifted 
        R_SPARC_WDISP19                   #  PC relative 19 bit shifted 
        R_SPARC_GLOB_JMP                  #  was part of v9 ABI but was removed 
        R_SPARC_7                         #  Direct 7 bit 
        R_SPARC_5                         #  Direct 5 bit 
        R_SPARC_6                         #  Direct 6 bit 
        R_SPARC_DISP64                    #  PC relative 64 bit 
        R_SPARC_PLT64                     #  Direct 64 bit ref to PLT entry 
        R_SPARC_HIX22                     #  High 22 bit complemented 
        R_SPARC_LOX10                     #  Truncated 11 bit complemented 
        R_SPARC_H44                       #  Direct high 12 of 44 bit 
        R_SPARC_M44                       #  Direct mid 22 of 44 bit 
        R_SPARC_L44                       #  Direct low 10 of 44 bit 
        R_SPARC_REGISTER                  #  Global register usage 
        R_SPARC_UA64                      #  Direct 64 bit unaligned 
        R_SPARC_UA16                      #  Direct 16 bit unaligned 
        R_SPARC_TLS_GD_HI22               # 
        R_SPARC_TLS_GD_LO10               # 
        R_SPARC_TLS_GD_ADD                # 
        R_SPARC_TLS_GD_CALL               # 
        R_SPARC_TLS_LDM_HI22              # 
        R_SPARC_TLS_LDM_LO10              # 
        R_SPARC_TLS_LDM_ADD               # 
        R_SPARC_TLS_LDM_CALL              # 
        R_SPARC_TLS_LDO_HIX22             # 
        R_SPARC_TLS_LDO_LOX10             # 
        R_SPARC_TLS_LDO_ADD               # 
        R_SPARC_TLS_IE_HI22               # 
        R_SPARC_TLS_IE_LO10               # 
        R_SPARC_TLS_IE_LD                 # 
        R_SPARC_TLS_IE_LDX                # 
        R_SPARC_TLS_IE_ADD                # 
        R_SPARC_TLS_LE_HIX22              # 
        R_SPARC_TLS_LE_LOX10              # 
        R_SPARC_TLS_DTPMOD32              # 
        R_SPARC_TLS_DTPMOD64              # 
        R_SPARC_TLS_DTPOFF32              # 
        R_SPARC_TLS_DTPOFF64              # 
        R_SPARC_TLS_TPOFF32               # 
        R_SPARC_TLS_TPOFF64               # 
        R_SPARC_GOTDATA_HIX22             # 
        R_SPARC_GOTDATA_LOX10             # 
        R_SPARC_GOTDATA_OP_HIX22          # 
        R_SPARC_GOTDATA_OP_LOX10          # 
        R_SPARC_GOTDATA_OP                # 
        R_SPARC_H34                       # 
        R_SPARC_SIZE32                    # 
        R_SPARC_SIZE64                    # 
        R_SPARC_WDISP10                   # 
        R_SPARC_JMP_IREL                  # 
        R_SPARC_IRELATIVE                 # 
        R_SPARC_GNU_VTINHERIT             # 
        R_SPARC_GNU_VTENTRY               # 
        R_SPARC_REV32                     # 
        R_SPARC_NUM                       # 
        DT_SPARC_REGISTER                 # 
        DT_SPARC_NUM                      # 
        EF_MIPS_NOREORDER                 #  A .noreorder directive was used 
        EF_MIPS_PIC                       #  Contains PIC code 
        EF_MIPS_CPIC                      #  Uses PIC calling sequence 
        EF_MIPS_XGOT                      # 
        EF_MIPS_64BIT_WHIRL               # 
        EF_MIPS_ABI2                      # 
        EF_MIPS_ABI_ON32                  # 
        EF_MIPS_ARCH                      #  MIPS architecture level 
        EF_MIPS_ARCH_1                    #  -mips1 code.  
        EF_MIPS_ARCH_2                    #  -mips2 code.  
        EF_MIPS_ARCH_3                    #  -mips3 code.  
        EF_MIPS_ARCH_4                    #  -mips4 code.  
        EF_MIPS_ARCH_5                    #  -mips5 code.  
        EF_MIPS_ARCH_32                   #  MIPS32 code.  
        EF_MIPS_ARCH_64                   #  MIPS64 code.  
        E_MIPS_ARCH_1                     #  -mips1 code.  
        E_MIPS_ARCH_2                     #  -mips2 code.  
        E_MIPS_ARCH_3                     #  -mips3 code.  
        E_MIPS_ARCH_4                     #  -mips4 code.  
        E_MIPS_ARCH_5                     #  -mips5 code.  
        E_MIPS_ARCH_32                    #  MIPS32 code.  
        E_MIPS_ARCH_64                    #  MIPS64 code.  
        SHN_MIPS_ACOMMON                  #  Allocated common symbols 
        SHN_MIPS_TEXT                     #  Allocated test symbols.  
        SHN_MIPS_DATA                     #  Allocated data symbols.  
        SHN_MIPS_SCOMMON                  #  Small common symbols 
        SHN_MIPS_SUNDEFINED               #  Small undefined symbols 
        SHT_MIPS_LIBLIST                  #  Shared objects used in link 
        SHT_MIPS_MSYM                     # 
        SHT_MIPS_CONFLICT                 #  Conflicting symbols 
        SHT_MIPS_GPTAB                    #  Global data area sizes 
        SHT_MIPS_UCODE                    #  Reserved for SGI/MIPS compilers 
        SHT_MIPS_DEBUG                    #  MIPS ECOFF debugging information
        SHT_MIPS_REGINFO                  #  Register usage information 
        SHT_MIPS_PACKAGE                  # 
        SHT_MIPS_PACKSYM                  # 
        SHT_MIPS_RELD                     # 
        SHT_MIPS_IFACE                    # 
        SHT_MIPS_CONTENT                  # 
        SHT_MIPS_OPTIONS                  #  Miscellaneous options.  
        SHT_MIPS_SHDR                     # 
        SHT_MIPS_FDESC                    # 
        SHT_MIPS_EXTSYM                   # 
        SHT_MIPS_DENSE                    # 
        SHT_MIPS_PDESC                    # 
        SHT_MIPS_LOCSYM                   # 
        SHT_MIPS_AUXSYM                   # 
        SHT_MIPS_OPTSYM                   # 
        SHT_MIPS_LOCSTR                   # 
        SHT_MIPS_LINE                     # 
        SHT_MIPS_RFDESC                   # 
        SHT_MIPS_DELTASYM                 # 
        SHT_MIPS_DELTAINST                # 
        SHT_MIPS_DELTACLASS               # 
        SHT_MIPS_DWARF                    #  DWARF debugging information.  
        SHT_MIPS_DELTADECL                # 
        SHT_MIPS_SYMBOL_LIB               # 
        SHT_MIPS_EVENTS                   #  Event section.  
        SHT_MIPS_TRANSLATE                # 
        SHT_MIPS_PIXIE                    # 
        SHT_MIPS_XLATE                    # 
        SHT_MIPS_XLATE_DEBUG              # 
        SHT_MIPS_WHIRL                    # 
        SHT_MIPS_EH_REGION                # 
        SHT_MIPS_XLATE_OLD                # 
        SHT_MIPS_PDR_EXCEPTION            # 
        SHF_MIPS_GPREL                    #  Must be part of global data area 
        SHF_MIPS_MERGE                    # 
        SHF_MIPS_ADDR                     # 
        SHF_MIPS_STRINGS                  # 
        SHF_MIPS_NOSTRIP                  # 
        SHF_MIPS_LOCAL                    # 
        SHF_MIPS_NAMES                    # 
        SHF_MIPS_NODUPE                   # 
        STO_MIPS_DEFAULT                  # 
        STO_MIPS_INTERNAL                 # 
        STO_MIPS_HIDDEN                   # 
        STO_MIPS_PROTECTED                # 
        STO_MIPS_PLT                      # 
        STO_MIPS_SC_ALIGN_UNUSED          # 
        STB_MIPS_SPLIT_COMMON             # 
        ODK_NULL                          #  Undefined.  
        ODK_REGINFO                       #  Register usage information.  
        ODK_EXCEPTIONS                    #  Exception processing options.  
        ODK_PAD                           #  Section padding options.  
        ODK_HWPATCH                       #  Hardware workarounds performed 
        ODK_FILL                          #  record the fill value used by the linker. 
        ODK_TAGS                          #  reserve space for desktop tools to write. 
        ODK_HWAND                         #  HW workarounds.  'AND' bits when merging. 
        ODK_HWOR                          #  HW workarounds.  'OR' bits when merging.  
        OEX_FPU_MIN                       #  FPE's which MUST be enabled.  
        OEX_FPU_MAX                       #  FPE's which MAY be enabled.  
        OEX_PAGE0                         #  page zero must be mapped.  
        OEX_SMM                           #  Force sequential memory mode?  
        OEX_FPDBUG                        #  Force floating point debug mode?  
        OEX_PRECISEFP                     # 
        OEX_DISMISS                       #  Dismiss invalid address faults?  
        OEX_FPU_INVAL                     # 
        OEX_FPU_DIV0                      # 
        OEX_FPU_OFLO                      # 
        OEX_FPU_UFLO                      # 
        OEX_FPU_INEX                      # 
        OHW_R4KEOP                        #  R4000 end-of-page patch.  
        OHW_R8KPFETCH                     #  may need R8000 prefetch patch.  
        OHW_R5KEOP                        #  R5000 end-of-page patch.  
        OHW_R5KCVTL                       #  R5000 cvt.[ds].l bug.  clean=1.  
        OPAD_PREFIX                       # 
        OPAD_POSTFIX                      # 
        OPAD_SYMBOL                       # 
        OHWA0_R4KEOP_CHECKED              # 
        OHWA1_R4KEOP_CLEAN                # 
        R_MIPS_NONE                       #  No reloc 
        R_MIPS_16                         #  Direct 16 bit 
        R_MIPS_32                         #  Direct 32 bit 
        R_MIPS_REL32                      #  PC relative 32 bit 
        R_MIPS_26                         #  Direct 26 bit shifted 
        R_MIPS_HI16                       #  High 16 bit 
        R_MIPS_LO16                       #  Low 16 bit 
        R_MIPS_GPREL16                    #  GP relative 16 bit 
        R_MIPS_LITERAL                    #  16 bit literal entry 
        R_MIPS_GOT16                      #  16 bit GOT entry 
        R_MIPS_PC16                       #  PC relative 16 bit 
        R_MIPS_CALL16                     #  16 bit GOT entry for function 
        R_MIPS_GPREL32                    #  GP relative 32 bit 
        R_MIPS_SHIFT5                     # 
        R_MIPS_SHIFT6                     # 
        R_MIPS_64                         # 
        R_MIPS_GOT_DISP                   # 
        R_MIPS_GOT_PAGE                   # 
        R_MIPS_GOT_OFST                   # 
        R_MIPS_GOT_HI16                   # 
        R_MIPS_GOT_LO16                   # 
        R_MIPS_SUB                        # 
        R_MIPS_INSERT_A                   # 
        R_MIPS_INSERT_B                   # 
        R_MIPS_DELETE                     # 
        R_MIPS_HIGHER                     # 
        R_MIPS_HIGHEST                    # 
        R_MIPS_CALL_HI16                  # 
        R_MIPS_CALL_LO16                  # 
        R_MIPS_SCN_DISP                   # 
        R_MIPS_REL16                      # 
        R_MIPS_ADD_IMMEDIATE              # 
        R_MIPS_PJUMP                      # 
        R_MIPS_RELGOT                     # 
        R_MIPS_JALR                       # 
        R_MIPS_TLS_DTPMOD32               #  Module number 32 bit 
        R_MIPS_TLS_DTPREL32               #  Module-relative offset 32 bit 
        R_MIPS_TLS_DTPMOD64               #  Module number 64 bit 
        R_MIPS_TLS_DTPREL64               #  Module-relative offset 64 bit 
        R_MIPS_TLS_GD                     #  16 bit GOT offset for GD 
        R_MIPS_TLS_LDM                    #  16 bit GOT offset for LDM 
        R_MIPS_TLS_DTPREL_HI16            #  Module-relative offset, high 16 bits 
        R_MIPS_TLS_DTPREL_LO16            #  Module-relative offset, low 16 bits 
        R_MIPS_TLS_GOTTPREL               #  16 bit GOT offset for IE 
        R_MIPS_TLS_TPREL32                #  TP-relative offset, 32 bit 
        R_MIPS_TLS_TPREL64                #  TP-relative offset, 64 bit 
        R_MIPS_TLS_TPREL_HI16             #  TP-relative offset, high 16 bits 
        R_MIPS_TLS_TPREL_LO16             #  TP-relative offset, low 16 bits 
        R_MIPS_GLOB_DAT                   # 
        R_MIPS_COPY                       # 
        R_MIPS_JUMP_SLOT                  # 
        R_MIPS_NUM                        # 
        PT_MIPS_REGINFO                   #  Register usage information 
        PT_MIPS_RTPROC                    #  Runtime procedure table. 
        PT_MIPS_OPTIONS                   # 
        PF_MIPS_LOCAL                     # 
        DT_MIPS_RLD_VERSION               #  Runtime linker interface version 
        DT_MIPS_TIME_STAMP                #  Timestamp 
        DT_MIPS_ICHECKSUM                 #  Checksum 
        DT_MIPS_IVERSION                  #  Version string (string tbl index) 
        DT_MIPS_FLAGS                     #  Flags 
        DT_MIPS_BASE_ADDRESS              #  Base address 
        DT_MIPS_MSYM                      # 
        DT_MIPS_CONFLICT                  #  Address of CONFLICT section 
        DT_MIPS_LIBLIST                   #  Address of LIBLIST section 
        DT_MIPS_LOCAL_GOTNO               #  Number of local GOT entries 
        DT_MIPS_CONFLICTNO                #  Number of CONFLICT entries 
        DT_MIPS_LIBLISTNO                 #  Number of LIBLIST entries 
        DT_MIPS_SYMTABNO                  #  Number of DYNSYM entries 
        DT_MIPS_UNREFEXTNO                #  First external DYNSYM 
        DT_MIPS_GOTSYM                    #  First GOT entry in DYNSYM 
        DT_MIPS_HIPAGENO                  #  Number of GOT page table entries 
        DT_MIPS_RLD_MAP                   #  Address of run time loader map.  
        DT_MIPS_DELTA_CLASS               #  Delta C++ class definition.  
        DT_MIPS_DELTA_CLASS_NO            #  Number of entries in
        DT_MIPS_DELTA_INSTANCE            #  Delta C++ class instances.  
        DT_MIPS_DELTA_INSTANCE_NO         #  Number of entries in
        DT_MIPS_DELTA_RELOC               #  Delta relocations.  
        DT_MIPS_DELTA_RELOC_NO            #  Number of entries in
        DT_MIPS_DELTA_SYM                 #  Delta symbols that Delta
        DT_MIPS_DELTA_SYM_NO              #  Number of entries in
        DT_MIPS_DELTA_CLASSSYM            #  Delta symbols that hold the
        DT_MIPS_DELTA_CLASSSYM_NO         #  Number of entries in
        DT_MIPS_CXX_FLAGS                 #  Flags indicating for C++ flavor.  
        DT_MIPS_PIXIE_INIT                # 
        DT_MIPS_SYMBOL_LIB                # 
        DT_MIPS_LOCALPAGE_GOTIDX          # 
        DT_MIPS_LOCAL_GOTIDX              # 
        DT_MIPS_HIDDEN_GOTIDX             # 
        DT_MIPS_PROTECTED_GOTIDX          # 
        DT_MIPS_OPTIONS                   #  Address of .options.  
        DT_MIPS_INTERFACE                 #  Address of .interface.  
        DT_MIPS_DYNSTR_ALIGN              # 
        DT_MIPS_INTERFACE_SIZE            #  Size of the .interface section. 
        DT_MIPS_RLD_TEXT_RESOLVE_ADDR     #  Address of rld_text_rsolve
        DT_MIPS_PERF_SUFFIX               #  Default suffix of dso to be added
        DT_MIPS_COMPACT_SIZE              #  (O32)Size of compact rel section. 
        DT_MIPS_GP_VALUE                  #  GP value for aux GOTs.  
        DT_MIPS_AUX_DYNAMIC               #  Address of aux .dynamic.  
        DT_MIPS_PLTGOT                    # 
        DT_MIPS_RWPLT                     # 
        DT_MIPS_NUM                       # 
        RHF_NONE                          #  No flags 
        RHF_QUICKSTART                    #  Use quickstart 
        RHF_NOTPOT                        #  Hash size not power of 2 
        RHF_NO_LIBRARY_REPLACEMENT        #  Ignore LD_LIBRARY_PATH 
        RHF_NO_MOVE                       # 
        RHF_SGI_ONLY                      # 
        RHF_GUARANTEE_INIT                # 
        RHF_DELTA_C_PLUS_PLUS             # 
        RHF_GUARANTEE_START_INIT          # 
        RHF_PIXIE                         # 
        RHF_DEFAULT_DELAY_LOAD            # 
        RHF_REQUICKSTART                  # 
        RHF_REQUICKSTARTED                # 
        RHF_CORD                          # 
        RHF_NO_UNRES_UNDEF                # 
        RHF_RLD_ORDER_SAFE                # 
        LL_NONE                           # 
        LL_EXACT_MATCH                    #  Require exact match 
        LL_IGNORE_INT_VER                 #  Ignore interface version 
        LL_REQUIRE_MINOR                  # 
        LL_EXPORTS                        # 
        LL_DELAY_LOAD                     # 
        LL_DELTA                          # 
        EF_PARISC_TRAPNIL                 #  Trap nil pointer dereference.  
        EF_PARISC_EXT                     #  Program uses arch. extensions. 
        EF_PARISC_LSB                     #  Program expects little endian. 
        EF_PARISC_WIDE                    #  Program expects wide mode.  
        EF_PARISC_NO_KABP                 #  No kernel assisted branch
        EF_PARISC_LAZYSWAP                #  Allow lazy swapping.  
        EF_PARISC_ARCH                    #  Architecture version.  
        EFA_PARISC_1_0                    #  PA-RISC 1.0 big-endian.  
        EFA_PARISC_1_1                    #  PA-RISC 1.1 big-endian.  
        EFA_PARISC_2_0                    #  PA-RISC 2.0 big-endian.  
        SHN_PARISC_ANSI_COMMON            #  Section for tenatively declared
        SHN_PARISC_HUGE_COMMON            #  Common blocks in huge model.  
        SHT_PARISC_EXT                    #  Contains product specific ext. 
        SHT_PARISC_UNWIND                 #  Unwind information.  
        SHT_PARISC_DOC                    #  Debug info for optimized code. 
        SHF_PARISC_SHORT                  #  Section with short addressing. 
        SHF_PARISC_HUGE                   #  Section far from gp.  
        SHF_PARISC_SBP                    #  Static branch prediction code. 
        STT_PARISC_MILLICODE              #  Millicode function entry point.  
        STT_HP_OPAQUE                     # 
        STT_HP_STUB                       # 
        R_PARISC_NONE                     #  No reloc.  
        R_PARISC_DIR32                    #  Direct 32-bit reference.  
        R_PARISC_DIR21L                   #  Left 21 bits of eff. address.  
        R_PARISC_DIR17R                   #  Right 17 bits of eff. address.  
        R_PARISC_DIR17F                   #  17 bits of eff. address.  
        R_PARISC_DIR14R                   #  Right 14 bits of eff. address.  
        R_PARISC_PCREL32                  #  32-bit rel. address.  
        R_PARISC_PCREL21L                 #  Left 21 bits of rel. address.  
        R_PARISC_PCREL17R                 #  Right 17 bits of rel. address.  
        R_PARISC_PCREL17F                 #  17 bits of rel. address.  
        R_PARISC_PCREL14R                 #  Right 14 bits of rel. address.  
        R_PARISC_DPREL21L                 #  Left 21 bits of rel. address.  
        R_PARISC_DPREL14R                 #  Right 14 bits of rel. address.  
        R_PARISC_GPREL21L                 #  GP-relative, left 21 bits.  
        R_PARISC_GPREL14R                 #  GP-relative, right 14 bits.  
        R_PARISC_LTOFF21L                 #  LT-relative, left 21 bits.  
        R_PARISC_LTOFF14R                 #  LT-relative, right 14 bits.  
        R_PARISC_SECREL32                 #  32 bits section rel. address.  
        R_PARISC_SEGBASE                  #  No relocation, set segment base.  
        R_PARISC_SEGREL32                 #  32 bits segment rel. address.  
        R_PARISC_PLTOFF21L                #  PLT rel. address, left 21 bits.  
        R_PARISC_PLTOFF14R                #  PLT rel. address, right 14 bits.  
        R_PARISC_LTOFF_FPTR32             #  32 bits LT-rel. function pointer. 
        R_PARISC_LTOFF_FPTR21L            #  LT-rel. fct ptr, left 21 bits. 
        R_PARISC_LTOFF_FPTR14R            #  LT-rel. fct ptr, right 14 bits. 
        R_PARISC_FPTR64                   #  64 bits function address.  
        R_PARISC_PLABEL32                 #  32 bits function address.  
        R_PARISC_PLABEL21L                #  Left 21 bits of fdesc address.  
        R_PARISC_PLABEL14R                #  Right 14 bits of fdesc address.  
        R_PARISC_PCREL64                  #  64 bits PC-rel. address.  
        R_PARISC_PCREL22F                 #  22 bits PC-rel. address.  
        R_PARISC_PCREL14WR                #  PC-rel. address, right 14 bits.  
        R_PARISC_PCREL14DR                #  PC rel. address, right 14 bits.  
        R_PARISC_PCREL16F                 #  16 bits PC-rel. address.  
        R_PARISC_PCREL16WF                #  16 bits PC-rel. address.  
        R_PARISC_PCREL16DF                #  16 bits PC-rel. address.  
        R_PARISC_DIR64                    #  64 bits of eff. address.  
        R_PARISC_DIR14WR                  #  14 bits of eff. address.  
        R_PARISC_DIR14DR                  #  14 bits of eff. address.  
        R_PARISC_DIR16F                   #  16 bits of eff. address.  
        R_PARISC_DIR16WF                  #  16 bits of eff. address.  
        R_PARISC_DIR16DF                  #  16 bits of eff. address.  
        R_PARISC_GPREL64                  #  64 bits of GP-rel. address.  
        R_PARISC_GPREL14WR                #  GP-rel. address, right 14 bits.  
        R_PARISC_GPREL14DR                #  GP-rel. address, right 14 bits.  
        R_PARISC_GPREL16F                 #  16 bits GP-rel. address.  
        R_PARISC_GPREL16WF                #  16 bits GP-rel. address.  
        R_PARISC_GPREL16DF                #  16 bits GP-rel. address.  
        R_PARISC_LTOFF64                  #  64 bits LT-rel. address.  
        R_PARISC_LTOFF14WR                #  LT-rel. address, right 14 bits.  
        R_PARISC_LTOFF14DR                #  LT-rel. address, right 14 bits.  
        R_PARISC_LTOFF16F                 #  16 bits LT-rel. address.  
        R_PARISC_LTOFF16WF                #  16 bits LT-rel. address.  
        R_PARISC_LTOFF16DF                #  16 bits LT-rel. address.  
        R_PARISC_SECREL64                 #  64 bits section rel. address.  
        R_PARISC_SEGREL64                 #  64 bits segment rel. address.  
        R_PARISC_PLTOFF14WR               #  PLT-rel. address, right 14 bits.  
        R_PARISC_PLTOFF14DR               #  PLT-rel. address, right 14 bits.  
        R_PARISC_PLTOFF16F                #  16 bits LT-rel. address.  
        R_PARISC_PLTOFF16WF               #  16 bits PLT-rel. address.  
        R_PARISC_PLTOFF16DF               #  16 bits PLT-rel. address.  
        R_PARISC_LTOFF_FPTR64             #  64 bits LT-rel. function ptr.  
        R_PARISC_LTOFF_FPTR14WR           #  LT-rel. fct. ptr., right 14 bits. 
        R_PARISC_LTOFF_FPTR14DR           #  LT-rel. fct. ptr., right 14 bits. 
        R_PARISC_LTOFF_FPTR16F            #  16 bits LT-rel. function ptr.  
        R_PARISC_LTOFF_FPTR16WF           #  16 bits LT-rel. function ptr.  
        R_PARISC_LTOFF_FPTR16DF           #  16 bits LT-rel. function ptr.  
        R_PARISC_LORESERVE                # 
        R_PARISC_COPY                     #  Copy relocation.  
        R_PARISC_IPLT                     #  Dynamic reloc, imported PLT 
        R_PARISC_EPLT                     #  Dynamic reloc, exported PLT 
        R_PARISC_TPREL32                  #  32 bits TP-rel. address.  
        R_PARISC_TPREL21L                 #  TP-rel. address, left 21 bits.  
        R_PARISC_TPREL14R                 #  TP-rel. address, right 14 bits.  
        R_PARISC_LTOFF_TP21L              #  LT-TP-rel. address, left 21 bits. 
        R_PARISC_LTOFF_TP14R              #  LT-TP-rel. address, right 14 bits.
        R_PARISC_LTOFF_TP14F              #  14 bits LT-TP-rel. address.  
        R_PARISC_TPREL64                  #  64 bits TP-rel. address.  
        R_PARISC_TPREL14WR                #  TP-rel. address, right 14 bits.  
        R_PARISC_TPREL14DR                #  TP-rel. address, right 14 bits.  
        R_PARISC_TPREL16F                 #  16 bits TP-rel. address.  
        R_PARISC_TPREL16WF                #  16 bits TP-rel. address.  
        R_PARISC_TPREL16DF                #  16 bits TP-rel. address.  
        R_PARISC_LTOFF_TP64               #  64 bits LT-TP-rel. address.  
        R_PARISC_LTOFF_TP14WR             #  LT-TP-rel. address, right 14 bits.
        R_PARISC_LTOFF_TP14DR             #  LT-TP-rel. address, right 14 bits.
        R_PARISC_LTOFF_TP16F              #  16 bits LT-TP-rel. address.  
        R_PARISC_LTOFF_TP16WF             #  16 bits LT-TP-rel. address.  
        R_PARISC_LTOFF_TP16DF             #  16 bits LT-TP-rel. address.  
        R_PARISC_GNU_VTENTRY              # 
        R_PARISC_GNU_VTINHERIT            # 
        R_PARISC_TLS_GD21L                #  GD 21-bit left.  
        R_PARISC_TLS_GD14R                #  GD 14-bit right.  
        R_PARISC_TLS_GDCALL               #  GD call to __t_g_a.  
        R_PARISC_TLS_LDM21L               #  LD module 21-bit left.  
        R_PARISC_TLS_LDM14R               #  LD module 14-bit right.  
        R_PARISC_TLS_LDMCALL              #  LD module call to __t_g_a.  
        R_PARISC_TLS_LDO21L               #  LD offset 21-bit left.  
        R_PARISC_TLS_LDO14R               #  LD offset 14-bit right.  
        R_PARISC_TLS_DTPMOD32             #  DTP module 32-bit.  
        R_PARISC_TLS_DTPMOD64             #  DTP module 64-bit.  
        R_PARISC_TLS_DTPOFF32             #  DTP offset 32-bit.  
        R_PARISC_TLS_DTPOFF64             #  DTP offset 32-bit.  
        R_PARISC_TLS_LE21L                # 
        R_PARISC_TLS_LE14R                # 
        R_PARISC_TLS_IE21L                # 
        R_PARISC_TLS_IE14R                # 
        R_PARISC_TLS_TPREL32              # 
        R_PARISC_TLS_TPREL64              # 
        R_PARISC_HIRESERVE                # 
        PT_HP_TLS                         # 
        PT_HP_CORE_NONE                   # 
        PT_HP_CORE_VERSION                # 
        PT_HP_CORE_KERNEL                 # 
        PT_HP_CORE_COMM                   # 
        PT_HP_CORE_PROC                   # 
        PT_HP_CORE_LOADABLE               # 
        PT_HP_CORE_STACK                  # 
        PT_HP_CORE_SHM                    # 
        PT_HP_CORE_MMF                    # 
        PT_HP_PARALLEL                    # 
        PT_HP_FASTBIND                    # 
        PT_HP_OPT_ANNOT                   # 
        PT_HP_HSL_ANNOT                   # 
        PT_HP_STACK                       # 
        PT_PARISC_ARCHEXT                 # 
        PT_PARISC_UNWIND                  # 
        PF_PARISC_SBP                     # 
        PF_HP_PAGE_SIZE                   # 
        PF_HP_FAR_SHARED                  # 
        PF_HP_NEAR_SHARED                 # 
        PF_HP_CODE                        # 
        PF_HP_MODIFY                      # 
        PF_HP_LAZYSWAP                    # 
        PF_HP_SBP                         # 
        EF_ALPHA_32BIT                    #  All addresses must be < 2GB.  
        EF_ALPHA_CANRELAX                 #  Relocations for relaxing exist.  
        SHT_ALPHA_DEBUG                   # 
        SHT_ALPHA_REGINFO                 # 
        SHF_ALPHA_GPREL                   # 
        STO_ALPHA_NOPV                    #  No PV required.  
        STO_ALPHA_STD_GPLOAD              #  PV only used for initial ldgp.  
        R_ALPHA_NONE                      #  No reloc 
        R_ALPHA_REFLONG                   #  Direct 32 bit 
        R_ALPHA_REFQUAD                   #  Direct 64 bit 
        R_ALPHA_GPREL32                   #  GP relative 32 bit 
        R_ALPHA_LITERAL                   #  GP relative 16 bit w/optimization 
        R_ALPHA_LITUSE                    #  Optimization hint for LITERAL 
        R_ALPHA_GPDISP                    #  Add displacement to GP 
        R_ALPHA_BRADDR                    #  PC+4 relative 23 bit shifted 
        R_ALPHA_HINT                      #  PC+4 relative 16 bit shifted 
        R_ALPHA_SREL16                    #  PC relative 16 bit 
        R_ALPHA_SREL32                    #  PC relative 32 bit 
        R_ALPHA_SREL64                    #  PC relative 64 bit 
        R_ALPHA_GPRELHIGH                 #  GP relative 32 bit, high 16 bits 
        R_ALPHA_GPRELLOW                  #  GP relative 32 bit, low 16 bits 
        R_ALPHA_GPREL16                   #  GP relative 16 bit 
        R_ALPHA_COPY                      #  Copy symbol at runtime 
        R_ALPHA_GLOB_DAT                  #  Create GOT entry 
        R_ALPHA_JMP_SLOT                  #  Create PLT entry 
        R_ALPHA_RELATIVE                  #  Adjust by program base 
        R_ALPHA_TLS_GD_HI                 # 
        R_ALPHA_TLSGD                     # 
        R_ALPHA_TLS_LDM                   # 
        R_ALPHA_DTPMOD64                  # 
        R_ALPHA_GOTDTPREL                 # 
        R_ALPHA_DTPREL64                  # 
        R_ALPHA_DTPRELHI                  # 
        R_ALPHA_DTPRELLO                  # 
        R_ALPHA_DTPREL16                  # 
        R_ALPHA_GOTTPREL                  # 
        R_ALPHA_TPREL64                   # 
        R_ALPHA_TPRELHI                   # 
        R_ALPHA_TPRELLO                   # 
        R_ALPHA_TPREL16                   # 
        R_ALPHA_NUM                       # 
        LITUSE_ALPHA_ADDR                 # 
        LITUSE_ALPHA_BASE                 # 
        LITUSE_ALPHA_BYTOFF               # 
        LITUSE_ALPHA_JSR                  # 
        LITUSE_ALPHA_TLS_GD               # 
        LITUSE_ALPHA_TLS_LDM              # 
        DT_ALPHA_PLTRO                    # 
        DT_ALPHA_NUM                      # 
        EF_PPC_EMB                        #  PowerPC embedded flag 
        EF_PPC_RELOCATABLE                #  PowerPC -mrelocatable flag
        EF_PPC_RELOCATABLE_LIB            #  PowerPC -mrelocatable-lib
        R_PPC_NONE                        # 
        R_PPC_ADDR32                      #  32bit absolute address 
        R_PPC_ADDR24                      #  26bit address, 2 bits ignored.  
        R_PPC_ADDR16                      #  16bit absolute address 
        R_PPC_ADDR16_LO                   #  lower 16bit of absolute address 
        R_PPC_ADDR16_HI                   #  high 16bit of absolute address 
        R_PPC_ADDR16_HA                   #  adjusted high 16bit 
        R_PPC_ADDR14                      #  16bit address, 2 bits ignored 
        R_PPC_ADDR14_BRTAKEN              # 
        R_PPC_ADDR14_BRNTAKEN             # 
        R_PPC_REL24                       #  PC relative 26 bit 
        R_PPC_REL14                       #  PC relative 16 bit 
        R_PPC_REL14_BRTAKEN               # 
        R_PPC_REL14_BRNTAKEN              # 
        R_PPC_GOT16                       # 
        R_PPC_GOT16_LO                    # 
        R_PPC_GOT16_HI                    # 
        R_PPC_GOT16_HA                    # 
        R_PPC_PLTREL24                    # 
        R_PPC_COPY                        # 
        R_PPC_GLOB_DAT                    # 
        R_PPC_JMP_SLOT                    # 
        R_PPC_RELATIVE                    # 
        R_PPC_LOCAL24PC                   # 
        R_PPC_UADDR32                     # 
        R_PPC_UADDR16                     # 
        R_PPC_REL32                       # 
        R_PPC_PLT32                       # 
        R_PPC_PLTREL32                    # 
        R_PPC_PLT16_LO                    # 
        R_PPC_PLT16_HI                    # 
        R_PPC_PLT16_HA                    # 
        R_PPC_SDAREL16                    # 
        R_PPC_SECTOFF                     # 
        R_PPC_SECTOFF_LO                  # 
        R_PPC_SECTOFF_HI                  # 
        R_PPC_SECTOFF_HA                  # 
        R_PPC_TLS                         #  none	(sym+add)@tls 
        R_PPC_DTPMOD32                    #  word32	(sym+add)@dtpmod 
        R_PPC_TPREL16                     #  half16*	(sym+add)@tprel 
        R_PPC_TPREL16_LO                  #  half16	(sym+add)@tprel@l 
        R_PPC_TPREL16_HI                  #  half16	(sym+add)@tprel@h 
        R_PPC_TPREL16_HA                  #  half16	(sym+add)@tprel@ha 
        R_PPC_TPREL32                     #  word32	(sym+add)@tprel 
        R_PPC_DTPREL16                    #  half16*	(sym+add)@dtprel 
        R_PPC_DTPREL16_LO                 #  half16	(sym+add)@dtprel@l 
        R_PPC_DTPREL16_HI                 #  half16	(sym+add)@dtprel@h 
        R_PPC_DTPREL16_HA                 #  half16	(sym+add)@dtprel@ha 
        R_PPC_DTPREL32                    #  word32	(sym+add)@dtprel 
        R_PPC_GOT_TLSGD16                 #  half16*	(sym+add)@got@tlsgd 
        R_PPC_GOT_TLSGD16_LO              #  half16	(sym+add)@got@tlsgd@l 
        R_PPC_GOT_TLSGD16_HI              #  half16	(sym+add)@got@tlsgd@h 
        R_PPC_GOT_TLSGD16_HA              #  half16	(sym+add)@got@tlsgd@ha 
        R_PPC_GOT_TLSLD16                 #  half16*	(sym+add)@got@tlsld 
        R_PPC_GOT_TLSLD16_LO              #  half16	(sym+add)@got@tlsld@l 
        R_PPC_GOT_TLSLD16_HI              #  half16	(sym+add)@got@tlsld@h 
        R_PPC_GOT_TLSLD16_HA              #  half16	(sym+add)@got@tlsld@ha 
        R_PPC_GOT_TPREL16                 #  half16*	(sym+add)@got@tprel 
        R_PPC_GOT_TPREL16_LO              #  half16	(sym+add)@got@tprel@l 
        R_PPC_GOT_TPREL16_HI              #  half16	(sym+add)@got@tprel@h 
        R_PPC_GOT_TPREL16_HA              #  half16	(sym+add)@got@tprel@ha 
        R_PPC_GOT_DTPREL16                #  half16*	(sym+add)@got@dtprel 
        R_PPC_GOT_DTPREL16_LO             #  half16*	(sym+add)@got@dtprel@l 
        R_PPC_GOT_DTPREL16_HI             #  half16*	(sym+add)@got@dtprel@h 
        R_PPC_GOT_DTPREL16_HA             #  half16*	(sym+add)@got@dtprel@ha 
        R_PPC_EMB_NADDR32                 # 
        R_PPC_EMB_NADDR16                 # 
        R_PPC_EMB_NADDR16_LO              # 
        R_PPC_EMB_NADDR16_HI              # 
        R_PPC_EMB_NADDR16_HA              # 
        R_PPC_EMB_SDAI16                  # 
        R_PPC_EMB_SDA2I16                 # 
        R_PPC_EMB_SDA2REL                 # 
        R_PPC_EMB_SDA21                   #  16 bit offset in SDA 
        R_PPC_EMB_MRKREF                  # 
        R_PPC_EMB_RELSEC16                # 
        R_PPC_EMB_RELST_LO                # 
        R_PPC_EMB_RELST_HI                # 
        R_PPC_EMB_RELST_HA                # 
        R_PPC_EMB_BIT_FLD                 # 
        R_PPC_EMB_RELSDA                  #  16 bit relative offset in SDA 
        R_PPC_DIAB_SDA21_LO               #  like EMB_SDA21, but lower 16 bit 
        R_PPC_DIAB_SDA21_HI               #  like EMB_SDA21, but high 16 bit 
        R_PPC_DIAB_SDA21_HA               #  like EMB_SDA21, adjusted high 16 
        R_PPC_DIAB_RELSDA_LO              #  like EMB_RELSDA, but lower 16 bit 
        R_PPC_DIAB_RELSDA_HI              #  like EMB_RELSDA, but high 16 bit 
        R_PPC_DIAB_RELSDA_HA              #  like EMB_RELSDA, adjusted high 16 
        R_PPC_IRELATIVE                   # 
        R_PPC_REL16                       #  half16   (sym+add-.) 
        R_PPC_REL16_LO                    #  half16   (sym+add-.)@l 
        R_PPC_REL16_HI                    #  half16   (sym+add-.)@h 
        R_PPC_REL16_HA                    #  half16   (sym+add-.)@ha 
        R_PPC_TOC16                       # 
        DT_PPC_GOT                        # 
        DT_PPC_NUM                        # 
        R_PPC64_NONE                      # 
        R_PPC64_ADDR32                    #  32bit absolute address 
        R_PPC64_ADDR24                    #  26bit address, word aligned 
        R_PPC64_ADDR16                    #  16bit absolute address 
        R_PPC64_ADDR16_LO                 #  lower 16bits of address 
        R_PPC64_ADDR16_HI                 #  high 16bits of address. 
        R_PPC64_ADDR16_HA                 #  adjusted high 16bits.  
        R_PPC64_ADDR14                    #  16bit address, word aligned 
        R_PPC64_ADDR14_BRTAKEN            # 
        R_PPC64_ADDR14_BRNTAKEN           # 
        R_PPC64_REL24                     #  PC-rel. 26 bit, word aligned 
        R_PPC64_REL14                     #  PC relative 16 bit 
        R_PPC64_REL14_BRTAKEN             # 
        R_PPC64_REL14_BRNTAKEN            # 
        R_PPC64_GOT16                     # 
        R_PPC64_GOT16_LO                  # 
        R_PPC64_GOT16_HI                  # 
        R_PPC64_GOT16_HA                  # 
        R_PPC64_COPY                      # 
        R_PPC64_GLOB_DAT                  # 
        R_PPC64_JMP_SLOT                  # 
        R_PPC64_RELATIVE                  # 
        R_PPC64_UADDR32                   # 
        R_PPC64_UADDR16                   # 
        R_PPC64_REL32                     # 
        R_PPC64_PLT32                     # 
        R_PPC64_PLTREL32                  # 
        R_PPC64_PLT16_LO                  # 
        R_PPC64_PLT16_HI                  # 
        R_PPC64_PLT16_HA                  # 
        R_PPC64_SECTOFF                   # 
        R_PPC64_SECTOFF_LO                # 
        R_PPC64_SECTOFF_HI                # 
        R_PPC64_SECTOFF_HA                # 
        R_PPC64_ADDR30                    #  word30 (S + A - P) >> 2 
        R_PPC64_ADDR64                    #  doubleword64 S + A 
        R_PPC64_ADDR16_HIGHER             #  half16 #higher(S + A) 
        R_PPC64_ADDR16_HIGHERA            #  half16 #highera(S + A) 
        R_PPC64_ADDR16_HIGHEST            #  half16 #highest(S + A) 
        R_PPC64_ADDR16_HIGHESTA           #  half16 #highesta(S + A) 
        R_PPC64_UADDR64                   #  doubleword64 S + A 
        R_PPC64_REL64                     #  doubleword64 S + A - P 
        R_PPC64_PLT64                     #  doubleword64 L + A 
        R_PPC64_PLTREL64                  #  doubleword64 L + A - P 
        R_PPC64_TOC16                     #  half16* S + A - .TOC 
        R_PPC64_TOC16_LO                  #  half16 #lo(S + A - .TOC.) 
        R_PPC64_TOC16_HI                  #  half16 #hi(S + A - .TOC.) 
        R_PPC64_TOC16_HA                  #  half16 #ha(S + A - .TOC.) 
        R_PPC64_TOC                       #  doubleword64 .TOC 
        R_PPC64_PLTGOT16                  #  half16* M + A 
        R_PPC64_PLTGOT16_LO               #  half16 #lo(M + A) 
        R_PPC64_PLTGOT16_HI               #  half16 #hi(M + A) 
        R_PPC64_PLTGOT16_HA               #  half16 #ha(M + A) 
        R_PPC64_ADDR16_DS                 #  half16ds* (S + A) >> 2 
        R_PPC64_ADDR16_LO_DS              #  half16ds  #lo(S + A) >> 2 
        R_PPC64_GOT16_DS                  #  half16ds* (G + A) >> 2 
        R_PPC64_GOT16_LO_DS               #  half16ds  #lo(G + A) >> 2 
        R_PPC64_PLT16_LO_DS               #  half16ds  #lo(L + A) >> 2 
        R_PPC64_SECTOFF_DS                #  half16ds* (R + A) >> 2 
        R_PPC64_SECTOFF_LO_DS             #  half16ds  #lo(R + A) >> 2 
        R_PPC64_TOC16_DS                  #  half16ds* (S + A - .TOC.) >> 2 
        R_PPC64_TOC16_LO_DS               #  half16ds  #lo(S + A - .TOC.) >> 2 
        R_PPC64_PLTGOT16_DS               #  half16ds* (M + A) >> 2 
        R_PPC64_PLTGOT16_LO_DS            #  half16ds  #lo(M + A) >> 2 
        R_PPC64_TLS                       #  none	(sym+add)@tls 
        R_PPC64_DTPMOD64                  #  doubleword64 (sym+add)@dtpmod 
        R_PPC64_TPREL16                   #  half16*	(sym+add)@tprel 
        R_PPC64_TPREL16_LO                #  half16	(sym+add)@tprel@l 
        R_PPC64_TPREL16_HI                #  half16	(sym+add)@tprel@h 
        R_PPC64_TPREL16_HA                #  half16	(sym+add)@tprel@ha 
        R_PPC64_TPREL64                   #  doubleword64 (sym+add)@tprel 
        R_PPC64_DTPREL16                  #  half16*	(sym+add)@dtprel 
        R_PPC64_DTPREL16_LO               #  half16	(sym+add)@dtprel@l 
        R_PPC64_DTPREL16_HI               #  half16	(sym+add)@dtprel@h 
        R_PPC64_DTPREL16_HA               #  half16	(sym+add)@dtprel@ha 
        R_PPC64_DTPREL64                  #  doubleword64 (sym+add)@dtprel 
        R_PPC64_GOT_TLSGD16               #  half16*	(sym+add)@got@tlsgd 
        R_PPC64_GOT_TLSGD16_LO            #  half16	(sym+add)@got@tlsgd@l 
        R_PPC64_GOT_TLSGD16_HI            #  half16	(sym+add)@got@tlsgd@h 
        R_PPC64_GOT_TLSGD16_HA            #  half16	(sym+add)@got@tlsgd@ha 
        R_PPC64_GOT_TLSLD16               #  half16*	(sym+add)@got@tlsld 
        R_PPC64_GOT_TLSLD16_LO            #  half16	(sym+add)@got@tlsld@l 
        R_PPC64_GOT_TLSLD16_HI            #  half16	(sym+add)@got@tlsld@h 
        R_PPC64_GOT_TLSLD16_HA            #  half16	(sym+add)@got@tlsld@ha 
        R_PPC64_GOT_TPREL16_DS            #  half16ds*	(sym+add)@got@tprel 
        R_PPC64_GOT_TPREL16_LO_DS         #  half16ds (sym+add)@got@tprel@l 
        R_PPC64_GOT_TPREL16_HI            #  half16	(sym+add)@got@tprel@h 
        R_PPC64_GOT_TPREL16_HA            #  half16	(sym+add)@got@tprel@ha 
        R_PPC64_GOT_DTPREL16_DS           #  half16ds*	(sym+add)@got@dtprel 
        R_PPC64_GOT_DTPREL16_LO_DS        #  half16ds (sym+add)@got@dtprel@l 
        R_PPC64_GOT_DTPREL16_HI           #  half16	(sym+add)@got@dtprel@h 
        R_PPC64_GOT_DTPREL16_HA           #  half16	(sym+add)@got@dtprel@ha 
        R_PPC64_TPREL16_DS                #  half16ds*	(sym+add)@tprel 
        R_PPC64_TPREL16_LO_DS             #  half16ds	(sym+add)@tprel@l 
        R_PPC64_TPREL16_HIGHER            #  half16	(sym+add)@tprel@higher 
        R_PPC64_TPREL16_HIGHERA           #  half16	(sym+add)@tprel@highera 
        R_PPC64_TPREL16_HIGHEST           #  half16	(sym+add)@tprel@highest 
        R_PPC64_TPREL16_HIGHESTA          #  half16	(sym+add)@tprel@highesta 
        R_PPC64_DTPREL16_DS               #  half16ds* (sym+add)@dtprel 
        R_PPC64_DTPREL16_LO_DS            #  half16ds	(sym+add)@dtprel@l 
        R_PPC64_DTPREL16_HIGHER           #  half16	(sym+add)@dtprel@higher 
        R_PPC64_DTPREL16_HIGHERA          #  half16	(sym+add)@dtprel@highera 
        R_PPC64_DTPREL16_HIGHEST          #  half16	(sym+add)@dtprel@highest 
        R_PPC64_DTPREL16_HIGHESTA         #  half16	(sym+add)@dtprel@highesta 
        R_PPC64_JMP_IREL                  # 
        R_PPC64_IRELATIVE                 # 
        R_PPC64_REL16                     #  half16   (sym+add-.) 
        R_PPC64_REL16_LO                  #  half16   (sym+add-.)@l 
        R_PPC64_REL16_HI                  #  half16   (sym+add-.)@h 
        R_PPC64_REL16_HA                  #  half16   (sym+add-.)@ha 
        DT_PPC64_GLINK                    # 
        DT_PPC64_OPD                      # 
        DT_PPC64_OPDSZ                    # 
        DT_PPC64_NUM                      # 
        EF_ARM_RELEXEC                    # 
        EF_ARM_HASENTRY                   # 
        EF_ARM_INTERWORK                  # 
        EF_ARM_APCS_26                    # 
        EF_ARM_APCS_FLOAT                 # 
        EF_ARM_PIC                        # 
        EF_ARM_ALIGN8                     #  8-bit structure alignment is in use 
        EF_ARM_NEW_ABI                    # 
        EF_ARM_OLD_ABI                    # 
        EF_ARM_SOFT_FLOAT                 # 
        EF_ARM_VFP_FLOAT                  # 
        EF_ARM_MAVERICK_FLOAT             # 
        EF_ARM_SYMSARESORTED              # 
        EF_ARM_DYNSYMSUSESEGIDX           # 
        EF_ARM_MAPSYMSFIRST               # 
        EF_ARM_EABIMASK                   # 
        EF_ARM_BE8                        # 
        EF_ARM_LE8                        # 
        EF_ARM_EABI_UNKNOWN               # 
        EF_ARM_EABI_VER1                  # 
        EF_ARM_EABI_VER2                  # 
        EF_ARM_EABI_VER3                  # 
        EF_ARM_EABI_VER4                  # 
        EF_ARM_EABI_VER5                  # 
        STT_ARM_TFUNC                     #  A Thumb function.  
        STT_ARM_16BIT                     #  A Thumb label.  
        SHF_ARM_ENTRYSECT                 #  Section contains an entry point 
        SHF_ARM_COMDEF                    #  Section may be multiply defined
        PF_ARM_SB                         #  Segment contains the location
        PF_ARM_PI                         #  Position-independent segment.  
        PF_ARM_ABS                        #  Absolute segment.  
        PT_ARM_EXIDX                      #  ARM unwind segment.  
        SHT_ARM_EXIDX                     #  ARM unwind section.  
        SHT_ARM_PREEMPTMAP                #  Preemption details.  
        SHT_ARM_ATTRIBUTES                #  ARM attributes section.  
        R_ARM_NONE                        #  No reloc 
        R_ARM_PC24                        #  PC relative 26 bit branch 
        R_ARM_ABS32                       #  Direct 32 bit  
        R_ARM_REL32                       #  PC relative 32 bit 
        R_ARM_PC13                        # 
        R_ARM_ABS16                       #  Direct 16 bit 
        R_ARM_ABS12                       #  Direct 12 bit 
        R_ARM_THM_ABS5                    # 
        R_ARM_ABS8                        #  Direct 8 bit 
        R_ARM_SBREL32                     # 
        R_ARM_THM_PC22                    # 
        R_ARM_THM_PC8                     # 
        R_ARM_AMP_VCALL9                  # 
        R_ARM_SWI24                       #  Obsolete static relocation.  
        R_ARM_TLS_DESC                    #  Dynamic relocation.  
        R_ARM_THM_SWI8                    # 
        R_ARM_XPC25                       # 
        R_ARM_THM_XPC22                   # 
        R_ARM_TLS_DTPMOD32                #  ID of module containing symbol 
        R_ARM_TLS_DTPOFF32                #  Offset in TLS block 
        R_ARM_TLS_TPOFF32                 #  Offset in static TLS block 
        R_ARM_COPY                        #  Copy symbol at runtime 
        R_ARM_GLOB_DAT                    #  Create GOT entry 
        R_ARM_JUMP_SLOT                   #  Create PLT entry 
        R_ARM_RELATIVE                    #  Adjust by program base 
        R_ARM_GOTOFF                      #  32 bit offset to GOT 
        R_ARM_GOTPC                       #  32 bit PC relative offset to GOT 
        R_ARM_GOT32                       #  32 bit GOT entry 
        R_ARM_PLT32                       #  32 bit PLT address 
        R_ARM_ALU_PCREL_7_0               # 
        R_ARM_ALU_PCREL_15_8              # 
        R_ARM_ALU_PCREL_23_15             # 
        R_ARM_LDR_SBREL_11_0              # 
        R_ARM_ALU_SBREL_19_12             # 
        R_ARM_ALU_SBREL_27_20             # 
        R_ARM_TLS_GOTDESC                 # 
        R_ARM_TLS_CALL                    # 
        R_ARM_TLS_DESCSEQ                 # 
        R_ARM_THM_TLS_CALL                # 
        R_ARM_GNU_VTENTRY                 # 
        R_ARM_GNU_VTINHERIT               # 
        R_ARM_THM_PC11                    #  thumb unconditional branch 
        R_ARM_THM_PC9                     #  thumb conditional branch 
        R_ARM_TLS_GD32                    #  PC-rel 32 bit for global dynamic
        R_ARM_TLS_LDM32                   #  PC-rel 32 bit for local dynamic
        R_ARM_TLS_LDO32                   #  32 bit offset relative to TLS
        R_ARM_TLS_IE32                    #  PC-rel 32 bit for GOT entry of
        R_ARM_TLS_LE32                    #  32 bit offset relative to static
        R_ARM_THM_TLS_DESCSEQ             # 
        R_ARM_IRELATIVE                   # 
        R_ARM_RXPC25                      # 
        R_ARM_RSBREL32                    # 
        R_ARM_THM_RPC22                   # 
        R_ARM_RREL32                      # 
        R_ARM_RABS22                      # 
        R_ARM_RPC24                       # 
        R_ARM_RBASE                       # 
        R_ARM_NUM                         # 
        EF_IA_64_MASKOS                   #  os-specific flags 
        EF_IA_64_ABI64                    #  64-bit ABI 
        EF_IA_64_ARCH                     #  arch. version mask 
        PT_IA_64_ARCHEXT                  #  arch extension bits 
        PT_IA_64_UNWIND                   #  ia64 unwind bits 
        PT_IA_64_HP_OPT_ANOT              # 
        PT_IA_64_HP_HSL_ANOT              # 
        PT_IA_64_HP_STACK                 # 
        PF_IA_64_NORECOV                  #  spec insns w/o recovery 
        SHT_IA_64_EXT                     #  extension bits 
        SHT_IA_64_UNWIND                  #  unwind bits 
        SHF_IA_64_SHORT                   #  section near gp 
        SHF_IA_64_NORECOV                 #  spec insns w/o recovery 
        DT_IA_64_PLT_RESERVE              # 
        DT_IA_64_NUM                      # 
        R_IA64_NONE                       #  none 
        R_IA64_IMM14                      #  symbol + addend, add imm14 
        R_IA64_IMM22                      #  symbol + addend, add imm22 
        R_IA64_IMM64                      #  symbol + addend, mov imm64 
        R_IA64_DIR32MSB                   #  symbol + addend, data4 MSB 
        R_IA64_DIR32LSB                   #  symbol + addend, data4 LSB 
        R_IA64_DIR64MSB                   #  symbol + addend, data8 MSB 
        R_IA64_DIR64LSB                   #  symbol + addend, data8 LSB 
        R_IA64_GPREL22                    #  @gprel(sym + add), add imm22 
        R_IA64_GPREL64I                   #  @gprel(sym + add), mov imm64 
        R_IA64_GPREL32MSB                 #  @gprel(sym + add), data4 MSB 
        R_IA64_GPREL32LSB                 #  @gprel(sym + add), data4 LSB 
        R_IA64_GPREL64MSB                 #  @gprel(sym + add), data8 MSB 
        R_IA64_GPREL64LSB                 #  @gprel(sym + add), data8 LSB 
        R_IA64_LTOFF22                    #  @ltoff(sym + add), add imm22 
        R_IA64_LTOFF64I                   #  @ltoff(sym + add), mov imm64 
        R_IA64_PLTOFF22                   #  @pltoff(sym + add), add imm22 
        R_IA64_PLTOFF64I                  #  @pltoff(sym + add), mov imm64 
        R_IA64_PLTOFF64MSB                #  @pltoff(sym + add), data8 MSB 
        R_IA64_PLTOFF64LSB                #  @pltoff(sym + add), data8 LSB 
        R_IA64_FPTR64I                    #  @fptr(sym + add), mov imm64 
        R_IA64_FPTR32MSB                  #  @fptr(sym + add), data4 MSB 
        R_IA64_FPTR32LSB                  #  @fptr(sym + add), data4 LSB 
        R_IA64_FPTR64MSB                  #  @fptr(sym + add), data8 MSB 
        R_IA64_FPTR64LSB                  #  @fptr(sym + add), data8 LSB 
        R_IA64_PCREL60B                   #  @pcrel(sym + add), brl 
        R_IA64_PCREL21B                   #  @pcrel(sym + add), ptb, call 
        R_IA64_PCREL21M                   #  @pcrel(sym + add), chk.s 
        R_IA64_PCREL21F                   #  @pcrel(sym + add), fchkf 
        R_IA64_PCREL32MSB                 #  @pcrel(sym + add), data4 MSB 
        R_IA64_PCREL32LSB                 #  @pcrel(sym + add), data4 LSB 
        R_IA64_PCREL64MSB                 #  @pcrel(sym + add), data8 MSB 
        R_IA64_PCREL64LSB                 #  @pcrel(sym + add), data8 LSB 
        R_IA64_LTOFF_FPTR22               #  @ltoff(@fptr(s+a)), imm22 
        R_IA64_LTOFF_FPTR64I              #  @ltoff(@fptr(s+a)), imm64 
        R_IA64_LTOFF_FPTR32MSB            #  @ltoff(@fptr(s+a)), data4 MSB 
        R_IA64_LTOFF_FPTR32LSB            #  @ltoff(@fptr(s+a)), data4 LSB 
        R_IA64_LTOFF_FPTR64MSB            #  @ltoff(@fptr(s+a)), data8 MSB 
        R_IA64_LTOFF_FPTR64LSB            #  @ltoff(@fptr(s+a)), data8 LSB 
        R_IA64_SEGREL32MSB                #  @segrel(sym + add), data4 MSB 
        R_IA64_SEGREL32LSB                #  @segrel(sym + add), data4 LSB 
        R_IA64_SEGREL64MSB                #  @segrel(sym + add), data8 MSB 
        R_IA64_SEGREL64LSB                #  @segrel(sym + add), data8 LSB 
        R_IA64_SECREL32MSB                #  @secrel(sym + add), data4 MSB 
        R_IA64_SECREL32LSB                #  @secrel(sym + add), data4 LSB 
        R_IA64_SECREL64MSB                #  @secrel(sym + add), data8 MSB 
        R_IA64_SECREL64LSB                #  @secrel(sym + add), data8 LSB 
        R_IA64_REL32MSB                   #  data 4 + REL 
        R_IA64_REL32LSB                   #  data 4 + REL 
        R_IA64_REL64MSB                   #  data 8 + REL 
        R_IA64_REL64LSB                   #  data 8 + REL 
        R_IA64_LTV32MSB                   #  symbol + addend, data4 MSB 
        R_IA64_LTV32LSB                   #  symbol + addend, data4 LSB 
        R_IA64_LTV64MSB                   #  symbol + addend, data8 MSB 
        R_IA64_LTV64LSB                   #  symbol + addend, data8 LSB 
        R_IA64_PCREL21BI                  #  @pcrel(sym + add), 21bit inst 
        R_IA64_PCREL22                    #  @pcrel(sym + add), 22bit inst 
        R_IA64_PCREL64I                   #  @pcrel(sym + add), 64bit inst 
        R_IA64_IPLTMSB                    #  dynamic reloc, imported PLT, MSB 
        R_IA64_IPLTLSB                    #  dynamic reloc, imported PLT, LSB 
        R_IA64_COPY                       #  copy relocation 
        R_IA64_SUB                        #  Addend and symbol difference 
        R_IA64_LTOFF22X                   #  LTOFF22, relaxable.  
        R_IA64_LDXMOV                     #  Use of LTOFF22X.  
        R_IA64_TPREL14                    #  @tprel(sym + add), imm14 
        R_IA64_TPREL22                    #  @tprel(sym + add), imm22 
        R_IA64_TPREL64I                   #  @tprel(sym + add), imm64 
        R_IA64_TPREL64MSB                 #  @tprel(sym + add), data8 MSB 
        R_IA64_TPREL64LSB                 #  @tprel(sym + add), data8 LSB 
        R_IA64_LTOFF_TPREL22              #  @ltoff(@tprel(s+a)), imm2 
        R_IA64_DTPMOD64MSB                #  @dtpmod(sym + add), data8 MSB 
        R_IA64_DTPMOD64LSB                #  @dtpmod(sym + add), data8 LSB 
        R_IA64_LTOFF_DTPMOD22             #  @ltoff(@dtpmod(sym + add)), imm22 
        R_IA64_DTPREL14                   #  @dtprel(sym + add), imm14 
        R_IA64_DTPREL22                   #  @dtprel(sym + add), imm22 
        R_IA64_DTPREL64I                  #  @dtprel(sym + add), imm64 
        R_IA64_DTPREL32MSB                #  @dtprel(sym + add), data4 MSB 
        R_IA64_DTPREL32LSB                #  @dtprel(sym + add), data4 LSB 
        R_IA64_DTPREL64MSB                #  @dtprel(sym + add), data8 MSB 
        R_IA64_DTPREL64LSB                #  @dtprel(sym + add), data8 LSB 
        R_IA64_LTOFF_DTPREL22             #  @ltoff(@dtprel(s+a)), imm22 
        EF_SH_MACH_MASK                   # 
        EF_SH_UNKNOWN                     # 
        EF_SH1                            # 
        EF_SH2                            # 
        EF_SH3                            # 
        EF_SH_DSP                         # 
        EF_SH3_DSP                        # 
        EF_SH4AL_DSP                      # 
        EF_SH3E                           # 
        EF_SH4                            # 
        EF_SH2E                           # 
        EF_SH4A                           # 
        EF_SH2A                           # 
        EF_SH4_NOFPU                      # 
        EF_SH4A_NOFPU                     # 
        EF_SH4_NOMMU_NOFPU                # 
        EF_SH2A_NOFPU                     # 
        EF_SH3_NOMMU                      # 
        EF_SH2A_SH4_NOFPU                 # 
        EF_SH2A_SH3_NOFPU                 # 
        EF_SH2A_SH4                       # 
        EF_SH2A_SH3E                      # 
        R_SH_NONE                         # 
        R_SH_DIR32                        # 
        R_SH_REL32                        # 
        R_SH_DIR8WPN                      # 
        R_SH_IND12W                       # 
        R_SH_DIR8WPL                      # 
        R_SH_DIR8WPZ                      # 
        R_SH_DIR8BP                       # 
        R_SH_DIR8W                        # 
        R_SH_DIR8L                        # 
        R_SH_SWITCH16                     # 
        R_SH_SWITCH32                     # 
        R_SH_USES                         # 
        R_SH_COUNT                        # 
        R_SH_ALIGN                        # 
        R_SH_CODE                         # 
        R_SH_DATA                         # 
        R_SH_LABEL                        # 
        R_SH_SWITCH8                      # 
        R_SH_GNU_VTINHERIT                # 
        R_SH_GNU_VTENTRY                  # 
        R_SH_TLS_GD_32                    # 
        R_SH_TLS_LD_32                    # 
        R_SH_TLS_LDO_32                   # 
        R_SH_TLS_IE_32                    # 
        R_SH_TLS_LE_32                    # 
        R_SH_TLS_DTPMOD32                 # 
        R_SH_TLS_DTPOFF32                 # 
        R_SH_TLS_TPOFF32                  # 
        R_SH_GOT32                        # 
        R_SH_PLT32                        # 
        R_SH_COPY                         # 
        R_SH_GLOB_DAT                     # 
        R_SH_JMP_SLOT                     # 
        R_SH_RELATIVE                     # 
        R_SH_GOTOFF                       # 
        R_SH_GOTPC                        # 
        R_SH_NUM                          # 
        EF_S390_HIGH_GPRS                 #  High GPRs kernel facility needed.  
        R_390_NONE                        #  No reloc.  
        R_390_8                           #  Direct 8 bit.  
        R_390_12                          #  Direct 12 bit.  
        R_390_16                          #  Direct 16 bit.  
        R_390_32                          #  Direct 32 bit.  
        R_390_PC32                        #  PC relative 32 bit.	
        R_390_GOT12                       #  12 bit GOT offset.  
        R_390_GOT32                       #  32 bit GOT offset.  
        R_390_PLT32                       #  32 bit PC relative PLT address.  
        R_390_COPY                        #  Copy symbol at runtime.  
        R_390_GLOB_DAT                    #  Create GOT entry.  
        R_390_JMP_SLOT                    #  Create PLT entry.  
        R_390_RELATIVE                    #  Adjust by program base.  
        R_390_GOTOFF32                    #  32 bit offset to GOT.	 
        R_390_GOTPC                       #  32 bit PC relative offset to GOT.  
        R_390_GOT16                       #  16 bit GOT offset.  
        R_390_PC16                        #  PC relative 16 bit.	
        R_390_PC16DBL                     #  PC relative 16 bit shifted by 1.  
        R_390_PLT16DBL                    #  16 bit PC rel. PLT shifted by 1.  
        R_390_PC32DBL                     #  PC relative 32 bit shifted by 1.  
        R_390_PLT32DBL                    #  32 bit PC rel. PLT shifted by 1.  
        R_390_GOTPCDBL                    #  32 bit PC rel. GOT shifted by 1.  
        R_390_64                          #  Direct 64 bit.  
        R_390_PC64                        #  PC relative 64 bit.	
        R_390_GOT64                       #  64 bit GOT offset.  
        R_390_PLT64                       #  64 bit PC relative PLT address.  
        R_390_GOTENT                      #  32 bit PC rel. to GOT entry >> 1. 
        R_390_GOTOFF16                    #  16 bit offset to GOT. 
        R_390_GOTOFF64                    #  64 bit offset to GOT. 
        R_390_GOTPLT12                    #  12 bit offset to jump slot.	
        R_390_GOTPLT16                    #  16 bit offset to jump slot.	
        R_390_GOTPLT32                    #  32 bit offset to jump slot.	
        R_390_GOTPLT64                    #  64 bit offset to jump slot.	
        R_390_GOTPLTENT                   #  32 bit rel. offset to jump slot.  
        R_390_PLTOFF16                    #  16 bit offset from GOT to PLT. 
        R_390_PLTOFF32                    #  32 bit offset from GOT to PLT. 
        R_390_PLTOFF64                    #  16 bit offset from GOT to PLT. 
        R_390_TLS_LOAD                    #  Tag for load insn in TLS code.  
        R_390_TLS_GDCALL                  #  Tag for function call in general
        R_390_TLS_LDCALL                  #  Tag for function call in local
        R_390_TLS_GD32                    #  Direct 32 bit for general dynamic
        R_390_TLS_GD64                    #  Direct 64 bit for general dynamic
        R_390_TLS_GOTIE12                 #  12 bit GOT offset for static TLS
        R_390_TLS_GOTIE32                 #  32 bit GOT offset for static TLS
        R_390_TLS_GOTIE64                 #  64 bit GOT offset for static TLS
        R_390_TLS_LDM32                   #  Direct 32 bit for local dynamic
        R_390_TLS_LDM64                   #  Direct 64 bit for local dynamic
        R_390_TLS_IE32                    #  32 bit address of GOT entry for
        R_390_TLS_IE64                    #  64 bit address of GOT entry for
        R_390_TLS_IEENT                   #  32 bit rel. offset to GOT entry for
        R_390_TLS_LE32                    #  32 bit negated offset relative to
        R_390_TLS_LE64                    #  64 bit negated offset relative to
        R_390_TLS_LDO32                   #  32 bit offset relative to TLS
        R_390_TLS_LDO64                   #  64 bit offset relative to TLS
        R_390_TLS_DTPMOD                  #  ID of module containing symbol.  
        R_390_TLS_DTPOFF                  #  Offset in TLS block.	 
        R_390_TLS_TPOFF                   #  Negated offset in static TLS
        R_390_20                          #  Direct 20 bit.  
        R_390_GOT20                       #  20 bit GOT offset.  
        R_390_GOTPLT20                    #  20 bit offset to jump slot.  
        R_390_TLS_GOTIE20                 #  20 bit GOT offset for static TLS
        R_390_NUM                         # 
        R_CRIS_NONE                       # 
        R_CRIS_8                          # 
        R_CRIS_16                         # 
        R_CRIS_32                         # 
        R_CRIS_8_PCREL                    # 
        R_CRIS_16_PCREL                   # 
        R_CRIS_32_PCREL                   # 
        R_CRIS_GNU_VTINHERIT              # 
        R_CRIS_GNU_VTENTRY                # 
        R_CRIS_COPY                       # 
        R_CRIS_GLOB_DAT                   # 
        R_CRIS_JUMP_SLOT                  # 
        R_CRIS_RELATIVE                   # 
        R_CRIS_16_GOT                     # 
        R_CRIS_32_GOT                     # 
        R_CRIS_16_GOTPLT                  # 
        R_CRIS_32_GOTPLT                  # 
        R_CRIS_32_GOTREL                  # 
        R_CRIS_32_PLT_GOTREL              # 
        R_CRIS_32_PLT_PCREL               # 
        R_CRIS_NUM                        # 
        R_X86_64_NONE                     #  No reloc 
        R_X86_64_64                       #  Direct 64 bit  
        R_X86_64_PC32                     #  PC relative 32 bit signed 
        R_X86_64_GOT32                    #  32 bit GOT entry 
        R_X86_64_PLT32                    #  32 bit PLT address 
        R_X86_64_COPY                     #  Copy symbol at runtime 
        R_X86_64_GLOB_DAT                 #  Create GOT entry 
        R_X86_64_JUMP_SLOT                #  Create PLT entry 
        R_X86_64_RELATIVE                 #  Adjust by program base 
        R_X86_64_GOTPCREL                 #  32 bit signed PC relative
        R_X86_64_32                       #  Direct 32 bit zero extended 
        R_X86_64_32S                      #  Direct 32 bit sign extended 
        R_X86_64_16                       #  Direct 16 bit zero extended 
        R_X86_64_PC16                     #  16 bit sign extended pc relative 
        R_X86_64_8                        #  Direct 8 bit sign extended  
        R_X86_64_PC8                      #  8 bit sign extended pc relative 
        R_X86_64_DTPMOD64                 #  ID of module containing symbol 
        R_X86_64_DTPOFF64                 #  Offset in module's TLS block 
        R_X86_64_TPOFF64                  #  Offset in initial TLS block 
        R_X86_64_TLSGD                    #  32 bit signed PC relative offset
        R_X86_64_TLSLD                    #  32 bit signed PC relative offset
        R_X86_64_DTPOFF32                 #  Offset in TLS block 
        R_X86_64_GOTTPOFF                 #  32 bit signed PC relative offset
        R_X86_64_TPOFF32                  #  Offset in initial TLS block 
        R_X86_64_PC64                     #  PC relative 64 bit 
        R_X86_64_GOTOFF64                 #  64 bit offset to GOT 
        R_X86_64_GOTPC32                  #  32 bit signed pc relative
        R_X86_64_GOT64                    #  64-bit GOT entry offset 
        R_X86_64_GOTPCREL64               #  64-bit PC relative offset
        R_X86_64_GOTPC64                  #  64-bit PC relative offset to GOT 
        R_X86_64_GOTPLT64                 #  like GOT64, says PLT entry needed 
        R_X86_64_PLTOFF64                 #  64-bit GOT relative offset
        R_X86_64_SIZE32                   #  Size of symbol plus 32-bit addend 
        R_X86_64_SIZE64                   #  Size of symbol plus 64-bit addend 
        R_X86_64_GOTPC32_TLSDESC          #  GOT offset for TLS descriptor.  
        R_X86_64_TLSDESC_CALL             #  Marker for call through TLS
        R_X86_64_TLSDESC                  #  TLS descriptor.  
        R_X86_64_IRELATIVE                #  Adjust indirectly by program base 
        R_X86_64_RELATIVE64               #  64-bit adjust by program base 
        R_X86_64_NUM                      # 
        R_MN10300_NONE                    #  No reloc.  
        R_MN10300_32                      #  Direct 32 bit.  
        R_MN10300_16                      #  Direct 16 bit.  
        R_MN10300_8                       #  Direct 8 bit.  
        R_MN10300_PCREL32                 #  PC-relative 32-bit.  
        R_MN10300_PCREL16                 #  PC-relative 16-bit signed.  
        R_MN10300_PCREL8                  #  PC-relative 8-bit signed.  
        R_MN10300_GNU_VTINHERIT           #  Ancient C++ vtable garbage... 
        R_MN10300_GNU_VTENTRY             #  ... collection annotation.  
        R_MN10300_24                      #  Direct 24 bit.  
        R_MN10300_GOTPC32                 #  32-bit PCrel offset to GOT.  
        R_MN10300_GOTPC16                 #  16-bit PCrel offset to GOT.  
        R_MN10300_GOTOFF32                #  32-bit offset from GOT.  
        R_MN10300_GOTOFF24                #  24-bit offset from GOT.  
        R_MN10300_GOTOFF16                #  16-bit offset from GOT.  
        R_MN10300_PLT32                   #  32-bit PCrel to PLT entry.  
        R_MN10300_PLT16                   #  16-bit PCrel to PLT entry.  
        R_MN10300_GOT32                   #  32-bit offset to GOT entry.  
        R_MN10300_GOT24                   #  24-bit offset to GOT entry.  
        R_MN10300_GOT16                   #  16-bit offset to GOT entry.  
        R_MN10300_COPY                    #  Copy symbol at runtime.  
        R_MN10300_GLOB_DAT                #  Create GOT entry.  
        R_MN10300_JMP_SLOT                #  Create PLT entry.  
        R_MN10300_RELATIVE                #  Adjust by program base.  
        R_MN10300_NUM                     # 
        R_M32R_NONE                       #  No reloc. 
        R_M32R_16                         #  Direct 16 bit. 
        R_M32R_32                         #  Direct 32 bit. 
        R_M32R_24                         #  Direct 24 bit. 
        R_M32R_10_PCREL                   #  PC relative 10 bit shifted. 
        R_M32R_18_PCREL                   #  PC relative 18 bit shifted. 
        R_M32R_26_PCREL                   #  PC relative 26 bit shifted. 
        R_M32R_HI16_ULO                   #  High 16 bit with unsigned low. 
        R_M32R_HI16_SLO                   #  High 16 bit with signed low. 
        R_M32R_LO16                       #  Low 16 bit. 
        R_M32R_SDA16                      #  16 bit offset in SDA. 
        R_M32R_GNU_VTINHERIT              # 
        R_M32R_GNU_VTENTRY                # 
        R_M32R_16_RELA                    #  Direct 16 bit. 
        R_M32R_32_RELA                    #  Direct 32 bit. 
        R_M32R_24_RELA                    #  Direct 24 bit. 
        R_M32R_10_PCREL_RELA              #  PC relative 10 bit shifted. 
        R_M32R_18_PCREL_RELA              #  PC relative 18 bit shifted. 
        R_M32R_26_PCREL_RELA              #  PC relative 26 bit shifted. 
        R_M32R_HI16_ULO_RELA              #  High 16 bit with unsigned low 
        R_M32R_HI16_SLO_RELA              #  High 16 bit with signed low 
        R_M32R_LO16_RELA                  #  Low 16 bit 
        R_M32R_SDA16_RELA                 #  16 bit offset in SDA 
        R_M32R_RELA_GNU_VTINHERIT         # 
        R_M32R_RELA_GNU_VTENTRY           # 
        R_M32R_REL32                      #  PC relative 32 bit.  
        R_M32R_GOT24                      #  24 bit GOT entry 
        R_M32R_26_PLTREL                  #  26 bit PC relative to PLT shifted 
        R_M32R_COPY                       #  Copy symbol at runtime 
        R_M32R_GLOB_DAT                   #  Create GOT entry 
        R_M32R_JMP_SLOT                   #  Create PLT entry 
        R_M32R_RELATIVE                   #  Adjust by program base 
        R_M32R_GOTOFF                     #  24 bit offset to GOT 
        R_M32R_GOTPC24                    #  24 bit PC relative offset to GOT 
        R_M32R_GOT16_HI_ULO               #  High 16 bit GOT entry with unsigned
        R_M32R_GOT16_HI_SLO               #  High 16 bit GOT entry with signed
        R_M32R_GOT16_LO                   #  Low 16 bit GOT entry 
        R_M32R_GOTPC_HI_ULO               #  High 16 bit PC relative offset to
        R_M32R_GOTPC_HI_SLO               #  High 16 bit PC relative offset to
        R_M32R_GOTPC_LO                   #  Low 16 bit PC relative offset to
        R_M32R_GOTOFF_HI_ULO              #  High 16 bit offset to GOT
        R_M32R_GOTOFF_HI_SLO              #  High 16 bit offset to GOT
        R_M32R_GOTOFF_LO                  #  Low 16 bit offset to GOT 
        R_M32R_NUM                        #  Keep this the last entry. 
        R_TILEPRO_NONE                    #  No reloc 
        R_TILEPRO_32                      #  Direct 32 bit 
        R_TILEPRO_16                      #  Direct 16 bit 
        R_TILEPRO_8                       #  Direct 8 bit 
        R_TILEPRO_32_PCREL                #  PC relative 32 bit 
        R_TILEPRO_16_PCREL                #  PC relative 16 bit 
        R_TILEPRO_8_PCREL                 #  PC relative 8 bit 
        R_TILEPRO_LO16                    #  Low 16 bit 
        R_TILEPRO_HI16                    #  High 16 bit 
        R_TILEPRO_HA16                    #  High 16 bit, adjusted 
        R_TILEPRO_COPY                    #  Copy relocation 
        R_TILEPRO_GLOB_DAT                #  Create GOT entry 
        R_TILEPRO_JMP_SLOT                #  Create PLT entry 
        R_TILEPRO_RELATIVE                #  Adjust by program base 
        R_TILEPRO_BROFF_X1                #  X1 pipe branch offset 
        R_TILEPRO_JOFFLONG_X1             #  X1 pipe jump offset 
        R_TILEPRO_JOFFLONG_X1_PLT         #  X1 pipe jump offset to PLT 
        R_TILEPRO_IMM8_X0                 #  X0 pipe 8-bit 
        R_TILEPRO_IMM8_Y0                 #  Y0 pipe 8-bit 
        R_TILEPRO_IMM8_X1                 #  X1 pipe 8-bit 
        R_TILEPRO_IMM8_Y1                 #  Y1 pipe 8-bit 
        R_TILEPRO_MT_IMM15_X1             #  X1 pipe mtspr 
        R_TILEPRO_MF_IMM15_X1             #  X1 pipe mfspr 
        R_TILEPRO_IMM16_X0                #  X0 pipe 16-bit 
        R_TILEPRO_IMM16_X1                #  X1 pipe 16-bit 
        R_TILEPRO_IMM16_X0_LO             #  X0 pipe low 16-bit 
        R_TILEPRO_IMM16_X1_LO             #  X1 pipe low 16-bit 
        R_TILEPRO_IMM16_X0_HI             #  X0 pipe high 16-bit 
        R_TILEPRO_IMM16_X1_HI             #  X1 pipe high 16-bit 
        R_TILEPRO_IMM16_X0_HA             #  X0 pipe high 16-bit, adjusted 
        R_TILEPRO_IMM16_X1_HA             #  X1 pipe high 16-bit, adjusted 
        R_TILEPRO_IMM16_X0_PCREL          #  X0 pipe PC relative 16 bit 
        R_TILEPRO_IMM16_X1_PCREL          #  X1 pipe PC relative 16 bit 
        R_TILEPRO_IMM16_X0_LO_PCREL       #  X0 pipe PC relative low 16 bit 
        R_TILEPRO_IMM16_X1_LO_PCREL       #  X1 pipe PC relative low 16 bit 
        R_TILEPRO_IMM16_X0_HI_PCREL       #  X0 pipe PC relative high 16 bit 
        R_TILEPRO_IMM16_X1_HI_PCREL       #  X1 pipe PC relative high 16 bit 
        R_TILEPRO_IMM16_X0_HA_PCREL       #  X0 pipe PC relative ha() 16 bit 
        R_TILEPRO_IMM16_X1_HA_PCREL       #  X1 pipe PC relative ha() 16 bit 
        R_TILEPRO_IMM16_X0_GOT            #  X0 pipe 16-bit GOT offset 
        R_TILEPRO_IMM16_X1_GOT            #  X1 pipe 16-bit GOT offset 
        R_TILEPRO_IMM16_X0_GOT_LO         #  X0 pipe low 16-bit GOT offset 
        R_TILEPRO_IMM16_X1_GOT_LO         #  X1 pipe low 16-bit GOT offset 
        R_TILEPRO_IMM16_X0_GOT_HI         #  X0 pipe high 16-bit GOT offset 
        R_TILEPRO_IMM16_X1_GOT_HI         #  X1 pipe high 16-bit GOT offset 
        R_TILEPRO_IMM16_X0_GOT_HA         #  X0 pipe ha() 16-bit GOT offset 
        R_TILEPRO_IMM16_X1_GOT_HA         #  X1 pipe ha() 16-bit GOT offset 
        R_TILEPRO_MMSTART_X0              #  X0 pipe mm "start" 
        R_TILEPRO_MMEND_X0                #  X0 pipe mm "end" 
        R_TILEPRO_MMSTART_X1              #  X1 pipe mm "start" 
        R_TILEPRO_MMEND_X1                #  X1 pipe mm "end" 
        R_TILEPRO_SHAMT_X0                #  X0 pipe shift amount 
        R_TILEPRO_SHAMT_X1                #  X1 pipe shift amount 
        R_TILEPRO_SHAMT_Y0                #  Y0 pipe shift amount 
        R_TILEPRO_SHAMT_Y1                #  Y1 pipe shift amount 
        R_TILEPRO_DEST_IMM8_X1            #  X1 pipe destination 8-bit 
        R_TILEPRO_TLS_GD_CALL             #  "jal" for TLS GD 
        R_TILEPRO_IMM8_X0_TLS_GD_ADD      #  X0 pipe "addi" for TLS GD 
        R_TILEPRO_IMM8_X1_TLS_GD_ADD      #  X1 pipe "addi" for TLS GD 
        R_TILEPRO_IMM8_Y0_TLS_GD_ADD      #  Y0 pipe "addi" for TLS GD 
        R_TILEPRO_IMM8_Y1_TLS_GD_ADD      #  Y1 pipe "addi" for TLS GD 
        R_TILEPRO_TLS_IE_LOAD             #  "lw_tls" for TLS IE 
        R_TILEPRO_IMM16_X0_TLS_GD         #  X0 pipe 16-bit TLS GD offset 
        R_TILEPRO_IMM16_X1_TLS_GD         #  X1 pipe 16-bit TLS GD offset 
        R_TILEPRO_IMM16_X0_TLS_GD_LO      #  X0 pipe low 16-bit TLS GD offset 
        R_TILEPRO_IMM16_X1_TLS_GD_LO      #  X1 pipe low 16-bit TLS GD offset 
        R_TILEPRO_IMM16_X0_TLS_GD_HI      #  X0 pipe high 16-bit TLS GD offset 
        R_TILEPRO_IMM16_X1_TLS_GD_HI      #  X1 pipe high 16-bit TLS GD offset 
        R_TILEPRO_IMM16_X0_TLS_GD_HA      #  X0 pipe ha() 16-bit TLS GD offset 
        R_TILEPRO_IMM16_X1_TLS_GD_HA      #  X1 pipe ha() 16-bit TLS GD offset 
        R_TILEPRO_IMM16_X0_TLS_IE         #  X0 pipe 16-bit TLS IE offset 
        R_TILEPRO_IMM16_X1_TLS_IE         #  X1 pipe 16-bit TLS IE offset 
        R_TILEPRO_IMM16_X0_TLS_IE_LO      #  X0 pipe low 16-bit TLS IE offset 
        R_TILEPRO_IMM16_X1_TLS_IE_LO      #  X1 pipe low 16-bit TLS IE offset 
        R_TILEPRO_IMM16_X0_TLS_IE_HI      #  X0 pipe high 16-bit TLS IE offset 
        R_TILEPRO_IMM16_X1_TLS_IE_HI      #  X1 pipe high 16-bit TLS IE offset 
        R_TILEPRO_IMM16_X0_TLS_IE_HA      #  X0 pipe ha() 16-bit TLS IE offset 
        R_TILEPRO_IMM16_X1_TLS_IE_HA      #  X1 pipe ha() 16-bit TLS IE offset 
        R_TILEPRO_TLS_DTPMOD32            #  ID of module containing symbol 
        R_TILEPRO_TLS_DTPOFF32            #  Offset in TLS block 
        R_TILEPRO_TLS_TPOFF32             #  Offset in static TLS block 
        R_TILEPRO_IMM16_X0_TLS_LE         #  X0 pipe 16-bit TLS LE offset 
        R_TILEPRO_IMM16_X1_TLS_LE         #  X1 pipe 16-bit TLS LE offset 
        R_TILEPRO_IMM16_X0_TLS_LE_LO      #  X0 pipe low 16-bit TLS LE offset 
        R_TILEPRO_IMM16_X1_TLS_LE_LO      #  X1 pipe low 16-bit TLS LE offset 
        R_TILEPRO_IMM16_X0_TLS_LE_HI      #  X0 pipe high 16-bit TLS LE offset 
        R_TILEPRO_IMM16_X1_TLS_LE_HI      #  X1 pipe high 16-bit TLS LE offset 
        R_TILEPRO_IMM16_X0_TLS_LE_HA      #  X0 pipe ha() 16-bit TLS LE offset 
        R_TILEPRO_IMM16_X1_TLS_LE_HA      #  X1 pipe ha() 16-bit TLS LE offset 
        R_TILEPRO_GNU_VTINHERIT           #  GNU C++ vtable hierarchy 
        R_TILEPRO_GNU_VTENTRY             #  GNU C++ vtable member usage 
        R_TILEPRO_NUM                     # 
        R_TILEGX_NONE                     #  No reloc 
        R_TILEGX_64                       #  Direct 64 bit 
        R_TILEGX_32                       #  Direct 32 bit 
        R_TILEGX_16                       #  Direct 16 bit 
        R_TILEGX_8                        #  Direct 8 bit 
        R_TILEGX_64_PCREL                 #  PC relative 64 bit 
        R_TILEGX_32_PCREL                 #  PC relative 32 bit 
        R_TILEGX_16_PCREL                 #  PC relative 16 bit 
        R_TILEGX_8_PCREL                  #  PC relative 8 bit 
        R_TILEGX_HW0                      #  hword 0 16-bit 
        R_TILEGX_HW1                      #  hword 1 16-bit 
        R_TILEGX_HW2                      #  hword 2 16-bit 
        R_TILEGX_HW3                      #  hword 3 16-bit 
        R_TILEGX_HW0_LAST                 #  last hword 0 16-bit 
        R_TILEGX_HW1_LAST                 #  last hword 1 16-bit 
        R_TILEGX_HW2_LAST                 #  last hword 2 16-bit 
        R_TILEGX_COPY                     #  Copy relocation 
        R_TILEGX_GLOB_DAT                 #  Create GOT entry 
        R_TILEGX_JMP_SLOT                 #  Create PLT entry 
        R_TILEGX_RELATIVE                 #  Adjust by program base 
        R_TILEGX_BROFF_X1                 #  X1 pipe branch offset 
        R_TILEGX_JUMPOFF_X1               #  X1 pipe jump offset 
        R_TILEGX_JUMPOFF_X1_PLT           #  X1 pipe jump offset to PLT 
        R_TILEGX_IMM8_X0                  #  X0 pipe 8-bit 
        R_TILEGX_IMM8_Y0                  #  Y0 pipe 8-bit 
        R_TILEGX_IMM8_X1                  #  X1 pipe 8-bit 
        R_TILEGX_IMM8_Y1                  #  Y1 pipe 8-bit 
        R_TILEGX_DEST_IMM8_X1             #  X1 pipe destination 8-bit 
        R_TILEGX_MT_IMM14_X1              #  X1 pipe mtspr 
        R_TILEGX_MF_IMM14_X1              #  X1 pipe mfspr 
        R_TILEGX_MMSTART_X0               #  X0 pipe mm "start" 
        R_TILEGX_MMEND_X0                 #  X0 pipe mm "end" 
        R_TILEGX_SHAMT_X0                 #  X0 pipe shift amount 
        R_TILEGX_SHAMT_X1                 #  X1 pipe shift amount 
        R_TILEGX_SHAMT_Y0                 #  Y0 pipe shift amount 
        R_TILEGX_SHAMT_Y1                 #  Y1 pipe shift amount 
        R_TILEGX_IMM16_X0_HW0             #  X0 pipe hword 0 
        R_TILEGX_IMM16_X1_HW0             #  X1 pipe hword 0 
        R_TILEGX_IMM16_X0_HW1             #  X0 pipe hword 1 
        R_TILEGX_IMM16_X1_HW1             #  X1 pipe hword 1 
        R_TILEGX_IMM16_X0_HW2             #  X0 pipe hword 2 
        R_TILEGX_IMM16_X1_HW2             #  X1 pipe hword 2 
        R_TILEGX_IMM16_X0_HW3             #  X0 pipe hword 3 
        R_TILEGX_IMM16_X1_HW3             #  X1 pipe hword 3 
        R_TILEGX_IMM16_X0_HW0_LAST        #  X0 pipe last hword 0 
        R_TILEGX_IMM16_X1_HW0_LAST        #  X1 pipe last hword 0 
        R_TILEGX_IMM16_X0_HW1_LAST        #  X0 pipe last hword 1 
        R_TILEGX_IMM16_X1_HW1_LAST        #  X1 pipe last hword 1 
        R_TILEGX_IMM16_X0_HW2_LAST        #  X0 pipe last hword 2 
        R_TILEGX_IMM16_X1_HW2_LAST        #  X1 pipe last hword 2 
        R_TILEGX_IMM16_X0_HW0_PCREL       #  X0 pipe PC relative hword 0 
        R_TILEGX_IMM16_X1_HW0_PCREL       #  X1 pipe PC relative hword 0 
        R_TILEGX_IMM16_X0_HW1_PCREL       #  X0 pipe PC relative hword 1 
        R_TILEGX_IMM16_X1_HW1_PCREL       #  X1 pipe PC relative hword 1 
        R_TILEGX_IMM16_X0_HW2_PCREL       #  X0 pipe PC relative hword 2 
        R_TILEGX_IMM16_X1_HW2_PCREL       #  X1 pipe PC relative hword 2 
        R_TILEGX_IMM16_X0_HW3_PCREL       #  X0 pipe PC relative hword 3 
        R_TILEGX_IMM16_X1_HW3_PCREL       #  X1 pipe PC relative hword 3 
        R_TILEGX_IMM16_X0_HW0_LAST_PCREL  #  X0 pipe PC-rel last hword 0 
        R_TILEGX_IMM16_X1_HW0_LAST_PCREL  #  X1 pipe PC-rel last hword 0 
        R_TILEGX_IMM16_X0_HW1_LAST_PCREL  #  X0 pipe PC-rel last hword 1 
        R_TILEGX_IMM16_X1_HW1_LAST_PCREL  #  X1 pipe PC-rel last hword 1 
        R_TILEGX_IMM16_X0_HW2_LAST_PCREL  #  X0 pipe PC-rel last hword 2 
        R_TILEGX_IMM16_X1_HW2_LAST_PCREL  #  X1 pipe PC-rel last hword 2 
        R_TILEGX_IMM16_X0_HW0_GOT         #  X0 pipe hword 0 GOT offset 
        R_TILEGX_IMM16_X1_HW0_GOT         #  X1 pipe hword 0 GOT offset 
        R_TILEGX_IMM16_X0_HW0_LAST_GOT    #  X0 pipe last hword 0 GOT offset 
        R_TILEGX_IMM16_X1_HW0_LAST_GOT    #  X1 pipe last hword 0 GOT offset 
        R_TILEGX_IMM16_X0_HW1_LAST_GOT    #  X0 pipe last hword 1 GOT offset 
        R_TILEGX_IMM16_X1_HW1_LAST_GOT    #  X1 pipe last hword 1 GOT offset 
        R_TILEGX_IMM16_X0_HW0_TLS_GD      #  X0 pipe hword 0 TLS GD offset 
        R_TILEGX_IMM16_X1_HW0_TLS_GD      #  X1 pipe hword 0 TLS GD offset 
        R_TILEGX_IMM16_X0_HW0_TLS_LE      #  X0 pipe hword 0 TLS LE offset 
        R_TILEGX_IMM16_X1_HW0_TLS_LE      #  X1 pipe hword 0 TLS LE offset 
        R_TILEGX_IMM16_X0_HW0_LAST_TLS_LE #  X0 pipe last hword 0 LE off 
        R_TILEGX_IMM16_X1_HW0_LAST_TLS_LE #  X1 pipe last hword 0 LE off 
        R_TILEGX_IMM16_X0_HW1_LAST_TLS_LE #  X0 pipe last hword 1 LE off 
        R_TILEGX_IMM16_X1_HW1_LAST_TLS_LE #  X1 pipe last hword 1 LE off 
        R_TILEGX_IMM16_X0_HW0_LAST_TLS_GD #  X0 pipe last hword 0 GD off 
        R_TILEGX_IMM16_X1_HW0_LAST_TLS_GD #  X1 pipe last hword 0 GD off 
        R_TILEGX_IMM16_X0_HW1_LAST_TLS_GD #  X0 pipe last hword 1 GD off 
        R_TILEGX_IMM16_X1_HW1_LAST_TLS_GD #  X1 pipe last hword 1 GD off 
        R_TILEGX_IMM16_X0_HW0_TLS_IE      #  X0 pipe hword 0 TLS IE offset 
        R_TILEGX_IMM16_X1_HW0_TLS_IE      #  X1 pipe hword 0 TLS IE offset 
        R_TILEGX_IMM16_X0_HW0_LAST_TLS_IE #  X0 pipe last hword 0 IE off 
        R_TILEGX_IMM16_X1_HW0_LAST_TLS_IE #  X1 pipe last hword 0 IE off 
        R_TILEGX_IMM16_X0_HW1_LAST_TLS_IE #  X0 pipe last hword 1 IE off 
        R_TILEGX_IMM16_X1_HW1_LAST_TLS_IE #  X1 pipe last hword 1 IE off 
        R_TILEGX_TLS_DTPMOD64             #  64-bit ID of symbol's module 
        R_TILEGX_TLS_DTPOFF64             #  64-bit offset in TLS block 
        R_TILEGX_TLS_TPOFF64              #  64-bit offset in static TLS block 
        R_TILEGX_TLS_DTPMOD32             #  32-bit ID of symbol's module 
        R_TILEGX_TLS_DTPOFF32             #  32-bit offset in TLS block 
        R_TILEGX_TLS_TPOFF32              #  32-bit offset in static TLS block 
        R_TILEGX_TLS_GD_CALL              #  "jal" for TLS GD 
        R_TILEGX_IMM8_X0_TLS_GD_ADD       #  X0 pipe "addi" for TLS GD 
        R_TILEGX_IMM8_X1_TLS_GD_ADD       #  X1 pipe "addi" for TLS GD 
        R_TILEGX_IMM8_Y0_TLS_GD_ADD       #  Y0 pipe "addi" for TLS GD 
        R_TILEGX_IMM8_Y1_TLS_GD_ADD       #  Y1 pipe "addi" for TLS GD 
        R_TILEGX_TLS_IE_LOAD              #  "ld_tls" for TLS IE 
        R_TILEGX_IMM8_X0_TLS_ADD          #  X0 pipe "addi" for TLS GD/IE 
        R_TILEGX_IMM8_X1_TLS_ADD          #  X1 pipe "addi" for TLS GD/IE 
        R_TILEGX_IMM8_Y0_TLS_ADD          #  Y0 pipe "addi" for TLS GD/IE 
        R_TILEGX_IMM8_Y1_TLS_ADD          #  Y1 pipe "addi" for TLS GD/IE 
        R_TILEGX_GNU_VTINHERIT            #  GNU C++ vtable hierarchy 
        R_TILEGX_GNU_VTENTRY              #  GNU C++ vtable member usage 
        R_TILEGX_NUM                      # 
