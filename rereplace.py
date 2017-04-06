#!/usr/bin/env python3

import sys
import re
import os
import select
from binaryornot.check import is_binary

# support renaming files as well

# support input from stdin like find
# http://stackoverflow.com/questions/3762881/how-do-i-check-if-stdin-has-some-data

if sys.version_info.major < 3:
    print("Must have Python 3")
    sys.exit()

if len(sys.argv) < 2 or sys.argv[1] == 'help':
    print("""This is the python regexp find and replace utility.
Created by Sam Bender 2017.

Note: by default, this utility does not replace text. It only outputs what the replacement would have been. In oder to execute the replacement, add the --exec or -e flag.

The options listed below must come *before* and files.

Options:
  -e or --exec: perform the replacement. by default, the replacement is not performed.

Usage:
  rereplace "search_pattern" "replace_pattern" file1 file2 file3 ...
  find . | rereplace "search_pattern" "replace_pattern" -t

Examples:
  rereplace "hello" "HELLO THERE" *

Regex cheat sheet:
  Characters that need to be escaped: *\.^$+?[]()|
  The first capture group backreference is \1""")
    sys.exit()

valid_options = ['--exec', '-e']

search_pattern = sys.argv[1]
replace_pattern = sys.argv[2]
options = list( filter(lambda s: s in valid_options, sys.argv) )

if sys.stdin:
    files = [l.rstrip() for l in sys.stdin]
else:
    files_start_index = 2 + len(options) + 1
    files = sys.argv[files_start_index:]

if False:
    print('sys.argv = ' + str(sys.argv))
    print('files = ' + str(files))

compiled_pattern = re.compile(search_pattern)
line_end_compiled = re.compile('.*\n')

arrow_color = '\033[91m'
bold_format = '\033[1m'
end_format = '\033[0m'

if '-e' in options or '--exec' in options:
    print('EXECUTING replacement')

fencepost_newline = ""
match_found = False

for fpath in files:
    if os.path.isfile(fpath) is False or '.git' in fpath or fpath.endswith('.swp'): 
        continue

    with open(fpath, 'r') as f:
        contents = f.read()

    if compiled_pattern.search(contents):
        match_found = True
        if is_binary(fpath):
            print('Skipping matches for binary file <{0}>'.format(fname))
            continue

        print(bold_format + fencepost_newline + "<" + fpath + ">" + end_format)
        fencepost_newline = "\n"

        # pre-parse file contents so we can print out line numbers
        # based on http://stackoverflow.com/a/16674895/337934
        lines = []
        for m in re.finditer(line_end_compiled, contents):
            lines.append(m.end())

        # print out the replacements
        for match in compiled_pattern.finditer(contents):
            line_no = next(i for i in range(len(lines)) if lines[i] > match.start())
            match = match.group(0)
            replacement = re.sub(compiled_pattern, replace_pattern, match)
            print('[{}] {} {}=>{} {}'.format(line_no, match, arrow_color + bold_format, end_format, replacement))

        # perform the replacement if in execute mode
        if '-e' in options or '--exec' in options:
            with open(fpath, 'w') as f:
                f.write(re.sub(compiled_pattern, replace_pattern, contents))

if match_found == False:
    print('No matches found in {} files'.format(len(files)))






