'''
This file is part of the ESO_time module.
It code the miscellaneous functions

@place: Marseille
@author(s): R. Thomas
@year(s): 2019
@First version: 19.7-0
@Current version: 19.7-0
@Telescope(s): ALL
@Instrument(s): ALL
@Valid for SciOpsPy: v19-10
@Documentation url:
@Last SciOps review [date + name]:
@Usage:
@Licence: GPLv3
@Testable:
@Test data place (if any required):
'''

###standard library
import unittest
import os
import sys
import io
import datetime
import requests

##third party
from bs4 import BeautifulSoup


##local imports
from . import hardcoded

def list_obs():
    '''
    This function list the observatory available
    in the module

    Parameters
    ----------
    none

    Returns
    -------
    none
    '''
    print(list(hardcoded.observatories.keys()))


def get_yearly_ephemerides(observatory, time = False):
    '''
    This function gets the ephemerides for the coming year
    Parameters
    ----------
    observatory : str, 
                  name of the observatory (use eso_time.list_obs()
                  to print the list)

    time : datetime object
           optional argument

    Return
    ------
    None
    '''

    if not os.path.isdir(hardcoded.home_hidden):
        os.makedirs(hardcoded.home_hidden)

    ##get the url
    url = hardcoded.ephemerides_url

    ##get observatory letter
    obs = hardcoded.observatories[observatory]

    ##get the start time 
    if time == False:
        now = datetime.datetime.now()
    else:
        now = time

    i = 1
    while i <= 13:
        ##create the url to fetch
        final_url = url%(obs, now.year, now.month, now.month) 

        ##We create the file name and the one with paths
        filename = 'ESO_ephe_%s_%s_%s.txt'%(observatory, now.year, now.month)
        with_path = os.path.join(hardcoded.home_hidden, filename)

        ###if the file does not already exists we scrap it
        if not os.path.isfile(with_path):
            response = requests.get(final_url)
            lines = str(BeautifulSoup(response.content, 'html.parser')).split('\n')
            ###and write it down
            with open(with_path, 'w') as F:
                for j in lines:
                    F.write(j+'\n')

        ###update to the next month
        now = now + datetime.timedelta(days=31)
        i+=1


class tests(unittest.TestCase):
    '''
    This class codes the tests of this files
    '''
    def test_list_obs(self):
        '''
        This function test that the display of the observatory 
        works correctly
        '''

        ##expected result
        exp = "['Paranal', 'LaSilla', 'Tololo']\n"

        ###first capture the output
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput

        ##start the function
        list_obs()

        ###list dir
        sys.stdout = sys.__stdout__
        printout = capturedOutput.getvalue()

        self.assertEqual(exp, printout)
