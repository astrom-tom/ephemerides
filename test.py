import eso_time
import datetime


##RUN TESTS
eso_time.test()

##list observatories
eso_time.list_obs()

##get yearly ephemerides
eso_time.get_yearly_ephemerides('Paranal', datetime.datetime(year=2019, month=5, day=1))

##eso_time
time = eso_time.ESO_time('Paranal', datetime.datetime(year=2019, month=7, day=1, hour=2))
print(time.day_data)



