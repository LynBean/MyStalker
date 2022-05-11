import nose2
import unittest

from src.__main__ import *
from src.__retrieve__ import *

class TestCase (unittest.TestCase) :
    
    # Present PB code but Absent School Code
    def test (self) :
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())


if __name__ == "__main__" :
    unittest.main()