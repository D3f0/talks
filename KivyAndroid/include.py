#!/usr/bin/env python

"""
Pandoc filter to process code blocks with class "include" and
replace their content with the included file
Additional features: Pradeep Gowda <@btbytes> 2014-08-28
- include only code between "start=x" and "end=y" line numberLines
- if '.numberLines' is specified in code fence, the line numbers shown
will correspond to the actual file line numbers.
Additional annotation to the fenced code blocks:
~~~~{.python .numberLines include="hello.py" start="1" end="3"}
~~~~
Typical Usage:
pandoc sample.md -t json | ./include.py | pandoc -f json -t html -s
"""

from pandocfilters import toJSONFilter, CodeBlock


def picklines(thefile, whatlines):
    return "".join([x for i, x in enumerate(thefile) if i in whatlines])


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def code_include(key, value, format, meta):
    if key == 'CodeBlock':
        [[ident, classes, namevals], code] = value
        start = -1
        end = -1
        for nameval in namevals:
            if nameval[0] == 'start':
                start = int(nameval[1]) - 1
            if nameval[0] == 'end':
                end = int(nameval[1])

        for nameval in namevals:
            if nameval[0] == 'include':
                fname = nameval[1]
                content = ""
                if start < 0:
                    thefile = open(fname, 'rb')
                    content = thefile.read()
                else:
                    if end < 0:
                        end = file_len(fname)
                    thefile = open(fname, 'rb')
                    content = picklines(thefile, range(start, end))
                content.decode('utf-8')
                if 'numberLines' in classes:
                    namevals.append(('startFrom', str(start + 1)))
                return CodeBlock([ident, classes, namevals], content)

if __name__ == "__main__":
    toJSONFilter(code_include)
