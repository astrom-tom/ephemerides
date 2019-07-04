'''
This file organises the tests of the library
'''

##standard import
import datetime

#testing
import unittest

#local imports
from . import miscellaneous
from . import ephemerides

miscellaneous.get_yearly_ephemerides('Paranal', datetime.datetime(year=2019, month=5, day=1))

def test():
    '''
    This function calls the test of each module and run them
    '''
    ###test the command line interface
    print('\n\033[1m---UnitTest the miscellaneous functions\033[0;0m')
    suite = unittest.TestLoader().loadTestsFromModule(miscellaneous)
    unittest.TextTestRunner(verbosity=2).run(suite)

    ##test the eso_time module
    print('\n\033[1m---UnitTest the ephemerides object\033[0;0m', True)
    suite = unittest.TestLoader().loadTestsFromModule(ephemerides)
    unittest.TextTestRunner(verbosity=2).run(suite)
