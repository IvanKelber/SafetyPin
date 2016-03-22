import csv
from isItDark import isItDark
import sqlite3
import numpy as np

# See "TO DO" from isItDark.py

def main():

    cities = {1:'NewYork', 2:'Chicago', 3:'Boston', 4:'Denver', 5:'Philly'}
    months = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep': 9, 'Oct':10, 'Nov':11, 'Dec':12}

    conn = sqlite3.connect("../crime.db")
    cursor = conn.cursor();

    events = []
    cursor.execute("select city_id,hour,minute,month,day,year from (select * from fact \
            inner join time \
            on fact.time_id = time.id) time_join \
        inner join date \
        on time_join.date_id = date.id")
    for event in cursor.fetchall():
        city = cities[event[0]]
        hour = event[1] / 100
        minute = event[2]
        month = months[event[3].encode('utf-8')]
        day = event[4]
        year = event[5]
        print isItDark(city, month, day, year, hour, minute)















if __name__ == '__main__':
    main()
