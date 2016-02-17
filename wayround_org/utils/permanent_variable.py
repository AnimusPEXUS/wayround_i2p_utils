
"""
This module is for creating variable-like objects for storring size python
objects
"""

import os.path
import yaml

import wayround_org.utils.path


class PermanentMemoryDriver:
    pass


class PermanentMemoryDriverFileSystem(PermanentMemoryDriver):

    def __init__(self, directory):
        self.directory = directory
        self.counter = 0
        os.makedirs(directory, exist_ok=True)
        self.clear_garbage_variables()
        return

    def clear_garbage_variables(self):
        files = os.listdir(self.directory)
        for i in files:

            if not i.endswith('.yaml'):
                continue

            descriptor = int(i[0:i.find('.')])
            os.unlink(self.gen_descriptor_filepath())
        return

    def new(self):
        ret = self.counter
        self.counter += 1
        return ret

    def delete(self, descriptor):
        f_path = self.gen_descriptor_filepath(descriptor)
        if os.path.isfile(f_path):
            os.unlink(f_path)
        return

    def get_value(self, descriptor):
        f_path = self.gen_descriptor_filepath(descriptor)
        with open(f_path) as f:
            ret = yaml.load(f.read())
        return ret

    def set_value(self, descriptor, value):
        f_path = self.gen_descriptor_filepath(descriptor)
        with open(f_path, 'w') as f:
            f.write(yaml.dump(value))
        return

    def open(self, descriptor, flags):
        f_path = self.gen_descriptor_filepath(descriptor)
        ret = open(f_path, flags)
        return ret

    def gen_descriptor_filepath(self, descriptor):
        if not isinstance(descriptor, int):
            raise TypeError("`descriptor' must be int")
        if descriptor < 0:
            raise ValueError("`descriptor' must be >= 0")
        ret = wayround_org.utils.path.join(
            self.directory,
            '{}.yaml'.format(str(descriptor))
            )
        return ret


class PermanentMemory:

    def __init__(self, driver):
        if not isinstance(driver, PermanentMemoryDriver):
            raise TypeError(
                "invalid `driver' instance type"
                )
        self.driver = driver
        self.driver.clear_garbage_variables()
        return

    def new(self, value=None):
        return PermanentVariable(self.driver, value)


class PermanentVariable:

    def __init__(self, driver, initial):
        if not isinstance(driver, PermanentMemoryDriver):
            raise TypeError(
                "invalid `driver' instance type"
                )
        self.driver = driver
        self.descriptor = self.driver.new()
        self.set(initial)
        return

    def get(self):
        return self.driver.get_value(self.descriptor)

    def set(self, value):
        return self.driver.set_value(self.descriptor, value)

    def __del__(self):
        self.driver.delete(self.descriptor)
        return

    def open(self, flags='r'):
        return self.driver.open(self.descriptor, flags)
