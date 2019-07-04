'''
This file is part of the ESO_time module.
It is the hardcoded parameters

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
import os
from pathlib import Path

###hidden directory where we save files
home_hidden = os.path.join(str(Path.home()), '.ephemerides')


###observatories:
observatories = {'Paranal':'v',\
                 'LaSilla':'e',\
                 'MaunaKea':'m',\
                 'Palomar':'p',\
                 'Tololo':'t'}

###ESO url
ephemerides_url = 'http://www.eso.org/sci/bin/skycalendar?site=%s&year=%s&ms=%s&me=%s'

###header of the file is hardcoded
ephemerides_header1 = 'Date (eve/morn)      JDmid    LMSTmidn   ---------- Sun: ---------'+\
                       '   LST twilight:  ------------- Moon: --------------'
ephemerides_header2 = '(2019 at start)    (-2450000)            set  twi.end twi.beg rise'+\
                      '    eve   morn    rise    set  %illum   RA      Dec'

