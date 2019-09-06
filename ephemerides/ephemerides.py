'''
Module that scrap the ESO ephmerides
and get the ephemerides for the present month
and the present night

@place: ESO - La Silla - Paranal Observatory
@author(s): R. Thomas, T. Berg
@year(s): 2019
@First version: 19.6-1
@Current version: 19.7-0
@Telescope(s): ALL
@Instrument(s): ALL
@Licence: GPLv3
@Testable: yes

Change log:
-----------
19.6-3 - in get_eso_now removed [2:] on self.month_data for loop.
to fix a bug on change of month. Code now works with
change of month (can test with changing the system clock).
'''

###standard Library import
import os
import datetime

##testing
import unittest

##local imports
from . import hardcoded
from . import miscellaneous as misc

class get_times():
    '''
    This class create the get_times object.
    This object should be the only one to be
    used when looking for ESO ephemerides

    This class does not compute anything. It fetches the
    time from the ESO-ephemerides website and take 
    everything from there.

    The current time is given by the clock of the system
    '''
    def __init__(self, observatory, today=False):
        '''
        Class initialization
        Parameters
        ----------
        Observatory : str
                      name of the observatory for which we want the ephemerides

        today :  datetime object
                 Optional: if none is given the module will take the present!
                 with datetime.datetime.now()

        Returns
        -------
        None
        '''
        if not today:
            today = datetime.datetime.now()

        ##attributes:
        self.obs = observatory

        ###get current time information
        self.get_system_time(today)

        ## get_month_data
        self.get_month_data()

        ##and get the line of today in the table
        self.get_eso_now()

        ##finally compute the fraction of night
        self.get_night_fractions()

    def get_system_time(self, today):
        '''
        This method look at the system date and grab it
        Parameters
        ----------
        today   datetime object
                datetime.datetime.now()

        Returns
        -------
        None
        '''
        ###if we are the first day of the month we must go back 12h to get to the right evening
        if today.hour < 12:
            self.tomorrow = today
            today = today - datetime.timedelta(hours=12)
        else:
            self.tomorrow = today + datetime.timedelta(hours=12)

        self.year = today.year
        self.month = today.month
        self.day = today.day
        self.time = today.hour
        self.issummer = None
        self.winter = hardcoded.daylight_save[str(self.year)][0]
        self.summer = hardcoded.daylight_save[str(self.year)][1]
        if today>self.summer or today<self.winter:
            self.daylight_save = 1
        else:
            self.daylight_save = 0

    def get_month_data(self):
        '''
        Get monthly ephemerides
        Parameters
        ----------
        None

        Returns
        -------
        None
        '''

        ##First we create the file name
        filename = 'ESO_ephe_%s_%s_%s.txt'%(self.obs, self.year, self.month)
        with_path = os.path.join(hardcoded.home_hidden, filename)

        if not os.path.isfile(with_path):
            raise No_ephemerides_file('Please download the ephemerides with'+\
                    'eso_time.get_yearly_ephemerides')

        ##open it and read it
        with  open(with_path, 'r') as F:
            lines = F.readlines()

        ##and get the data
        self.month_header = lines[40:47]
        month_data = lines[50:]
        month_data = [i.replace('.....', '.. ..') for i in month_data]
        good = []
        for i in month_data:
            if i.split():
                day_evening = i.split()[2].split('/')[0]
                if datetime.datetime(year=self.year, month=self.month, day=int(day_evening))\
                     >= self.summer or datetime.datetime(year=self.year, month=self.month, \
                     day=int(day_evening)) <= self.winter - datetime.timedelta(hours=24): 
                    new_i = i[:43] + str(int(i[43:45])+1) + i[45:50] + str(int(i[50:52])+1) +\
                            i[52:58] + str(int(i[58:59])+1) + i[59:64] + str(int(i[64:65])+1) + i[65:]
                    good.append(new_i) 

                elif datetime.datetime(year=self.year, month=self.month, day=int(day_evening))\
                        >= self.summer-datetime.timedelta(hours=24): 
                    new_i =  i[:58] + str(int(i[58:59])+1) + i[59:64] + str(int(i[64:65])+1) + i[65:]
                    good.append(new_i)
 
                elif datetime.datetime(year=self.year, month=self.month, day=int(day_evening))\
                        == self.winter: 
                    new_i = i[:43] + str(int(i[43:45])+1) + i[45:50] + str(int(i[50:52])+1) + i[52:] 
                    good.append(new_i)


                else:
                    good.append(i)
            else:
                good.append('')

        self.month_data = good 

    def get_eso_now(self):
        '''
        This method take the table of ephemerides
        of the current month and get the line of today
        Parameters
        ----------
        None

        Returns
        -------
        None
        '''

        #If we are after noon we use the present day
        #if we are before we use the previous day
        #compare it with the table
        for i in self.month_data:
            if i.split():
                #element with the day of the evening
                day_evening = i.split()[2].split('/')[0]
                # and compare
                if int(day_evening) == self.day:
                    self.day_data = i
                    break


    def get_night_fractions(self):
        '''
        This method extracts the nights fraction for the present night
        '''

        ##split the line:
        split = self.day_data.split()

        ##extract sunset and sunrise data
        ##and transform to datetime object

        self.sunset = datetime.datetime(self.year, self.month, self.day, \
                int(split[9]), int(split[10]), 00)
        self.twi_eve = datetime.datetime(self.year, self.month, self.day, \
                int(split[11]), int(split[12]), 00)
        self.twi_mor = datetime.datetime(self.tomorrow.year, self.tomorrow.month, \
                self.tomorrow.day, int(split[13]), int(split[14]), 00)
        self.sunrise = datetime.datetime(self.tomorrow.year, self.tomorrow.month, \
                self.tomorrow.day, int(split[15]), int(split[16]), 00)

        ##and compute worthy information
        self.night_length = self.twi_mor-self.twi_eve
        self.half_night = self.night_length/2
        self.tenth_night = self.night_length/10

        ###get all tenth of night points
        self.fractions = {}
        for i in range(10):
            self.fractions['%sn'%((i+1)/10)] = self.twi_eve + (i+1)*self.night_length/10


