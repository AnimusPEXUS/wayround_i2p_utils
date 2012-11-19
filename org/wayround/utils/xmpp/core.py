
import logging
import threading
import time


import lxml.etree

import mako.template

import org.wayround.utils.stream
import org.wayround.utils.xml

class Stanza:

    def __init__(self):
        pass

def start_stream(
    fro,
    to,
    version = '1.0',
    xml_lang = 'en',
    xmlns = 'jabber:client',
    xmlns_stream = 'http://etherx.jabber.org/streams'
    ):

    return mako.template.Template(
        """\
<?xml version="1.0"?>
<stream:stream
    from="${ fro | x }"
    to="${ to | x }"
    version="${ version | x }"
    xml:lang="${ xml_lang | x }"
    xmlns="${ xmlns | x }"
    xmlns:stream="${ xmlns_stream | x }">
""").render(
            fro = fro,
            to = to,
            version = version,
            xml_lang = xml_lang,
            xmlns = xmlns,
            xmlns_stream = xmlns_stream
            )

def check_stream_handler_correctness(handler):

    ret = 0


    return ret


def _info_dict_to_add(handler):

    return dict(
        handler = handler,
        name = handler.name,
        tag = handler.tag,
        ns = handler.ns
        )


class XMPPInputStreamReaderTarget:

    def __init__(
        self,
        on_stream_start = None,
        on_stream_start_error = None,
        on_stream_end = None,
        on_element_readed = None
        ):

        self._on_stream_start = on_stream_start
        self._on_stream_start_error = on_stream_start_error
        self._on_stream_end = on_stream_end
        self._on_element_readed = on_element_readed

        self.clear(init = True)


    def clear(self, init = False):
        self._tree_builder = None
        self._tree_builder_start_depth = None

        self._depth_tracker = []


    def start(self, name, attributes):

        logging.debug("{} :: start tag: `{}'; attrs: {}".format(type(self).__name__, name, attributes))

        if len(self._depth_tracker) == 0:

            if name == '{http://etherx.jabber.org/streams}stream':
                if self._on_stream_start:
                    self._on_stream_start(attributes)

            else:
                if self._on_stream_start_error:
                    self._on_stream_start_error()

        else:

            if not self._tree_builder:
                self._tree_builder = lxml.etree.TreeBuilder()

            self._tree_builder.start(name, attributes)

        self._depth_tracker.append(name)

        return

    def end(self, name):

        logging.debug("{} :: end `{}'".format(type(self).__name__, name))

        self._tree_builder.end(name)

        del self._depth_tracker[-1]

        if len(self._depth_tracker) == 1:

            element = self._tree_builder.close()
            self._tree_builder = None

            if self._on_element_readed:
                self._on_element_readed(element)

        return

    def data(self, data):

        logging.debug("{} :: data `{}'".format(type(self).__name__, data))

        self._tree_builder.data(data)

        return

    def comment(self, text):

        logging.debug("{} :: comment `{}'".format(type(self).__name__, text))

        self._tree_builder.comment(text)

        return

    def close(self):

        logging.debug("{} :: close".format(type(self).__name__))

        if self._on_stream_end:
            self._on_stream_end()

        return




class XMPPInputStreamReader:

    def __init__(
        self,
        read_from,
        xml_parser
        ):
        """
        read_from - xml stream input
        """

        self._read_from = read_from

        self._xml_parser = xml_parser

        self._clean(init = True)


    def _clean(self, init = False):

        if not init:
            if self.is_working():
                raise RuntimeError("Working. Cleaning not allowed")

        self._stop_flag = False

        self._stream_reader_thread = None
        return

    def start(self):


        thread_name_in = 'Thread feeding data to XML parser'

        if self.is_working():
            raise RuntimeError("Already working")

        else:
            self._stop_flag = False

            if not self._stream_reader_thread:
                try:
                    self._stream_reader_thread = org.wayround.utils.stream.cat(
                        stdin = self._read_from,
                        stdout = self,
                        threaded = True,
                        write_method_name = '_feed',
                        close_output_on_eof = False,
                        thread_name = thread_name_in,
                        bs = (2 * 1024 ** 2),
                        convert_to_str = False,
                        read_method_name = 'read',
                        exit_on_input_eof = True,
                        waiting_for_input = False,
                        descriptor_to_wait_for_input = None,
                        waiting_for_output = False,
                        descriptor_to_wait_for_output = None,
                        apply_input_seek = False,
                        apply_output_seek = False,
                        flush_on_input_eof = False,
                        standard_write_method_result = True,
                        on_exit_callback = self._on_stream_reader_thread_exit,
                        callback_for_termination_flag = self._callback_for_termination_flag,
                        verbose = True
                        )
                except:
                    logging.exception("Error on starting {}".format(thread_name_in))
                else:
                    self._stream_reader_thread.start()

        return


    def stop(self):

        self._stop_flag = True

        self._wait()

        return

    def is_working(self):

        return (
            bool(self._stream_reader_thread)
            )

    def _wait(self):

        while True:
            if not self.is_working():
                break

            time.sleep(0.5)

        return

    def _on_stream_reader_thread_exit(self):
        self._stream_reader_thread = None

    def _callback_for_termination_flag(self):

        return self._stop_flag


    def _feed(self, bytes_text):

        logging.debug("{} :: received feed of {}".format(type(self).__name__, repr(bytes_text)))

        if not isinstance(bytes_text, bytes):
            raise TypeError("bytes_text must be bytes type")

        ret = 0

        try:
            self._xml_parser.feed(bytes_text)
        except:
            logging.debug("{} :: _feed {}".format(type(self).__name__, str(bytes_text, encoding = 'utf-8')))
            ret = 0
        else:
            ret = len(bytes_text)

        return ret

