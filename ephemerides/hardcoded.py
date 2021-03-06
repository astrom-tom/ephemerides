'''
This file is part of the ESO_time module.
It is the hardcoded parameters

@place: Marseille
@author(s): R. Thomas
@year(s): 2019
@First version: 19.7-0
@Current version: 20.1-1
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

###saving daylight time dates in Chile
daylight_save_chile = {'2014': [datetime.datetime(year=2014, month=4, day=27),
                                datetime.datetime(year=2014, month=9, day=7)],
                       '2015': [datetime.datetime(year=2015, month=4, day=27, hour=12),
                                datetime.datetime(year=2015, month=4, day=27, hour=12, minute=10)], 
                                ###no daylight savin time in 2015
                       '2016': [datetime.datetime(year=2016, month=5, day=15),
                                datetime.datetime(year=2016, month=8, day=14)],
                       '2017': [datetime.datetime(year=2017, month=5, day=14),
                                datetime.datetime(year=2017, month=8, day=13)],
                       '2018': [datetime.datetime(year=2018, month=5, day=13),
                                datetime.datetime(year=2018, month=8, day=12)],
                       '2019': [datetime.datetime(year=2019, month=4, day=7),
                                datetime.datetime(year=2019, month=9, day=8)],
                       '2020': [datetime.datetime(year=2020, month=4, day=5),
                                datetime.datetime(year=2020, month=9, day=6)],
                       '2021': [datetime.datetime(year=2021, month=4, day=4),
                                datetime.datetime(year=2021, month=9, day=5)],
                       '2022': [datetime.datetime(year=2022, month=4, day=3),
                                datetime.datetime(year=2022, month=9, day=4)]}



###saving daylight time dates in Chile
daylight_save_EU = {'2014': [datetime.datetime(year=2014, month=10, day=12),
                             datetime.datetime(year=2014, month=3, day=9)],
                    '2015': [datetime.datetime(year=2015, month=10, day=11),
                             datetime.datetime(year=2015, month=3, day=8)],
                    '2016': [datetime.datetime(year=2016, month=10, day=9),
                             datetime.datetime(year=2016, month=3, day=13)],
                    '2017': [datetime.datetime(year=2017, month=10, day=8),
                             datetime.datetime(year=2017, month=3, day=12)],
                    '2018': [datetime.datetime(year=2018, month=10, day=28),
                             datetime.datetime(year=2018, month=3, day=11)],
                    '2019': [datetime.datetime(year=2019, month=10, day=13),
                             datetime.datetime(year=2019, month=3, day=10)],
                    '2020': [datetime.datetime(year=2020, month=10, day=11),
                             datetime.datetime(year=2020, month=3, day=8)],
                    '2021': [datetime.datetime(year=2021, month=10, day=10),
                             datetime.datetime(year=2021, month=3, day=14)],
                    '2022': [datetime.datetime(year=2022, month=10, day=9),
                             datetime.datetime(year=2022, month=3, day=13)]}




###observatories:
observatories = {'Paranal':'v'}

###ESO url
ephemerides_url = 'http://www.eso.org/sci/bin/skycalendar?site=%s&year=%s&ms=%s&me=%s'

###header of the file is hardcoded
ephemerides_header1 = 'Date (eve/morn)      JDmid    LMSTmidn   ---------- Sun: ---------'+\
                       '   LST twilight:  ------------- Moon: --------------'
ephemerides_header2 = '(2019 at start)    (-2450000)            set  twi.end twi.beg rise'+\
                      '    eve   morn    rise    set  %illum   RA      Dec'

