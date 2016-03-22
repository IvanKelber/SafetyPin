import csv
from isItDark import isItDark
import sqlite3
from scipy import stats

# See "TO DO" from isItDark.py

def main():

    # Things that I'm hard-coding because I'm feeling lazy...
    cities = {1:'NewYork', 2:'Chicago', 3:'Boston', 4:'Denver', 5:'Philly'}
    months = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep': 9, 'Oct':10, 'Nov':11, 'Dec':12}

    # Get ready to use SQL
    conn = sqlite3.connect("../crime.db")
    cursor = conn.cursor();

    # Query our database to get hour, minute, month, day, and year for all crimes in all cities
    events = []
    cursor.execute("select city_id,hour,minute,month,day,year from (select * from fact \
            inner join time \
            on fact.time_id = time.id) time_join \
        inner join date \
        on time_join.date_id = date.id")

    # Initialize our counts for daylight and darkness
    light_total = 0
    dark_total = 0
    light_by_city = {}
    dark_by_city = {}
    for city_id,city in cities.items():
        light_by_city[city] = 0
        dark_by_city[city] = 0

    # Count the number of crimes in the daylight and the darkness
    allcrimes = cursor.fetchall()

    for event in allcrimes:
        city = cities[event[0]]
        hour = event[1] / 100
        minute = event[2]
        month = months[event[3].encode('utf-8')]
        day = event[4]
        year = event[5]
        if isItDark(city, month, day, year, hour, minute):
            dark_total += 1
            dark_by_city[city] += 1
        elif ~isItDark(city, month, day, year, hour, minute):
            light_total += 1
            light_by_city[city] += 1

    # Perform binomial tests
    # Null hypothesis: The probability of a crime being committed in the daylight/darkness is 0.5    for 
    pval_total = stats.binom_test([light_total,dark_total])
    print 'p-value for all cities ' + str(pval_total)

    pval = {}
    for city_id,city in cities.items():
        pval[city] = stats.binom_test([light_by_city[city],dark_by_city[city]])
        print 'p-value for ' + city + ' ' + str(pval[city])


if __name__ == '__main__':
    main()
