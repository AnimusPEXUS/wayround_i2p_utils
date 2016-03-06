
import os.path

import wayround_org.utils.path


class DataCache:

    def __init__(
            self,
            storage_directory,
            cache_name,
            cache_check_refresh_required_callback,
            cache_check_refresh_required_cb_args,
            cache_check_refresh_required_cb_kwargs,
            refresh_callback,
            refresh_cb_args,
            refresh_cb_kwargs
            ):
        """
        storage_directory - directory where cache is stored
        cache_name - name to whcih .cache extension added
        cache_check_refresh_required_callback - callable with one parameter,
            by which complete cache file name is passed. this callable should
            return:
                None - on error, True - if refresh is required, False - if
                refresh is not needed
        refresh_callback - callcble to call whan refresh is needed.
            refresh_callback must accept one parameter - complete cache
            filename, and parameters passed by refresh_cb_args and
            refresh_cb_kwargs. this callable should write fresh data into file
            pointed by first parameter
        """

        if not isinstance(storage_directory, str):
            raise TypeError("`storage_directory' must be str")

        if not isinstance(cache_name, str):
            raise TypeError("`cache_name' must be str")

        if not callable(cache_check_refresh_required_callback):
            raise TypeError(
                "`cache_check_refresh_required_callback' must be callable"
                )

        if not callable(refresh_callback):
            raise TypeError("`refresh_callback' must be callable")

        self.storage_directory = storage_directory

        if not os.path.isdir(storage_directory):
            os.makedirs(storage_directory, exist_ok=True)

        self.cache_name = cache_name

        self.cache_check_refresh_required_callback = \
            cache_check_refresh_required_callback

        self.cache_check_refresh_required_cb_args = \
            cache_check_refresh_required_cb_args

        self.cache_check_refresh_required_cb_kwargs = \
            cache_check_refresh_required_cb_kwargs

        self.refresh_callback = refresh_callback

        self.refresh_cb_args = refresh_cb_args

        self.refresh_cb_kwargs = refresh_cb_kwargs
        return

    def get_complete_filename(self):
        ret = wayround_org.utils.path.join(
            self.storage_directory,
            self.cache_name + '.cache'
            )
        return ret

    def open_cache(self):
        """
        return: None - on error, file opened in 'r' mode - on success
        """
        ret = None
        complete_filename = self.get_complete_filename()
        ct_cb_res = self.cache_check_refresh_required_callback(
            complete_filename,
            *self.cache_check_refresh_required_cb_args,
            **self.cache_check_refresh_required_cb_kwargs
            )
        if ct_cb_res is None:
            ret = None
        else:
            ct_cb_res = bool(ct_cb_res)
            if ct_cb_res is True:
                self.refresh_callback(
                    complete_filename,
                    *self.refresh_cb_args,
                    **self.refresh_cb_kwargs
                    )
            ret = open(complete_filename, 'r')
        return ret
