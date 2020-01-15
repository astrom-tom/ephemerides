'''
Module that scrap the ESO ephmerides
and get the ephemerides for the present month
and the present night

@place: ESO - La Silla - Paranal Observatory
@author(s): R. Thomas, T. Berg
@year(s): 2019
@First version: 19.6-1
@Current version: 20.1-1
@Telescope(s): ALL
@Instrument(s): ALL
@Licence: GPLv3
@Testable: yes

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
        self.next_year = int(today.year)+1
        self.month = today.month
        self.day = today.day
        self.time = today.hour
        self.issummer = None
        self.winter = hardcoded.daylight_save_chile[str(self.year)][0]
        self.summer = hardcoded.daylight_save_chile[str(self.next_year)][1]
        self.winter_EU = hardcoded.daylight_save_EU[str(self.year)][0]
        self.summer_EU = hardcoded.daylight_save_EU[str(self.next_year)][1]
 
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
        self.month_header = lines[38:45]
        month_data = lines[49:]
        month_data = [i.replace('.....', '.. ..') for i in month_data]
        good = []
        for i in month_data:
            if i.split():
                day_evening = i.split()[2].split('/')[0]
                day_evening_date = datetime.datetime(year=self.year, month=self.month, day=int(day_evening))
                if day_evening_date >= self.summer and day_evening_date<= self.winter_EU - datetime.timedelta(hours=24): 
                    new_i = i[:43] + str(int(i[43:45])+1) + i[45:50] + str(int(i[50:52])+1) +\
                            i[52:58] + str(int(i[58:59])+1) + i[59:64] + str(int(i[64:65])+1) + i[65:]
                    good.append(new_i) 
 
                elif day_evening_date >= self.winter_EU and day_evening_date<= self.summer_EU - datetime.timedelta(hours=24): 
                    new_i = i[:43] + str(int(i[43:45])) + i[45:50] + str(int(i[50:52])) +\
                            i[52:58] + str(int(i[58:59])) + i[59:64] + str(int(i[64:65])) + i[65:]
                    good.append(new_i) 
 
                elif day_evening_date >= self.summer_EU-datetime.timedelta(hours=24) and day_evening_date<self.winter: 
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


    def to_dir_format(self):
        '''
        Method that transform the current date into
        a directory format, e.g., 2019-08-07
        '''
        if len(str(self.day)) == 1:
            day = '0%s'%self.day
        else:
            day = self.day
        if len(str(self.month)) == 1:
            month = '0%s'%self.month
        else:
            month = self.month

        return '%s-%s-%s'%(self.year, month, day)


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
        fake = datetime.datetime(2020, 2, 15, 14)
        mytime = get_times('Paranal', fake)

        self.assertEqual(mytime.time, fake.hour)
        self.assertEqual(mytime.year, fake.year)
        self.assertEqual(mytime.month, fake.month)

        ##try in the morning!!
        fake = datetime.datetime(2020, 2, 15, 2)
        mytime = get_times('Paranal', fake)
        fake_new = fake-datetime.timedelta(hours=12)
        self.assertEqual(mytime.day, fake_new.day)


        ##try in the morning on 1st of the month!!
        fake = datetime.datetime(2020, 2, 1, 2)
        mytime = get_times('Paranal', fake)
        fake_new = fake-datetime.timedelta(hours=12)
        self.assertEqual(mytime.day, fake_new.day)

    def test_today_data(self):
        '''
        This test check that the line from the ESO sheet
        is the right one
        '''
        ##create the object
        fake = datetime.datetime(2020, 2, 15, 2)
        mytime = get_times('Paranal', fake)

        ##line from the sheet
        expect = 'Fri Feb 14/Sat Feb 15  8894.6    7 56 48'+\
                 '   20 31  21 44   6 08  7 21    5 40  14 06    0 31  .. ..    58  15 00.8 -12 12\n'
        ##and compare
        self.assertEqual(expect, mytime.day_data)


        ##same day, later in the afternoon
        ##create the object
        fake = datetime.datetime(2020, 2, 15, 23)
        mytime = get_times('Paranal', fake)

        expect = 'Sat Feb 15/Sun Feb 16  8895.6    8 00 44'+\
                 '   20 30  21 43   6 09  7 21    5 43  14 11    1 14  .. ..    47  15 54.8 -16 26\n'
        self.assertEqual(expect, mytime.day_data)


    def test_night_length(self):
        '''
        This test check that the length computation is
        correct
        '''
        misc.get_yearly_ephemerides('Paranal', datetime.datetime(year=2020, month=2, day=1))
        ##create the object
        fake = datetime.datetime(2020, 2, 15, 23)
        mytime = get_times('Paranal', fake)

        expect_nightlength = datetime.timedelta(hours=8, minutes=26)
        self.assertEqual(mytime.night_length, expect_nightlength)

        expect_nighttenth = datetime.timedelta(minutes=50, seconds=36)
        self.assertEqual(mytime.tenth_night, expect_nighttenth)

        expect_nighthalf = datetime.timedelta(hours=4, minutes=13)
        self.assertEqual(mytime.half_night, expect_nighthalf)


