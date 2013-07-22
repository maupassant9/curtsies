from bpython import formatter
from termformatconstants import FG_COLORS, BG_COLORS, colors
from fmtstr import fmtstr

import re


cnames = dict(zip('krgybmcwd', colors + ('default',)))

def parse(s):
    r"""
    >>> parse(u'\x01y\x03print\x04\x01C\x03 \x04\x01G\x031\x04\x01C\x03 \x04\x01Y\x03+\x04\x01C\x03 \x04\x01G\x032\x04')
    yellow("print")+cyan(" ")+green("1")+cyan(" ")+yellow("+")+cyan(" ")+green("2")
    """
    rest = s
    stuff = []
    while True:
        if not rest:
            break
        d, rest = peel_off_string(rest)
        stuff.append(d)
    return sum([fs_from_match(d) for d in stuff], fmtstr(""))

def fs_from_match(d):
    atts = {}
    if d['fg']:
        color = cnames[d['fg'].lower()]
        if color != 'default':
            atts['fg'] = FG_COLORS[color]
    if d['bg']:
        color = cnames[d['fg'].lower()]
        if color != 'default':
            atts['bg'] = FG_COLORS[color]
    if d['bold']:
        atts['bold'] = True
    return fmtstr(d['string'], **atts)

def peel_off_string(s):
    p = r"""(?P<colormarker>\x01
                (?P<fg>[krgybmcwdKRGYBMCWD]?)
                (?P<bg>[krgybmcwdKRGYBMCWD]?)?)
            (?P<bold>\x01?)
            \x03
            (?P<string>[^\x04]+)
            \x04
            (?P<rest>.*)
            """
    m = re.match(p, s, re.X | re.DOTALL)
    d = m.groupdict()
    rest = d['rest']
    del d['rest']
    return d, rest

def test():
    from pygments import format
    from bpython.formatter import BPythonFormatter
    from bpython._py3compat import PythonLexer
    from bpython.config import Struct, loadini, default_config_path
    config = Struct()
    loadini(config, default_config_path())

    all_tokens = list(PythonLexer().get_tokens('print 1 + 2'))
    formatted_line = format(all_tokens, BPythonFormatter(config.color_scheme))
    print repr(formatted_line)
    fs = parse(formatted_line)
    print repr(fs)
    print fs

if __name__ == '__main__':
    import doctest; doctest.testmod()
    test()
