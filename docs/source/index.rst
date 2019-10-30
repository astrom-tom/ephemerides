.. ephemerides documentation master file, created by
   sphinx-quickstart on Thu Jul  4 13:35:22 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Ephemerides
===========

.. toctree::
   :maxdepth: 1
   :caption: Contents:

Change log
==========
**19.10.1**:
        * Take skycalc daylight saving time into consideration

**19.9.1**:
        * Take Chile daylight saving time into consideration

**19.7.3**:
        * Add sunrise and sunset attributes

**19.7.2**:
        * Add version number

**19.7.1**:
        * First version

What is Ephemerides?
====================

*Ephemerides* is a very short module that retrieves the night information for a given date and a given observatory. All the informations are extracted from the European Southerm Observatory [ESO] ephemerides `webpage <https://www.eso.org/sci/observing/tools/calendar/skycalc.html>`_ that uses the *skycalc* tool of John Thorstensen.

As such, *ephmerides* does not make any compuation but relies on the ESO official ephemerides.


How to use it?
==============

Installation 
^^^^^^^^^^^^
*Ephemerides* is available on pip. To install is you can just use the traditional::

        pip install ephemerides --user

Using this command all the dependencies will be installed along the present module


Usage
^^^^^

*Ephemerides* must be used as any other python module.

To import it::

        In [1]: import ephemerides

For the main functinnality of the module you must select the observatory. As for now, five of them are available and can be listed via the **list_obs()** function::

        In [2]: ephemerides.list_obs()
        ['Paranal', 'LaSilla', 'Tololo']

Then, you must webscrap the epehemerides from the ESO website. To do so yyou use the **get_yearly_ephemerides()** function. The help of this function will help you to use it::

        In [3]: help(ephemerides.get_yearly_ephemerides)
        
        get_yearly_ephemerides(observatory, time=False)
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

As you can see, this function will download the ephemerides for the next year (so you do not have to do it too often). It takes one mandatory argument which is the name of the observatory. By default this function will take the ephemerides of the coming year starting from now. If you want passed ephemerides you must provide a different date. This is done using the *datetime* python module. If we are in the first case we will use and we want the ephemerides for the Paranal observatory we will do::

        In [4]: ephemerides.get_yearly_ephemerides('Paranal')

This function will webscrap all the ephemerides for the next month. The files will be places in your home directory in a hidden subdirectory called *ephemerides*. They have a format 'ESO_ephem_Observatory_name_year_month.txt' and are human readable.

Once you have them all you can use the main functionality of the code, the **get_times** object. The help of this class gives::

        In [5]: help(ephemerides.get_times)

        class get_times(builtins.object)
         |  get_times(observatory, today=False)
         |
         |  This class create the get_times object.
         |  This object should be the only one to be
         |  used when looking for ESO ephemerides
         |
         |  This class does not compute anything. It fetches the
         |  time from the ESO-ephemerides website and take
         |  everything from there.
         |
         |  The current time is given by the clock of the system
         |
         |  __init__(self, observatory, today=False)
         |      Class initialization
         |      Parameters
         |      ----------
         |      Observatory : str
         |                    name of the observatory for which we want the ephemerides
         |      
         |      today :  datetime object
         |               Optional: if none is given the module will take the present!
         |               with datetime.datetime.now()
         |      
         |      Returns
         |      -------
         |      None


As before, this class takes an observatory argument (the name of the observatory) and eventually a *today* argument that is a datetime object. If none is given, the system clock is used. In the first case::

                In [6]: t = ephemerides.get_times('Paranal')

And that's it! From this you have a lot of quantities available. 

.. Note::
        
        It is important to understand one thing when you use ephemerides. Since it has been written to reflet the current night information, the date change does not happen at midnight but at noon! So if your system clock (or the time you give as argument) is between midnight and noon, you will get all the information from the previous evening to the sunrise following it


