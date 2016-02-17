
import os.path
import yaml
import weakref

import wayround_org.utils.path


class PermanentMemoryDriver:
    pass


class PermanentMemoryDriverFileSystem(PermanentMemoryDriver):

    def __init__(self, directory):
        self.directory = directory
        self.counter = 0

        self.active_descriptors = []

        os.makedirs(directory, exist_ok=True)

        # TODO: complete cleaner
        self.clear_garbage_variables()
        return

    '''
    def clear_garbage_variables(self):
        files = os.listdir(self.directory)
        for i in files:
            if not i in self.active_descriptors:
                os.unlink(self.descriptor_filepath())

        for i in:

        return
    '''

    def new_descriptor(self, value):
        ret = self.counter
        self.counter += 1
        return ret

    def delete(self, descriptor):
        f_path = self.gen_descriptor_filepath(descriptor)
        try:
            os.unlink(f_path)
        except:
            pass
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
        return wayround_org.utils.path.join(self.directory, descriptor)


class PermanentMemory:

    def __init__(self, driver_instance):

        if not isinstance(driver_instance, PermanentMemoryDriver):
            raise TypeError(
                "`driver_instance' must be inst of PermanentMemoryDriver"
                )

        self.driver_instance = driver_instance

        return

    def clear_garbage_variables(self):
        return self.driver_instance.clear_garbage_variables()

    def new_variable(self, value):
        return self.driver_instance.new_variable(value)

    def _add(self, permanent_variable):
        return

    def _delete(self, permanent_variable):
        self.driver_instance._delete(permanent_variable)
        return

    def _get_value(self, permanent_variable):
        return self.driver_instance._get_value(permanent_variable)


class PermanentVariable:

    def __init__(self, permanent_memory, value):

        self.permanent_memory = permanent_memory
        self.memory_descriptor = None

        return

    def __get__(self):
        return self.permanent_memory._get_value(self)

    def __del__(self):
        self.permanent_memory._delete(self)
        return
