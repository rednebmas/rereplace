#!/usr/bin/env python3

import sys
import re
import os
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

The options listed below must come *before* and files.

Options:
  -t or --test: don't perform replacements, just output matches and replacements

Usage:
  replace "search_pattern" "replace_pattern" file1 file2 file3 ...
  find . | replace "search_pattern" "replace_pattern" -t

Examples:
  replace "hello" "HELLO THERE" *

Regex cheat sheet:
  Characters that need to be escaped: *\.^$+?[]()|
  The first capture group backreference is \1""")
    sys.exit()

valid_options = ['-t', '--test']

search_pattern = sys.argv[1]
replace_pattern = sys.argv[2]
file_pattern = sys.argv[-1]
options = list( filter(lambda s: s in valid_options, sys.argv) )

print('sys.argv = ' + str(sys.argv))

files_start_index = 2 + len(options) + 1
files = sys.argv[files_start_index:]
print('files = ' + str(files) + '\n')

compiled_pattern = re.compile(search_pattern)

arrow_color = '\033[91m'
bold_format = '\033[1m'
end_format = '\033[0m'

for fpath in files:
    if os.path.isfile(fpath) is False or '.git' in fpath or fpath.endswith('.swp'): 
        continue

    with open(fpath, 'r') as f:
        contents = f.read()

    if compiled_pattern.search(contents):
        if is_binary(fpath):
            print('Skipping matches for binary file <{0}>'.format(fname))
            continue

        print(bold_format + "<" + fpath + ">" + end_format)

        # print out the replacements
        matches = compiled_pattern.findall(contents)
        for match in matches:
            replacement = re.sub(compiled_pattern, replace_pattern, match)
            print('{} {}=>{} {}'.format(match, arrow_color + bold_format, end_format, replacement))

        # perform the replacement if not in test mode
        if '-t' not in options and '--test' not in options:
            with open(fpath, 'w') as f:
                f.write(re.sub(compiled_pattern, replace_pattern, contents))








