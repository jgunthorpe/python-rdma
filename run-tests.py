#!/usr/bin/env python
# Copyright 2011 Obsidian Research Corp. GPLv2, see COPYING.
import unittest,os,os.path,fnmatch
import tests

def testAll():
    """Return a test suite for everything in the test/ directory.
    Replace me with discover for Python 2.7"""
    return suite;

module = __import__("tests");
fns = [os.path.splitext(I)[0] for I in
         fnmatch.filter(os.listdir(module.__path__[0]),"*.py")];
fns.remove("__init__");
for I in fns:
    __import__("tests." + I);
suite = unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromNames(fns,module));

if __name__ == "__main__":
    unittest.main(defaultTest="testAll");