###define errors
class No_ephemerides_file(Exception):
    def __init__(self, value):
        self.error = value


class eso_time_test(unittest.TestCase):
    '''
    Class that define the tests for the eso_time module
    '''
    def test_today_attributes(self):
        '''
        In this test we check that year, month,
        day and time are the one we provided
        '''

        ##create the object (in the afternoon)
        fake = datetime.datetime(2019, 6, 15, 14)
        mytime = get_times('Paranal', fake)

        self.assertEqual(mytime.time, fake.hour)
        self.assertEqual(mytime.year, fake.year)
        self.assertEqual(mytime.month, fake.month)

        ##try in the morning!!
        fake = datetime.datetime(2019, 6, 15, 2)
        mytime = get_times('Paranal', fake)
        fake_new = fake-datetime.timedelta(hours=12)
        self.assertEqual(mytime.day, fake_new.day)


        ##try in the morning on 1st of the month!!
        fake = datetime.datetime(2019, 7, 1, 2)
        mytime = get_times('Paranal', fake)
        fake_new = fake-datetime.timedelta(hours=12)
        self.assertEqual(mytime.day, fake_new.day)

    def test_today_data(self):
        '''
        This test check that the line from the ESO sheet
        is the right one
        '''
        ##create the object
        fake = datetime.datetime(2019, 6, 15, 2)
        mytime = get_times('Paranal', fake)

        ##line from the sheet
        expect = 'Fri Jun 14/Sat Jun 15  8649.7   16 51 02'+\
                '   18 08  19 22   6 02  7 16   12 12  22 54   16 02   5 42    94  15 42.4 -15 26\n'
        ##and compare
        self.assertEqual(expect, mytime.day_data)


        ##same day, later in the afternoon
        ##create the object
        fake = datetime.datetime(2019, 6, 15, 16)
        mytime = get_times('Paranal', fake)

        expect = 'Sat Jun 15/Sun Jun 16  8650.7   16 54 58'+\
                '   18 09  19 22   6 03  7 16   12 16  22 58   16 46   6 41    98  16 37.1 -18 47\n'
        self.assertEqual(expect, mytime.day_data)


    def test_night_length(self):
        '''
        This test check that the length computation is
        correct
        '''
        misc.get_yearly_ephemerides('Paranal', datetime.datetime(year=2019, month=6, day=1))
        ##create the object
        fake = datetime.datetime(2019, 6, 15, 2)
        mytime = get_times('Paranal', fake)

        expect_nightlength = datetime.timedelta(hours=10, minutes=40)
        self.assertEqual(mytime.night_length, expect_nightlength)

        expect_nighttenth = datetime.timedelta(hours=1, minutes=4)
        self.assertEqual(mytime.tenth_night, expect_nighttenth)

        expect_nighthalf = datetime.timedelta(hours=5, minutes=20)
        self.assertEqual(mytime.half_night, expect_nighthalf)
