

import org.wayround.utils.format.elf


#org.wayround.utils.format.elf.read_elf('/usr/bin/cp')
#org.wayround.utils.format.elf.read_elf('mips/cp')
e = org.wayround.utils.format.elf.ELF('/usr/bin/cp')
e = org.wayround.utils.format.elf.ELF('v20002d.uc')
#e = org.wayround.utils.format.elf.ELF('mips/cp')
print(e.return_text())

exit(0)
