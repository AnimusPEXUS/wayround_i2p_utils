


def elf_deps(filename, mute=True):

    import org.wayround.utils.format.elf

    ret = org.wayround.utils.format.elf.get_libs_list(filename)

    return ret
