import sqlite3
import numpy as np
from sklearn.linear_model import LinearRegression

#---IGNORE THIS SCRIPT FOR NOW---

def classify(crimes,classifier): # crimes should be list of tuples (city_id, offense_id, lat, long, hour, minute) and clf should be 'logistic regression' or 'svm'
    # Get ready to use SQL
    conn = sqlite3.connect("../crime_new.db")
    cursor = conn.cursor()

    # Query our database to build a dictionary of offense IDs to offense names
    crimetypes = {}
    cursor.execute("select * from offense")
    for crime in cursor.fetchall():
            crimetypes[crime[0]] = crime[1].encode('utf-8')

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
    X_test = np.transpose(X_test)
    label_test = np.transpose(label_test)

    # Convert labels to 1d numpy array
    label_train = np.ravel(label_train)

    # Perform feature scaling
    X_train = scale(X_train)
    X_test = scale(X_test)

    # Initialize classifier
    if classifier.lower() == 'logistic regression':
        clf = LogisticRegression(solver='sag') # class_weight='balanced' didn't converge
    elif classifier.lower() == 'svm':
        clf = LinearSVC()

    # Train classifier
    clf.fit(X_train,label_train)

    # Perform 10-fold cross-validation
    acc_folds = cross_validation.cross_val_score(clf,X_train,label_train,scoring='accuracy',cv=10)

    # Print mean training accuracy
    acc_trn = np.mean(acc_folds)
    print 'accuracy on training data...',acc_trn # DEBUG

    # Print mean testing accuracy
    acc_test = clf.score(X_test,label_test)
    print 'accuracy on testing data...', acc_test # DEBUG

    # Print predicted labels for training set
    label_pred = clf.predict(X_test)
    print label_pred
    for lbl in set(label_pred):
        print crimetypes[lbl], ':', list(label_pred).count(lbl), 'predicted incidents'


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
    cursor.execute("select city_id,offense_id,latitude,longitude,hour,minute from (select * from (select * from fact \
                inner join time \
                on fact.time_id = time.id) time_join \
            inner join date \
            on time_join.date_id = date.id) date_join \
            inner join location \
            on date_join.location_id = location.id \
            where city_id = 1")
    NYCrimes = cursor.fetchall()

    # Chicago
    cursor.execute("select city_id,offense_id,latitude,longitude,hour,minute from (select * from (select * from fact \
                inner join time \
                on fact.time_id = time.id) time_join \
            inner join date \
            on time_join.date_id = date.id) date_join \
            inner join location \
            on date_join.location_id = location.id \
            where city_id = 2")
    ChiCrimes = cursor.fetchall()

    # Boston
    cursor.execute("select city_id,offense_id,latitude,longitude,hour,minute from (select * from (select * from fact \
                inner join time \
                on fact.time_id = time.id) time_join \
            inner join date \
            on time_join.date_id = date.id) date_join \
            inner join location \
            on date_join.location_id = location.id \
            where city_id = 3")
    BosCrimes = cursor.fetchall()

    # Denver
    cursor.execute("select city_id,offense_id,latitude,longitude,hour,minute from (select * from (select * from fact \
                inner join time \
                on fact.time_id = time.id) time_join \
            inner join date \
            on time_join.date_id = date.id) date_join \
            inner join location \
            on date_join.location_id = location.id \
            where city_id = 4")
    DenCrimes = cursor.fetchall()

    # Philadelphia
    cursor.execute("select city_id,offense_id,latitude,longitude,hour,minute from (select * from (select * from fact \
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

    And now... CLASSIFY
    print '================Logistic Regression================'
    print '----------------New York----------------'
    classify(NYCrimes,'logistic regression')

    print '----------------Chicago----------------'
    classify(ChiCrimes,'logistic regression')

    print '----------------Boston----------------'
    classify(BosCrimes,'logistic regression')    

    print '----------------Denver----------------'
    classify(DenCrimes,'logistic regression')

    print '----------------Philadelphia----------------'
    classify(PhillyCrimes,'logistic regression')

    print '----------------All Cities----------------'
    classify(allCrimes,'logistic regression')

    print '=======================SVM======================='
    print '----------------New York----------------'
    classify(NYCrimes,'svm')

    print '----------------Chicago----------------'
    classify(ChiCrimes,'svm')

    print '----------------Boston----------------'
    classify(BosCrimes,'svm')    

    print '----------------Denver----------------'
    classify(DenCrimes,'svm')

    print '----------------Philadelphia----------------'
    classify(PhillyCrimes,'svm')

    print '----------------All Cities----------------'
    classify(allCrimes,'svm')

if __name__ == '__main__':
    main()
