import sqlite3
import numpy as np
from sklearn.preprocessing import scale
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC

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
    # Query our database to get location and date/time info for all crimes...

    # ...in all cities
    # ---TO DO--- take out and construct by combining all 5 cities (?)
    cursor.execute("select city_id,offense_id,latitude,longitude,hour,minute,month,day,year from (select * from (select * from fact \
                inner join time \
                on fact.time_id = time.id) time_join \
            inner join date \
            on time_join.date_id = date.id) date_join \
            inner join location \
            on date_join.location_id = location.id")
    allCrimes = cursor.fetchall()
    print allCrimes[0] # DEBUG

    # # ...just New York
    # cursor.execute("select city_id,offense_id,latitude,longitude,hour,minute,month,day,year from (select * from (select * from fact \
    #             inner join time \
    #             on fact.time_id = time.id) time_join \
    #         inner join date \
    #         on time_join.date_id = date.id) date_join \
    #         inner join location \
    #         on date_join.location_id = location.id \
    #         where city_id = 1")
    # NYCrimes = cursor.fetchall()

    # # ...just Chicago
    # cursor.execute("select city_id,offense_id,latitude,longitude,hour,minute,month,day,year from (select * from (select * from fact \
    #             inner join time \
    #             on fact.time_id = time.id) time_join \
    #         inner join date \
    #         on time_join.date_id = date.id) date_join \
    #         inner join location \
    #         on date_join.location_id = location.id \
    #         where city_id = 2")
    # ChiCrimes = cursor.fetchall()

    # # ...just Boston
    # cursor.execute("select city_id,offense_id,latitude,longitude,hour,minute,month,day,year from (select * from (select * from fact \
    #             inner join time \
    #             on fact.time_id = time.id) time_join \
    #         inner join date \
    #         on time_join.date_id = date.id) date_join \
    #         inner join location \
    #         on date_join.location_id = location.id \
    #         where city_id = 3")
    # BosCrimes = cursor.fetchall()

    # # ...just Denver
    # cursor.execute("select city_id,offense_id,latitude,longitude,hour,minute,month,day,year from (select * from (select * from fact \
    #             inner join time \
    #             on fact.time_id = time.id) time_join \
    #         inner join date \
    #         on time_join.date_id = date.id) date_join \
    #         inner join location \
    #         on date_join.location_id = location.id \
    #         where city_id = 4")
    # DenCrimes = cursor.fetchall()

    # # ...and just Philadelphia
    # cursor.execute("select city_id,offense_id,latitude,longitude,hour,minute,month,day,year from (select * from (select * from fact \
    #             inner join time \
    #             on fact.time_id = time.id) time_join \
    #         inner join date \
    #         on time_join.date_id = date.id) date_join \
    #         inner join location \
    #         on date_join.location_id = location.id \
    #         where city_id = 5")
    # PhillyCrimes = cursor.fetchall()

    # Build data from location and time info
    data = []
    for incident in allCrimes:
        # event = [latitude, longitude, time in minutes from midnight]
        event = [incident[2], incident[3], 60*incident[4]/100 + incident[5], incident[1]]
        data.append(event)

    # Transform data to numpy array
    data = np.array(data)

    # Shuffle data
    np.random.shuffle(data)

    # Split the data into training and test sets
    to_test = (2 * data.shape[0]) // 10 # Set aside 20% of data for testing
    data_train = data[:-to_test]
    data_test = data[-to_test:]

    # Transpose temporarily...
    # ---TO DO--- Be less silly?
    data_train = np.transpose(data_train)
    data_test = np.transpose(data_test)

    # Separate features vs. labels
    X_train = data_train[0:-1]
    label_train = data_train[-1:]
    X_test = data_test[0:-1]
    label_test = data_test[-1:]

    # Transpose back...
    # ---TO DO--- Be less silly?
    X_train = np.transpose(X_train)
    label_train = np.transpose(label_train)
    
    # Convert labels to 1d numpy array
    label_train = np.ravel(label_train)

    # Perform feature scaling
    X_train = scale(X_train)
    X_test = scale(X_test)

    # Initialize classifier
    # Specify that should inversely balance weights assign to classes and should faster solver
    clf = LogisticRegression(class_weight='balanced',solver='sag',max_iter=1000);

    # Train classifier
    clf.fit(X_train,label_train)

    # Print training mean accuracy
    acc_train = clf.score(X_train,label_train)
    print 'mean accuracy on training data...', acc_train # DEBUG    






    




if __name__ == '__main__':
    main()
