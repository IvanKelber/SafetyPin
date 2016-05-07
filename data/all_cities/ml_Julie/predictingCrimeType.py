# Multiclass Logistic Regression for Crime Data
import sqlite3

def main():

    # Things that I'm hard-coding because I'm feeling lazy...
    cities = {1:'NewYork', 2:'Chicago', 3:'Boston', 4:'Denver', 5:'Philly'}
    months = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep': 9, 'Oct':10, 'Nov':11, 'Dec':12}

    # Get ready to use SQL
    conn = sqlite3.connect("../crime.db")
    cursor = conn.cursor();

    # Query our database to build a dictionary of offense IDs to offense names
    crimes = {}
    cursor.execute("select * from offense")
    for crime in cursor.fetchall():
            crimes[crime[0]] = crime[1].encode('utf-8')

    # Now, what we actually care about:
    # Query our database to get latitude, longitude, and hour, minute, month, day, and year for all crimes in all cities
    events = []
    cursor.execute("select city_id,offense_id,latitude,longitude,hour,minute,month,day,year from (select * from (select * from fact \
                inner join time \
                on fact.time_id = time.id) time_join \
            inner join date \
            on time_join.date_id = date.id) date_join \
            inner join location \
            on date_join.location_id = location.id")

    allcrimes = cursor.fetchall()
    



if __name__ == '__main__':
    main()