In our current example, the code was ran at 2.11 pm on the 4th of July 2019. Consequently, the information that are accessible will be for the following night. All the attributes can be listed using **__dict__**:: 

                In [7]: t.__dict__ 

                {'obs': 'Paranal',
         'tomorrow': datetime.datetime(2019, 7, 5, 2, 11, 35, 528871),
         'year': 2019,
         'month': 7,
         'day': 4,
         'time': 14,
         'month_header': ['                                           ***** 2019 JULY *****\n',
          '\n',
          'Calendar for ESO VLT (Cerro Paranal), west longitude (h.m.s) =   4 41 36, latitude (d.m) = -24 37.4\n',
          'Note that each line lists events of one night, spanning two calendar dates.  Rise/set times are given\n',
          'in Chilean time (  4 hr W), for 2635 m above surroundings, DAYLIGHT time used, * shows night clocks are reset.\n',
          'Moon coords. and illum. are for local midnight, even if moon is down.  Program: John Thorstensen, Dartmouth College.\n',
          '\n'],
         'month_data': ['Mon Jul 01/Tue Jul 02  8666.7   17 58 03   18 12  19 26   6 05  7 19   13 23   0 04    7 01  17 18     1   6 06.5  22 00\n',
          'Tue Jul 02/Wed Jul 03  8667.7   18 02 00   18 13  19 26   6 05  7 19   13 27   0 08    8 02  18 16     0   7 07.7  22 23\n',
          'Wed Jul 03/Thu Jul 04  8668.7   18 05 56   18 13  19 26   6 06  7 19   13 31   0 12   .. ..  19 20     2   8 09.5  21 19\n',
          'Thu Jul 04/Fri Jul 05  8669.7   18 09 53   18 14  19 27   6 06  7 19   13 36   0 16   .. ..  20 25     7   9 10.5  18 50\n',
          'Fri Jul 05/Sat Jul 06  8670.7   18 13 49   18 14  19 27   6 06  7 19   13 40   0 20   .. ..  21 31    15  10 09.3  15 10\n',
          'Sat Jul 06/Sun Jul 07  8671.7   18 17 46   18 14  19 27   6 06  7 18   13 44   0 24   .. ..  22 35    24  11 05.7  10 36\n',
          '\n',
          'Sun Jul 07/Mon Jul 08  8672.7   18 21 42   18 15  19 28   6 06  7 18   13 49   0 28   .. ..  23 38    35  11 59.8   5 29\n',
          'Mon Jul 08/Tue Jul 09  8673.7   18 25 39   18 15  19 28   6 06  7 18   13 53   0 32   .. ..   0 39    46  12 52.2   0 09\n',
          'Tue Jul 09/Wed Jul 10  8674.7   18 29 36   18 15  19 28   6 06  7 18   13 57   0 36   .. ..   1 38    57  13 43.9 - 5 06\n',
          'Wed Jul 10/Thu Jul 11  8675.7   18 33 32   18 16  19 29   6 05  7 18   14 01   0 40   .. ..   2 37    68  14 35.5 -10 02\n',
          'Thu Jul 11/Fri Jul 12  8676.7   18 37 29   18 16  19 29   6 05  7 18   14 06   0 44   .. ..   3 36    78  15 27.9 -14 23\n',
          'Fri Jul 12/Sat Jul 13  8677.7   18 41 25   18 17  19 29   6 05  7 18   14 10   0 48   .. ..   4 34    86  16 21.2 -17 56\n',
          'Sat Jul 13/Sun Jul 14  8678.7   18 45 22   18 17  19 30   6 05  7 18   14 14   0 52   .. ..   5 31    92  17 15.6 -20 31\n',
          '\n',
          'Sun Jul 14/Mon Jul 15  8679.7   18 49 18   18 18  19 30   6 05  7 17   14 19   0 55   16 16   6 26    97  18 10.5 -21 59\n',
          'Mon Jul 15/Tue Jul 16  8680.7   18 53 15   18 18  19 30   6 05  7 17   14 23   0 59   17 07   7 18    99  19 05.4 -22 19\n',
          'Tue Jul 16/Wed Jul 17  8681.7   18 57 11   18 18  19 31   6 05  7 17   14 27   1 03   17 59  .. ..   100  19 59.2 -21 30\n',
          'Wed Jul 17/Thu Jul 18  8682.7   19 01 08   18 19  19 31   6 04  7 17   14 31   1 07   18 52  .. ..    98  20 51.3 -19 41\n',
          'Thu Jul 18/Fri Jul 19  8683.7   19 05 05   18 19  19 31   6 04  7 16   14 36   1 10   19 45  .. ..    95  21 41.3 -16 58\n',
          'Fri Jul 19/Sat Jul 20  8684.7   19 09 01   18 20  19 32   6 04  7 16   14 40   1 14   20 37  .. ..    90  22 29.2 -13 34\n',
          'Sat Jul 20/Sun Jul 21  8685.7   19 12 58   18 20  19 32   6 04  7 16   14 44   1 18   21 29  .. ..    83  23 15.2 - 9 39\n',
          '\n',
          'Sun Jul 21/Mon Jul 22  8686.7   19 16 54   18 21  19 32   6 04  7 15   14 49   1 21   22 19  .. ..    76   0 00.0 - 5 22\n',
          'Mon Jul 22/Tue Jul 23  8687.7   19 20 51   18 21  19 33   6 03  7 15   14 53   1 25   23 09  .. ..    67   0 44.3 - 0 53\n',
          'Tue Jul 23/Wed Jul 24  8688.7   19 24 47   18 21  19 33   6 03  7 15   14 57   1 29   24 00  .. ..    58   1 28.8   3 41\n',
          'Wed Jul 24/Thu Jul 25  8689.7   19 28 44   18 22  19 33   6 03  7 14   15 01   1 32    0 52  .. ..    48   2 14.4   8 10\n',
          'Thu Jul 25/Fri Jul 26  8690.7   19 32 40   18 22  19 34   6 02  7 14   15 06   1 36    1 46  .. ..    38   3 02.0  12 25\n',
          'Fri Jul 26/Sat Jul 27  8691.7   19 36 37   18 23  19 34   6 02  7 13   15 10   1 40    2 42  .. ..    28   3 52.3  16 13\n',
          'Sat Jul 27/Sun Jul 28  8692.7   19 40 34   18 23  19 35   6 02  7 13   15 14   1 43    3 41  .. ..    19   4 46.0  19 20\n',
          '\n',
          'Sun Jul 28/Mon Jul 29  8693.7   19 44 30   18 24  19 35   6 01  7 12   15 19   1 47    4 43  .. ..    12   5 43.2  21 29\n',
          'Mon Jul 29/Tue Jul 30  8694.7   19 48 27   18 24  19 35   6 01  7 12   15 23   1 50    5 44  .. ..     5   6 43.3  22 25\n',
          'Tue Jul 30/Wed Jul 31  8695.7   19 52 23   18 25  19 36   6 00  7 11   15 27   1 54    6 44  17 00     1   7 45.3  21 54\n',
          'Wed Jul 31/Thu Aug 01  8696.7   19 56 20   18 25  19 36   6 00  7 11   15 32   1 57    7 40  18 05     0   8 47.5  19 55\n',
          '\n'],
         'day_data': 'Thu Jul 04/Fri Jul 05  8669.7   18 09 53   18 14  19 27   6 06  7 19   13 36   0 16   .. ..  20 25     7   9 10.5  18 50\n',
         'twi_eve': datetime.datetime(2019, 7, 4, 19, 27),
         'twi_mor': datetime.datetime(2019, 7, 5, 6, 6),
         'night_length': datetime.timedelta(seconds=38340),
         'half_night': datetime.timedelta(seconds=19170),
         'tenth_night': datetime.timedelta(seconds=3834),
         'fractions': {'1/10': datetime.datetime(2019, 7, 4, 20, 30, 54),
          '2/10': datetime.datetime(2019, 7, 4, 21, 34, 48),
          '3/10': datetime.datetime(2019, 7, 4, 22, 38, 42),
          '4/10': datetime.datetime(2019, 7, 4, 23, 42, 36),
          '5/10': datetime.datetime(2019, 7, 5, 0, 46, 30),
          '6/10': datetime.datetime(2019, 7, 5, 1, 50, 24),
          '7/10': datetime.datetime(2019, 7, 5, 2, 54, 18),
          '8/10': datetime.datetime(2019, 7, 5, 3, 58, 12),
          '9/10': datetime.datetime(2019, 7, 5, 5, 2, 6),
          '10/10': datetime.datetime(2019, 7, 5, 6, 6)}}

