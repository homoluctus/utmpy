import sys
import unittest
import ctypes
from io import StringIO
sys.path.append('../')
from pyutmp.utmpy import utmpy

class TestUtmp(unittest.TestCase):
    def test_utmp_status(self):
        status = str(utmpy.UTMPStatus(0))
        self.assertEqual('empty', status)

    def test_utmp_struct(self):
        byte_num = utmpy.UTMPStruct()
        self.assertTrue(isinstance(byte_num, ctypes.Structure))


    def test_utmp_parse(self):
        utmp = utmpy.UtmpHandler()
        self.assertRaises(FileNotFoundError, utmp.parse, "none.log")

if __name__ == '__main__':
    unittest.main(verbosity=2)