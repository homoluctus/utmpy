import sys
import unittest
from io import StringIO

sys.path.append('/app/utmpy')
import utmpy

class TestUtmp(unittest.TestCase):
    def setUp(self):
        self.utmp = utmpy.UtmpHandler()
        self.captured_stdout = StringIO()
        sys.stdout = self.captured_stdout

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_utmp_load(self):
        self.assertRaises(FileNotFoundError, self.utmp.load, "none.log")

    def test_utmp_dump_json(self):
        self.utmp.dump(data={1:1, 2:2, 3:3})
        self.assertEqual(self.captured_stdout.getvalue(), '{\n    "1": 1,\n    "2": 2,\n    "3": 3\n}\n')

    def test_utmp_dump_yaml(self):
        self.utmp.dump(data=[1, 2, 3], fmt='yaml')
        self.assertEqual(self.captured_stdout.getvalue(), '- 1\n- 2\n- 3\n\n')

if __name__ == '__main__':
    unittest.main(verbosity=2)