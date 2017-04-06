#!/usr/bin/env python3

import sys
import glob

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
  replace search_pattern replace_pattern file1 file2 file3 ...
  find . | replace search_pattern replace_pattern -t

Examples:
  replace "hello" "HELLO THERE" "*"

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
print('files')
print(files)

print('\nsearch pattern: ' + search_pattern)

import re
import os

compiled_pattern = re.compile(search_pattern)

for fpath in files:
    if os.path.isfile(fpath) is False or '.git' in fpath: 
        continue

    with open(fpath, 'r') as f:
        contents = f.read()

    print('here')

    if compiled_pattern.search(contents):
        print('matched')
        print("<" + fpath + ">")
        with open(fpath, 'w') as f:
            # write to file if not in test mode
            if '-t' not in options and '--test' not in options:
                f.write(re.sub(compiled_pattern, replace_pattern, contents))

            # print out the replacements
            matches = re.search(compiled_pattern, contents)
            for match in matches.groups():
                print("Match: " + match)
                print("Replacement: " + re.sub(compiled_pattern, replace_pattern, match))







