#!/usr/bin/env python


'''
Created on March 12, 2017
for the WRAL Weather Blog.  Analysis of the Wake County Schools traditional calendar and
proposed bell schedule changes against sunrise times. Calculations are aligned with 
the US Naval Observatory's navigational definition of sunrise which accounts for 
34 arc seconds of atmospheric refraction.

Current and 2017-18 proposed bell schedules are from the Board of Education Work Session 3/7/2017
https://simbli.eboardsolutions.com/Meetings/ViewMeetingOrder.aspx?S=920&MID=3102

@author: Tony Rice
'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import matplotlib.dates as dates
import ephem
import time
from datetime import datetime, timedelta

sun = ephem.Sun()
raleigh = ephem.Observer()  
raleigh.lon, raleigh.lat = "-78.64", '35.78'
raleigh.horizon = '-0:34'  # match US Naval Observatory
raleigh.pressure = 0       # atmospheric refraction parameters

# WCPSS traditional calendars http://www.wcpss.net/calendars
WCPSSholidays2016 = ['2016-09-05', '2016-09-22', '2016-10-31', '2016-11-11', 
            '2016-11-23', '2016-11-24', '2016-11-25', '2016-12-22', 
            '2016-12-26', '2016-12-27', '2016-12-28', '2016-12-29', 
            '2016-12-30', '2017-01-02', '2017-01-16', '2017-01-27', 
            '2017-02-20', '2017-03-31', '2017-04-10', '2017-04-11', 
            '2017-04-12', '2017-04-13', '2017-04-14', '2017-05-12',
            '2017-05-29', ] 

WCPSSholidays2017 = ['2017-09-04', '2017-09-21', '2017-10-31', '2017-11-10', 
            '2017-11-22', '2017-11-23', '2017-11-24', '2017-12-22', 
            '2017-12-25', '2017-12-26', '2017-12-27', '2017-12-28', 
            '2017-12-29', '2018-01-01', '2018-01-15', '2018-01-22', 
            '2018-02-19', '2018-03-29', '2018-03-30', '2018-04-02', 
            '2018-04-03', '2018-04-04', '2018-04-05', '2018-04-06', 
            '2018-05-28', ]  # Python embraces the Oxford comma


def sunrise(date):
    raleigh.date = date
    sun.compute(raleigh)
    sr = ephem.localtime(raleigh.next_rising(sun))
    return sr

def sunrise_seconds_since_midnight(date):
    sr = sunrise(date)
    midnight = sr.replace(hour=0, minute=0, second=0, microsecond=0)
    return (sr - midnight).seconds

def schoolcalendar(start, end, holidays):
    calendar = pd.DataFrame(index=pd.date_range(start=start, end=end,  freq='D'))
    calendar['day of the week'] = calendar.index.map(lambda d: d.strftime("%a"))
    newcal = calendar.loc[~calendar.index.isin(holidays)]
    return newcal[newcal['day of the week'].isin(['Mon','Tue','Wed','Thu','Fri'])]
    
def presunrisebell(df, bell):
    df['sunrise'] = df.index.map(lambda d: sunrise(d).strftime("%X"))      # sunrise time
    df['secs'] = df.index.map(lambda d: sunrise_seconds_since_midnight(d)) # in seconds for easy filtering
    return df[(df['secs'] > bell) ] # sunrise after the bell


# WCPSS High Schools start time
bell = ((7 * 60) + 25 ) * 60   # seconds after midnight at 7:25am

WCPSS2016 = schoolcalendar('2016-08-29', '2017-06-09', WCPSSholidays2016)
darkdays2016 = presunrisebell(WCPSS2016, bell)
print 'WCPSS hs 2016'
print darkdays2016.shape
print darkdays2016

# Wake Forest High
bell = ((7 * 60) + 20 ) * 60   # seconds after midnight at 7:10 am
WF2016 = schoolcalendar('2016-08-29', '2017-06-09', WCPSSholidays2016)
darkdaysWF = presunrisebell(WF2016, bell)
print 'Wake Forest HS 2017'
print darkdaysWF.shape
print darkdaysWF

# Apex / Green Level High School proposed start time
bell = ((7 * 60) + 10 ) * 60   # seconds after midnight at 7:10 am

WCPSS2017 = schoolcalendar('2017-08-28', '2018-06-08', WCPSSholidays2017)
darkdays2017 = presunrisebell(WCPSS2017, bell)
print 'Apex HS 2017'
print darkdays2017.shape
print darkdays2017
