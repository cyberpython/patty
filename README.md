patty
=====

Description
-----------

A simple Python 3.5+ script that recursively scans a directory for files that
match a set of given filename patterns and then searches each matching file 
line-by-line using a user-provided regular expression. All unique results are
printed on the standard output.


Intended use
------------

To search for a string pattern (e.g. implemented software requirement IDs)
in text files using a regular expression.


Usage
-----

The script takes as its first command-line argument a regular expression that **must have at least 1 matching group**. This regular expression defines the pattern to search for and the matching group is what is extracted from each match and appended to the result set.

Additional arguments defining Unix-shell style file name patterns can be provided to limit the files to be searched.

E.g.

        python3 patty.py '(SRS_REQ_[^\s]+_[0-9]+)' *.cpp *.c *.py *.java

Requirements
------------

* `Python 3.5+`


License
-------

MIT License.