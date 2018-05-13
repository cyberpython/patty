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

The 

        python3 patty.py '(SRS_REQ_[^\s]+_[0-9]+)' *.cpp *.c *.py *.java

Requirements
------------

* `Python 3.5+`


License
-------

MIT License.