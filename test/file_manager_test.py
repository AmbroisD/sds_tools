import unittest
from utils.file_manager import test_name_format, in_white_list

class TestStringMethods(unittest.TestCase):

    def test_white_list(self):
        in_white_list()


    def test_re_test_name(self):
        class myPath:
            def __init__(self, name):
                self.name = name

        myPath.name = 'AG.FLF.00.ENE.D.2010.167'
        self.assertTrue(test_name_format(myPath))
        myPath.name = 'G.FLF..ENE.D.2010.167'
        self.assertTrue(test_name_format(myPath))
        myPath.name = 'G.FLF..ENE.D.200.167'
        self.assertFalse(test_name_format(myPath))

if __name__ == '__main__':
    unittest.main()
