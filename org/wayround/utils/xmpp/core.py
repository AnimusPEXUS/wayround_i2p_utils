
import logging
import threading
import time
import xml.parsers.expat
import lxml.etree

import org.wayround.utils.stream
import org.wayround.utils.xml

class Stanza:

    def __init__(self):
        pass

class XMPPInputStreamHandler:

    def __init__(
        self,
        on_read_error = None,
        on_stream_close = None,
        on_xml_error = None,
        on_stanza_read = None,
        on_protocol_start = None
        ):

        self.on_xml_error = on_xml_error
        self.on_stream_close = on_stream_close
        self.on_read_error = on_read_error

        self.stanza_layer = False

        self.tree_builder = None
        self.tree_builder_start_depth = None

        self.depth_tracking = []


    def parse_stanza(self, boolean):

        self.stanza_layer = boolean

        if not self.stanza_layer:
            self.tree_builder = None
            self.tree_builder_start_depth = None

        return


    def start(self, name, attributes):

        self.depth_tracking.append(name)

        if len(self.depth_tracking) == 1:
            if self.on_protocol_start:
                self.on_protocol_start(name, attributes)

        if self.stanza_layer:

            if not self.tree_builder:
                self.tree_builder_start_depth = len(self.depth_tracking)
                self.tree_builder = lxml.etree.TreeBuilder()

            self.tree_builder.start(name, attributes)

        return

    def end(self, name):

        if len(self.depth_tracking) == 0:
            if self.on_xml_error:
                self.on_xml_error()
        else:

            if not self.depth_tracking[-1] == name:
                if self.on_xml_error:
                    self.on_xml_error()
            else:
                del self.depth_tracking[-1]


            if len(self.depth_tracking) == 0:
                self.on_stream_close()
            else:
                if self.stanza_layer:
                    self.tree_builder.end(name)

                    if len(self.depth_tracking) == self.tree_builder_start_depth:
                        stanza = self.tree_builder.close()

                        if self.on_read_error:
                            self.on_read_error(stanza)

                        self.tree_builder = None

        return

    def data(self, data):

        if self.stanza_layer:
            self.tree_builder.data(data)

        return

    def comment(self, text):

        if self.stanza_layer:
            self.tree_builder.comment(text)

        return

    def close(self):

        if self.on_stream_close:
            self.on_stream_close()

        return

