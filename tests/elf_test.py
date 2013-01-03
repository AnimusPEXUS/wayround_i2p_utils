
import os

import org.wayround.utils.format.elf

count = 0

for i in os.walk("/home/agu/_sda3/_UNICORN/b/gajim/gajim-0.15.2--20130102.174429.0729418-1jmqw0/04.DESTDIR"):

    i[2].sort()
    for j in i[2]:

#        org.wayround.utils.format.elf.test_empty()
        file_n = os.path.join(i[0], j)
        print("file: {}".format(file_n))
        libs = org.wayround.utils.format.elf.get_libs_list(file_n)

        print("libs:")
        print(repr(libs))

        count += 1

print("Count: {}".format(count))
