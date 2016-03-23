import sys
import csv
import math

# INPUT: city name (string corresponding to that city's directory in our github repo), month (int), day (int), year (int), hour (int), and minute (int)

def isItDark(city, mo, d, y, h, mi):
    fname = '../../' + city + '/sun_' + str(y) + '.csv'
    with open(fname,'rb') as sundata:
        sun = list(sundata.read().splitlines())

    # Access the correct row and column
    row = sun[d-1].split(',')
    sunrise = int(row[(mo*2)-1])
    sunset = int(row[(mo*2)])

    # Adjust for Daylight Savings Time if necessary
    # SOURCE: http://aa.usno.navy.mil/faq/docs/daylight_time.php
    DSTstart = {2011:13, 2012:11, 2013:10, 2014:9, 2015:8, 2016:13} # always starts in March
    DSTend = {2011:6, 2012:4, 2013:3, 2014:2, 2015:1, 2016:6} # always end in November

    if (mo==3 and d>=DSTstart[y]) or (mo==11 and d<DSTend[y]) or (mo>3 and mo<11): # Daylight Savings Time is in effect
        sunrise += 100
        sunset += 100

    t = int(str(h) + str(mi))

    if t < sunrise: # Time is between midnight and sunrise
        #print 'Between midnight and sunrise'
        return True # It is dark
    else:
        if t < sunset: # Time is between sunrise and sunset
            #print 'Between sunrise and sunset'
            return False # It is not dark
        else: # Time is between sunset and midnight
            #print 'Between sunset and midnight'
            return True # It is dark
