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
import datetime
from pathlib import Path

###hidden directory where we save files
home_hidden = os.path.join(str(Path.home()), '.ephemerides')


###saving daylight time dates in Chile
daylight_save_chile = {'2019': [datetime.datetime(year=2019, month=4, day=7), datetime.datetime(year=2019, month=9, day=8)],
                 '2020': [datetime.datetime(year=2020, month=4, day=4), datetime.datetime(year=2020, month=9, day=6)],
                 '2021': [datetime.datetime(year=2021, month=4, day=4), datetime.datetime(year=2021, month=9, day=5)],
                 '2022': [datetime.datetime(year=2022, month=4, day=3), datetime.datetime(year=2022, month=9, day=4)]}

###saving daylight time dates in Chile
daylight_save_EU = {'2019': [datetime.datetime(year=2019, month=10, day=13), datetime.datetime(year=2019, month=3, day=31)],
                    '2020': [datetime.datetime(year=2020, month=10, day=25), datetime.datetime(year=2020, month=3, day=8)]}



###observatories:
observatories = {'Paranal':'v',\
                 'LaSilla':'e',\
                 'Tololo':'t'}

###ESO url
ephemerides_url = 'http://www.eso.org/sci/bin/skycalendar?site=%s&year=%s&ms=%s&me=%s'

###header of the file is hardcoded
ephemerides_header1 = 'Date (eve/morn)      JDmid    LMSTmidn   ---------- Sun: ---------'+\
                       '   LST twilight:  ------------- Moon: --------------'
ephemerides_header2 = '(2019 at start)    (-2450000)            set  twi.end twi.beg rise'+\
                      '    eve   morn    rise    set  %illum   RA      Dec'