class StanzaProcessor:

    def __init__(
        self,
        in_stream,
        out_stream,
        on_input_read_error = None,
        on_input_cutter_error = None
        ):

        self.on_input_read_error = on_input_read_error
        self.on_input_cutter_error = on_input_cutter_error

        self.turned_on = False

        self.in_stream = in_stream
        self.out_stream = out_stream

        self.sliced_stanza_queue_in = []
        self.sliced_stanza_queue_out = []

        self.input_pool = b''
        self.working_input_pool = b''

        self.output_pool = b''

        self.wait_for_stanzas = []

        self.stream_reader_thread = None
        self.stream_writer_thread = None

        self.input_pool_slicer_thread = None
        self.input_pool_slicer_error = False

        self.output_queue_processor_thread = None

        self.lxml_parser = lxml.etree.XMLParser(target = EchoTarget())


    def start(self):
        self.turned_on = True

        thread_name_in = 'Thread Appending Data to StanzaReader Input Pool'
        thread_name_out = 'Thread Appending Data to StanzaReader Output Pool'

        if not self.stream_reader_thread:
            try:
                self.stream_reader_thread = org.wayround.utils.stream.cat(
                    stdin = self.in_stream,
                    stdout = self,
                    threaded = True,
                    write_method_name = 'append_data_to_input_pool',
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
                    on_exit_callback = self.on_stream_reader_thread_exit,
                    callback_for_termination_flag = self.callback_for_termination_flag
                    )
            except:
                logging.exception("Error on starting {}".format(thread_name_in))

        if not self.stream_writer_thread:
            try:
                self.stream_writer_thread = org.wayround.utils.stream.cat(
                    stdin = self,
                    stdout = self.out_stream,
                    threaded = True,
                    write_method_name = 'write',
                    close_output_on_eof = False,
                    thread_name = thread_name_out,
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
                    flush_on_input_eof = True,
                    standard_write_method_result = True,
                    on_exit_callback = self.on_stream_writer_thread_exit,
                    callback_for_termination_flag = self.callback_for_termination_flag
                    )
            except:
                logging.exception("Error on starting {}".format(thread_name_out))

    def stop(self, wait = False):

        ret = 0

        self.turned_on = False

        if wait:
            ret = self.wait()

        return ret

    def is_working(self):

        return (
            self.turned_on
            or self.input_pool_slicer_thread
            or self.stream_reader_thread
            or self.output_queue_processor_thread
            )

    def wait(self, check_interval = 0.5, timeout = 60.0):

        ret = 0

        total_slept = 0.0

        while True:
            if not self.is_working():
                ret = 0
                break
            if total_slept >= timeout:
                ret = 1
                break
            time.sleep(check_interval)
            total_slept += check_interval

        return ret

    def on_stream_reader_thread_exit(self):
        self.stream_reader_thread = None

    def on_stream_writer_thread_exit(self):
        self.stream_writer_thread = None

    def callback_for_termination_flag(self):

        ret = False

        if not self.turned_on:
            ret = True

        return ret


    def write(self, bytes_text):

        ret = len(bytes_text)

        self.input_pool += bytes_text

        if self.input_pool_slicer_error:
            raise Exception("Some error")

        if (
            len(self.input_pool) > 0
            and
            not self.input_pool_slicer_thread
            ):

            self.input_pool_slicer_thread = threading.Thread(
                self.working_input_pool_slicer,
                'Thread of StanzaReader Input Pool',
                args = tuple(),
                kwargs = dict()
                )

            self.input_pool_slicer_thread.start()


        return ret

    def read(self, buff_size):

        # TODO: check needed
        ret = self.output_pool[:buff_size]

        self.output_pool = self.output_pool[buff_size:]

        return ret

    def working_input_pool_slicer(self):

        ret = 0

        while True:
            cut_res = self.cutout_next_stanza_from_working_input_pool()

            if cut_res in [0, 3]:
                if len(self.input_pool) > 0:
                    self.working_input_pool += self.input_pool
                    self.input_pool = b''
                else:
                    break
            else:
                ret = 1
                break

        self.input_pool_slicer_thread = None

        return ret

    def cutout_next_stanza_from_working_input_pool(self):

        ret = 0

        if self.working_input_pool.isspace():
            self.working_input_pool = b''
            ret = 0

        else:
            next_stanza_end = -1
            try:
                next_stanza_end = (
                    org.wayround.utils.xml.find_next_tag_end(self.working_input_pool)
                    )
            except:
                logging.exception("Some error while seeking for stanza end")
                ret = 1
            else:
                if next_stanza_end == -1:
                    ret = 3
                else:
                    str_repr = ''
                    try:
                        str_repr = str(
                            self.working_input_pool[:next_stanza_end],
                            encoding = 'utf-8'
                            )
                    except:
                        logging.exception("bytes to str convert exception")
                        ret = 2
                    else:
                        self.sliced_stanza_queue_in.append(str_repr)
                        self.working_input_pool = self.working_input_pool[next_stanza_end:]

        return ret

    def append_object_to_output_queue(self, obj):

        if not isinstance(obj, (str, Stanza)):
            raise TypeError("Not supported type `{}'".format(type(obj).__name__))

        self.sliced_stanza_queue_out.append(obj)

    def output_queue_processor(self):

        if not self.output_queue_processor_thread:
            self.output_queue_processor_thread = threading.Thread(
                target = self.process_next_output_queue_object,
                name = 'Output Queue Processor Thread',
                args = tuple(),
                kwargs = dict()
                )

    def process_next_output_queue_object(self):

        if len(self.sliced_stanza_queue_out) > 0:
            obj = self.sliced_stanza_queue_out[0]
            del self.sliced_stanza_queue_out[0]

            if isinstance(obj, str):
                self.output_pool += obj

            if isinstance(obj, Stanza):
                self.output_pool += str(obj)

        if len(self.output_pool) > 0:

            self.out_stream.write(bytes(self.output_pool, encoding = 'utf-8'))
            self.output_pool = b''