The most important are:

* **t.obs**: The name of the observatory you have given
* **t.tomorrow**: The date of tomorrow (if you have been running the case before noon, it will be today).
* **t.month_data**: the full ephemerides table from the skycalc tool.
* **t.day_data**: The line of the table of the current night.
* **t.twi_eve**: The end of evening twilight for the current night [datetime.datetime object]
* **t.twi_mor**: The beginning of morning twilight for the current night [datetime.datetime.object]
* **t.night_length**: The length of the night [datetime.timedelta object]
* **t.half_night**: The length of half of the night [datetime.timedelta object]
* **t.tenth_night**: The duration of 1/10 of the night [datetime.timedelta]
* **t.fractions**: This is a dictionnary containing the hours of all the 1/10th of the night (1/10, 2/10....10/10). Each keyword are the fraction (e.g. 1/10) and the values are one it occures during the night (as a datetime.datetime object). 


Tests
=====

A short testing suite have been implemented in the module and can be ran with::

        In [8]: ephemerides.test()

        ---UnitTest the miscellaneous functions
        test_list_obs (ephemerides.miscellaneous.tests) ... ok

        ----------------------------------------------------------------------
        Ran 1 test in 0.000s

        OK

        ---UnitTest the ephemerides object True
        test_night_length (ephemerides.ephemerides.eso_time_test) ... ok
        test_today_attributes (ephemerides.ephemerides.eso_time_test) ... ok
        test_today_data (ephemerides.ephemerides.eso_time_test) ... ok

        ----------------------------------------------------------------------
        Ran 3 tests in 0.003s


.. warning::

	**Copyright**

	ephemerides is a free software: you can redistribute it and/or modify it under
	the terms of the GNU General Public License as published by the Free Software Foundation,
	version 3 of the License.

	ephemerides is distributed without any warranty; without even the implied warranty of merchantability
	or fitness for a particular purpose.  See the GNU General Public License for more details.

	You should have received a copy of the GNU General Public License along with the program.
	If not, see http://www.gnu.org/licenses/ .

----

.. warning::

	**Disclaimer**

	ephemerides is not supported nor endorsed by the European Southern Observatory [ESO].

