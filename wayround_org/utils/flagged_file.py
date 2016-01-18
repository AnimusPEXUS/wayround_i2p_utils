
import os.path

import yaml

import wayround_org.utils.path
import wayround_org.utils.threading


def verify_flag_name(flagged_file, flag_name):
    if not isinstance(flagged_file, FlaggedFile):
        raise TypeError("`flagged_object' must be inst of FlaggedFile")

    if not isinstance(flag_name, str):
        raise TypeError("`flag_name' must be str")

    if not flag_name in flagged_file.possible_flags:
        raise ValueError("invalid flag_name")
    return


class FlaggedFile:

    def __init__(self, path, basename, possible_flags, object_locker=None):

        self._path = None
        self._basename = None

        self.path = path
        self.basename = basename
        self.possible_flags = possible_flags

        if object_locker is None:
            object_locker = wayround_org.utils.threading.ObjectLocker()

        self.object_locker = object_locker

        for i in possible_flags:
            setattr(self, '{}_path'.format(i), self.gen_flag_path(i))

        return

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        if not isinstance(value, str):
            raise TypeError("`path' must be str")
        self._path = value
        return

    @property
    def basename(self):
        return self._basename

    @basename.setter
    def basename(self, value):
        if not isinstance(value, str):
            raise TypeError("`basename' must be str")
        self._basename = value
        return

    def install_methods(self, obj):
        for i in [
                'get_flag_path',
                'get_is_flag_set',
                'set_flag'
                ]:
            setattr(obj, i, getattr(self, i))

        return

    def gen_flag_path(self, name):
        verify_flag_name(self, name)
        return wayround_org.utils.path.join(
            self.path,
            self.basename
            ) + '.' + name

    def get_flag_path(self, name):
        verify_flag_name(self, name)
        return getattr(self, '{}_path'.format(name))

    def get_is_flag_set(self, name):
        return os.path.isfile(
            self.get_flag_path(name)
            )

    def set_flag(self, name):
        data = self.get_flag_data(name)
        self.set_flag_data(name, data)
        return

    def set_flag_data(self, name, data):

        if not isinstance(name, str):
            raise TypeError("`name' must be str")

        if data is None:
            data = None

        if not self.get_is_flag_set(name):
            f_path = self.get_flag_path(name)
            f_path_dir = os.path.dirname(f_path)
            if not os.path.isdir(f_path_dir):
                os.makedirs(f_path_dir)
            with self.object_locker[f_path]:
                with open(f_path, 'w') as f:
                    f.write(yaml.dump(data))

        return

    def get_flag_data(self, name):

        ret = None

        if not isinstance(name, str):
            raise TypeError("`name' must be str")

        if self.get_is_flag_set(name):
            f_path = self.get_flag_path(name)
            if os.path.isfile(f_path):
                with self.object_locker[f_path]:
                    with open(f_path, 'r') as f:
                        ret = yaml.load(f.read())

        return ret

    def unset_flag(self, name):
        if not isinstance(name, str):
            raise TypeError("`name' must be str")

        if self.get_is_flag_set(name):
            f_path = self.get_flag_path(name)
            with self.object_locker[f_path]:
                os.unlink(f_path)
        return
