import sqlite3
import numpy as np
from sklearn.preprocessing import scale
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC

# ---TO DO---
# [] Either add features that use month, day, year or don't select in SQL queries
# [] Be less silly with regard to transposing and then transposing back
# [] Play around with balanced vs. not balanced class weights (so far, only not balanced is converging)
# [] Play around with solver for logistic regression (currently using 'sag')
# [] Um, still need to calculate accuracy on test set!
# [] Calculate precision and recall for each class
# [] Implement SVM (better or worse than logistic regression?)


def classify(crimes): # crimes should be list of tuples (city_id, offense_id, lat, long, hour, minute, ...)
    # Build data from location and time info
    data = []
    for incident in crimes:
        # event = [latitude, longitude, time in minutes from midnight]
        event = [incident[2], incident[3], 60*incident[4]/100 + incident[5], incident[1]]
        data.append(event)

    # Transform data into numpy array
    data = np.array(data)

    # Shuffle data
    np.random.shuffle(data)

    # Split the data into training (80% of data) and test sets (20% of data)
    to_test = (2 * data.shape[0]) // 10
    data_train = data[:-to_test]
    data_test = data[-to_test:]

    # Transpose temporarily...
    data_train = np.transpose(data_train)
    data_test = np.transpose(data_test)

    # Separate features vs. labels
    X_train = data_train[0:-1]
    label_train = data_train[-1:]
    X_test = data_test[0:-1]
    label_test = data_test[-1:]

    # Transpose back...
    X_train = np.transpose(X_train)
    label_train = np.transpose(label_train)
    
    # Convert labels to 1d numpy array
    label_train = np.ravel(label_train)

    # Perform feature scaling
    X_train = scale(X_train)
    X_test = scale(X_test)

    # Initialize classifier
    clf = LogisticRegression(solver='sag') # class_weight='balanced' didn't converge

    # Train classifier
    clf.fit(X_train,label_train)

    # Print training mean accuracy
    acc_train = clf.score(X_train,label_train)
    print 'mean accuracy on training data...', acc_train # DEBUG    

def main():
    # Get ready to use SQL
    conn = sqlite3.connect("../crime_new.db")
    cursor = conn.cursor()

    # Query our database to build a dictionary of offense IDs to offense names ---TO DO--- use this somewhere or remove
    crimes = {}
    cursor.execute("select * from offense")
    for crime in cursor.fetchall():
            crimes[crime[0]] = crime[1].encode('utf-8')

    # Now, what we actually care about:
    # Query our database to get location and date/time info for all crimes for a given city

    # New York
    cursor.execute("select city_id,offense_id,latitude,longitude,hour,minute,month,day,year from (select * from (select * from fact \
                inner join time \
                on fact.time_id = time.id) time_join \
            inner join date \
            on time_join.date_id = date.id) date_join \
            inner join location \
            on date_join.location_id = location.id \
            where city_id = 1")
    NYCrimes = cursor.fetchall()

    # Chicago
    cursor.execute("select city_id,offense_id,latitude,longitude,hour,minute,month,day,year from (select * from (select * from fact \
                inner join time \
                on fact.time_id = time.id) time_join \
            inner join date \
            on time_join.date_id = date.id) date_join \
            inner join location \
            on date_join.location_id = location.id \
            where city_id = 2")
    ChiCrimes = cursor.fetchall()

    # Boston
    cursor.execute("select city_id,offense_id,latitude,longitude,hour,minute,month,day,year from (select * from (select * from fact \
                inner join time \
                on fact.time_id = time.id) time_join \
            inner join date \
            on time_join.date_id = date.id) date_join \
            inner join location \
            on date_join.location_id = location.id \
            where city_id = 3")
    BosCrimes = cursor.fetchall()

    # Denver
    cursor.execute("select city_id,offense_id,latitude,longitude,hour,minute,month,day,year from (select * from (select * from fact \
                inner join time \
                on fact.time_id = time.id) time_join \
            inner join date \
            on time_join.date_id = date.id) date_join \
            inner join location \
            on date_join.location_id = location.id \
            where city_id = 4")
    DenCrimes = cursor.fetchall()

    # Philadelphia
    cursor.execute("select city_id,offense_id,latitude,longitude,hour,minute,month,day,year from (select * from (select * from fact \
                inner join time \
                on fact.time_id = time.id) time_join \
            inner join date \
            on time_join.date_id = date.id) date_join \
            inner join location \
            on date_join.location_id = location.id \
            where city_id = 5")
    PhillyCrimes = cursor.fetchall()

    # All cities together
    allCrimes = NYCrimes+ChiCrimes+BosCrimes+DenCrimes+PhillyCrimes

    # And now... CLASSIFY!
    print '----------------New York----------------'
    classify(NYCrimes)

    print '----------------Chicago----------------'
    classify(ChiCrimes)

    print '----------------Boston----------------'
    classify(BosCrimes)    

    print '----------------Denver----------------'
    classify(DenCrimes)

    print '----------------Philadelphia----------------'
    classify(PhillyCrimes)

    print '----------------All Cities----------------'
    classify(allCrimes)


if __name__ == '__main__':
    main()
