#!/usr/bin/python3
"""
Provides a regular-expression based pattern matching class (Patty) that
recursively searches directories for files with the given file name pattern and
then uses the given regular expression to check if it matches within the lines
of the file. If a match is found in line, the first group of the match is stored
in the result-set.

Also, contains a main program that accepts as its first argument the regular
expression to be used during searches and as additional arguments Unix-shell
style filename patterns to limit the scope of the search.

Distributed under the terms of the MIT License (see below).

Copyright 2018 Georgios Migdos

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in 
the Software without restriction, including without limitation the rights to 
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import os
import sys
import glob
import re
import logging

class Patty:

  def search(self, patterns, regex):
    """ Searches all files that match the given filename patterns line-by-line
        for matches using the given regex.
    
    If one or more matches are found in a line, the first match group of the
    regex is extracted and stored to the results set.
    **IMPORTANT**: THE GIVEN REGULAR EXPRESSION MUST CONTAIN AT LEAST ONE MATCH
    GROUP!!!
    """
    files = self.__list_files(patterns)
    return self.__search_for_pattern_in_files(files, re.compile(regex))

  def __list_files(self, patterns=None):
    """ Returns a list of paths that match the given patterns (recursively).

    If the `patterns` parameter is ommitted all files are selected.
    """
    if patterns is None or len(patterns) == 0:
      patterns = ['./**/*']
    result = []
    for pattern in patterns:
        result.extend(glob.glob('./**/'+pattern, recursive=True))
    return sorted(result)

  def __search_for_pattern_line_by_line(self, f, regex, results_set):
    """ Searches a file line-by-line for the given pattern.
    
    If one or more matches are found in a line, the first match group of the
    regex is extracted and stored to the results set.
    **IMPORTANT**: THE GIVEN REGULAR EXPRESSION MUST CONTAIN AT LEAST ONE MATCH
    GROUP!!!
    """
    for line in f:
      matches_in_line = regex.findall(line)
      for m in matches_in_line:
        if len(m.strip()) > 0:
          results_set.add(m)

  def __search_for_pattern_in_files(self, file_paths, regex):
    """ Searches all the given files line-by-line for the given pattern.
    
    If one or more matches are found in a line, the first match group of the
    regex is extracted and stored to the results set.
    **IMPORTANT**: THE GIVEN REGULAR EXPRESSION MUST CONTAIN AT LEAST ONE MATCH
    GROUP!!!
    """
    result = set()
    for file in file_paths:
      try:
        with open(file, 'r', encoding='utf8') as f:
          self.__search_for_pattern_line_by_line(f, regex, result)
      except UnicodeDecodeError:
        try:
          with open(file, 'r', encoding='latin-1') as f:
            self.__search_for_pattern_line_by_line(f, regex, result)
        except:
          try:
            with open(file, 'r', encoding='cp1252') as f:
              self.__search_for_pattern_line_by_line(f, regex, result)
          except:
            logger.error('Could not process file: %s' % (file))
    return sorted(result)

if __name__=='__main__':
  
  logging.basicConfig()
  logger = logging.getLogger('patty')

  if len(sys.argv) > 2:
    patty = Patty()
    reqs = patty.search(sys.argv[2:], re.compile(sys.argv[1]))
    for req in reqs:
      print(req)
  else:
    logger.error("Invalid parameters!")
    logger.error("Usage:")
    logger.error("\tpython3 patty.py <regex_with_at_least_on_match_group> <filename_pattern_1> .. <filename_pattern_N>")
    logger.error("e.g.")
    logger.error(r"\tpython3 patty.py '(SRS_REQ_[^\s]+_[0-9]+)' *.cpp *.c *.py *.java")
    sys.exit(1)
