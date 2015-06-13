

import wayround_org.utils.format.elf


#wayround_org.utils.format.elf.read_elf('/usr/bin/cp')
#wayround_org.utils.format.elf.read_elf('mips/cp')
e = wayround_org.utils.format.elf.ELF('/usr/bin/cp', debug=True)
#e = wayround_org.utils.format.elf.ELF('v20002d.uc')
#e = wayround_org.utils.format.elf.ELF('maya2spr.dbg', debug=True)
#e = wayround_org.utils.format.elf.ELF('mips/cp')
print(e.return_text())

exit(0)
