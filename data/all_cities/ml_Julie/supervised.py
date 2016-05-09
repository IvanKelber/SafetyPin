# Supervised learning algorithms (logistic regression and SVM) to predict TYPE OF CRIME from LATITUDE, LONGITUDE, and TIME

import sqlite3

import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import scale
from sklearn.metrics import classification_report, confusion_matrix
from sklearn import cross_validation
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC

# ---POTENTIAL IMPROVEMENTS---
# [] Play around with balanced vs. not balanced class weights: So far, only not balanced is converging, but balanced makes more sense for our dataset
# [] Play around with solver for logistic regression: Currently using 'sag' because sklearn documentation said it was faster for large datasets
# [] Calculate precision and recall for each class: Skipping for now because can tell that mostly just predicting THEFT
# [] Idea of how to integrate with our app: Allow someone to input a specific time and location and receive predicted probabilties for each crime type

def classify(crimes,classifier): # crimes should be list of tuples (city_id, offense_id, lat, long, hour, minute) and clf should be 'logistic regression' or 'svm'
    # Get ready to use SQL
    conn = sqlite3.connect("../crime_new.db")
    cursor = conn.cursor()

    # Query our database to build a dictionary of offense IDs to offense names
    allcrimetypes = {}
    cursor.execute("select * from offense")
    for crime in cursor.fetchall():
            allcrimetypes[crime[0]] = crime[1].encode('utf-8')

    # Build data from location and time info
    data = []
    citycrimes = []
    for incident in crimes:
        # event = [latitude, longitude, time in minutes from midnight, type of crime]
        event = [incident[2], incident[3], 60*incident[4]/100 + incident[5], incident[1]]
        data.append(event)

        if incident[1] not in citycrimes: # We are building a list of crime types used in this city
            citycrimes.append(incident[1])

    # Restrict our dictionary of offense types to only those used for this city
    crimetypes = {}
    for offense in allcrimetypes:
        if offense in citycrimes:
            crimetypes[offense] = allcrimetypes[offense]

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
        clf = LogisticRegression(solver='sag')
    elif classifier.lower() == 'svm':
        clf = LinearSVC()
    else:
        print "please enter either 'logistic regression' or 'svm' as the classifier type"

    # Train classifier
    clf.fit(X_train,label_train)

    # Perform 10-fold cross-validation
    acc_folds = cross_validation.cross_val_score(clf,X_train,label_train,scoring='accuracy',cv=10)

    # Print mean training accuracy
    acc_trn = np.mean(acc_folds)
    print 'accuracy on training data...',acc_trn

    # Print mean testing accuracy
    acc_test = clf.score(X_test,label_test)
    print 'accuracy on testing data...', acc_test

    # Print predicted labels for training set
    label_pred = clf.predict(X_test)
    print label_pred
    for lbl in set(label_pred):
        print crimetypes[lbl], ':', list(label_pred).count(lbl), 'predicted incidents'

    # Lines XXX through XXX are borrowed from the sci-kit learn documentation:
    # http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html
    def plot_confusion_matrix(cm, title='Confusion matrix', cmap=plt.cm.Blues):
        plt.imshow(cm, interpolation='nearest', cmap=cmap)
        plt.title(title)
        plt.colorbar()
        tick_marks = np.arange(len(crimetypes))
        plt.xticks(tick_marks, crimetypes.values(), rotation=90)
        plt.yticks(tick_marks, crimetypes.values())
        plt.tight_layout()
        plt.ylabel('True label')
        plt.xlabel('Predicted label')

    # Compute confusion matrix
    cm = confusion_matrix(label_test, label_pred)
    np.set_printoptions(precision=2)
    print('Confusion matrix, without normalization')
    print(cm)
    plt.figure()
    plot_confusion_matrix(cm)

    # Normalize the confusion matrix by row (i.e by the number of samples in each class)
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    print('Normalized confusion matrix')
    print(cm_normalized)
    plt.figure()
    plot_confusion_matrix(cm_normalized, title='Normalized confusion matrix')

    plt.show()

def main():
    # Get ready to use SQL
    conn = sqlite3.connect("../crime_new.db")
    cursor = conn.cursor()

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

    # And now... CLASSIFY
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
