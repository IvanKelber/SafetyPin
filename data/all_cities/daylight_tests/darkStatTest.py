import csv
from isItDark import isItDark
import sqlite3
from scipy import stats

def main():

    # Things that I'm hard-coding because I'm feeling lazy...
    cities = {1:'NewYork', 2:'Chicago', 3:'Boston', 4:'Denver', 5:'Philly'}
    months = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep': 9, 'Oct':10, 'Nov':11, 'Dec':12}

    # Get ready to use SQL
    conn = sqlite3.connect("../crime_new.db")
    cursor = conn.cursor()

    # Query our database to build a dictionary of offense IDs to offense names
    crimes = {}
    cursor.execute("select * from offense")
    for crime in cursor.fetchall():
            crimes[crime[0]] = crime[1].encode('utf-8')

    # Now, what we actually care about:
    # Query our database to get hour, minute, month, day, and year for all crimes in all cities
    cursor.execute("select city_id,offense_id,hour,minute,month,day,year from (select * from fact \
            inner join time \
            on fact.time_id = time.id) time_join \
        inner join date \
        on time_join.date_id = date.id")

    # Initialize our counts for daylight and darkness
    # Total
    light_total = 0
    dark_total = 0

    # By city
    light_by_city = {}
    dark_by_city = {}
    for city_id,city in cities.items():
        light_by_city[city] = 0
        dark_by_city[city] = 0

    # By type of crime
    light_by_crime = {}
    dark_by_crime = {}
    for crime_id,crime in crimes.items():
        light_by_crime[crime] = 0
        dark_by_crime[crime] = 0

    # Count the number of crimes in the daylight and the darkness
    # Total, by city, and by type of crime
    allcrimes = cursor.fetchall()
    for event in allcrimes:
        city = cities[event[0]]
        crime = crimes[event[1]].encode('utf-8')
        hour = event[2] / 100
        minute = event[3]
        month = months[event[4].encode('utf-8')]
        day = event[5]
        year = event[6]
        if isItDark(city, month, day, year, hour, minute): # Darkness
            dark_total += 1
            dark_by_city[city] += 1
            dark_by_crime[crime] += 1
        elif ~isItDark(city, month, day, year, hour, minute): # Daylight
            light_total += 1
            light_by_city[city] += 1
            light_by_crime[crime] += 1

    # Perform binomial tests
    # Null hypothesis: The probability of a crime being committed in the daylight/darkness is 0.5
    # Total
    print '------------------------------------------------'
    print '----- Across all cities and types of crime -----'
    print '------------------------------------------------'
    pval_total = stats.binom_test([light_total,dark_total])
    print 'Daylight: ' + str(light_total) + ' incidents | Darkness: ' + str(dark_total) + ' incidents'
    print 'P-Value: ' + str(pval_total) + '\n'
    
    # By city
    print '------------------------------------------------'
    print '------ By city, across all types of crime ------'
    print '------------------------------------------------'
    pval_by_city = {}
    for city_id,city in cities.items():
        pval_by_city[city] = stats.binom_test([light_by_city[city],dark_by_city[city]])
        print city.upper()
        print 'Daylight: ' + str(light_by_city[city]) + ' incidents | Darkness: ' + str(dark_by_city[city]) + ' incidents'
        print 'P-Value: ' + str(pval_by_city[city]) + '\n'

    # By type of crime
    print '------------------------------------------------'
    print '----- By type of crime, across all cities ------'
    print '------------------------------------------------'
    pval_by_crime = {}
    for crime_id,crime in crimes.items():
        pval_by_crime[crime] = stats.binom_test([light_by_crime[crime],dark_by_crime[crime]])
        print crime
        print 'Daylight: ' + str(light_by_crime[crime]) + ' incidents | Darkness: ' + str(dark_by_crime[crime]) + ' incidents'
        print 'P-Value: ' + str(pval_by_crime[crime]) + '\n'
    
if __name__ == '__main__':
    main()
