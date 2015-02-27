import glob
import unittest

# need to run this file from within this directory
test_file_strings = glob.glob('test_unit_*.py')
print test_file_strings
module_strings = [str[0:len(str)-3] for str in test_file_strings]
suites = [unittest.defaultTestLoader.loadTestsFromName(str) 
          for str in module_strings]
testSuite = unittest.TestSuite(suites)
text_runner = unittest.TextTestRunner().run(testSuite)
