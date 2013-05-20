import mako.filters

mako.filters.DEFAULT_ESCAPES['u_path'] = 'filters.u_path_escape'

def u_path_escape(text):
    return urllib.parse.quote(text)

mako.filters.u_path_escape = u_path_escape
