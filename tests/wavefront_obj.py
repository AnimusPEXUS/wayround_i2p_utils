
import pprint

import org.wayround.utils.format.wavefront_obj

a = org.wayround.utils.format.wavefront_obj.read_wavefront_obj_file(
    'test.obj'
    )

pprint.pprint(a)
