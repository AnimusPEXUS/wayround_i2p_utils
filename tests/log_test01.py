
import subprocess

import wayround_org.utils.log

l = wayround_org.utils.log.Log('test_logs', 'test log')

for i in range(10):
    print(">>>>>>>>> calling the cat #{}".format(i))
    subprocess.Popen(['cat', '/proc/cpuinfo'], stdout=l.stdout).wait()
