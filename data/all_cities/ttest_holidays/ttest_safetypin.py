'''
This code will perform a two-tailed t-test for crime rate on holiday and average crime rate per day for a city.
We choose significance level of 0.05
We claim a null hypothesis that crime rate on holiday is same as average crime rate per day
We propose an alternate hypothesis that crime rate on holiday varies from average crime rate per day
We picked some holidays where we expect a significant trend. Some of them are federal holidays, some are observances.
The t-test should help to conclude which holidays are significant.
This data can be leveraged in future to make more accurate crime predictions.
'''

from __future__ import division
import random
import argparse
import csv
import numpy as np
from scipy import stats as st

def ztest():
    ################################### BOSTON #########################################
    with open('boston.csv', 'r') as file_reader, open('boston_holiday_stats.csv','wb') as writedata:
        data = []
        reader = csv.reader(file_reader)
        for row in reader:
            data.append(row)
        length = len(data)

        fieldnames = ['holiday','p-value','conclusion']
        writer = csv.DictWriter(writedata,fieldnames)
        writer.writeheader()

        for onelist in data:
                crime_data = []
                event_day = onelist[0]
                mu0= float(onelist[1]) #crime_per_day
                crime_data = [float(x) for x in onelist[2:]]
                t,p = st.ttest_1samp(crime_data, mu0)
                if p <=0.05:
                    conclusion = "REJECT NULL HYPOTHESIS"
                else:
                    conclusion = "fail to reject null hypothesis"
                writer.writerow({'holiday':event_day,'p-value':p,'conclusion':conclusion})

    ################################### DENVER #########################################
    with open('denver.csv', 'r') as file_reader, open('denver_holiday_stats.csv','wb') as writedata:
        data = []
        reader = csv.reader(file_reader)
        for row in reader:
            data.append(row)
        length = len(data)

        fieldnames = ['holiday','p-value','conclusion']
        writer = csv.DictWriter(writedata,fieldnames)
        writer.writeheader()

        for onelist in data:
                crime_data = []
                event_day = onelist[0]
                mu0= float(onelist[1]) #crime_per_day
                crime_data = [float(x) for x in onelist[2:]]
                t,p = st.ttest_1samp(crime_data, mu0)
                if p <=0.05:
                    conclusion = "REJECT NULL HYPOTHESIS"
                else:
                    conclusion = "fail to reject null hypothesis"
                writer.writerow({'holiday':event_day,'p-value':p,'conclusion':conclusion})

    ################################### PHILADELPHIA #########################################
    with open('philadelphia.csv', 'r') as file_reader, open('philadelphia_holiday_stats.csv','wb') as writedata:
        data = []
        reader = csv.reader(file_reader)
        for row in reader:
            data.append(row)
        length = len(data)

        fieldnames = ['holiday','p-value','conclusion']
        writer = csv.DictWriter(writedata,fieldnames)
        writer.writeheader()

        for onelist in data:
                crime_data = []
                event_day = onelist[0]
                mu0= float(onelist[1]) #crime_per_day
                crime_data = [float(x) for x in onelist[2:]]
                t,p = st.ttest_1samp(crime_data, mu0)
                if p <=0.05:
                    conclusion = "REJECT NULL HYPOTHESIS"
                else:
                    conclusion = "fail to reject null hypothesis"
                writer.writerow({'holiday':event_day,'p-value':p,'conclusion':conclusion})


    ''' As of now the data available for Chicago and New York cities is for one year.
        So running a statistical t-test is meaningless.
        Code can be uncommented and used if data is avalaible for more than 2 years
    '''

    '''
    ################################### CHICAGO #########################################
    with open('chicago.csv', 'r') as file_reader, open('chicago_holiday_stats.csv','wb') as writedata:
        data = []
        reader = csv.reader(file_reader)
        for row in reader:
            data.append(row)
        length = len(data)

        fieldnames = ['holiday','p-value','conclusion']
        writer = csv.DictWriter(writedata,fieldnames)
        writer.writeheader()

        for onelist in data:
                crime_data = []
                event_day = onelist[0]
                mu0= float(onelist[1]) #crime_per_day
                crime_data = [float(x) for x in onelist[2:]]
                t,p = st.ttest_1samp(crime_data, mu0)
                if p <=0.05:
                    conclusion = "REJECT NULL HYPOTHESIS"
                else:
                    conclusion = "fail to reject null hypothesis"
                writer.writerow({'holiday':event_day,'p-value':p,'conclusion':conclusion})

    ################################### NEWYORK #########################################
    with open('newyork.csv', 'r') as file_reader, open('newyork_holiday_stats.csv','wb') as writedata:
        data = []
        reader = csv.reader(file_reader)
        for row in reader:
            data.append(row)
        length = len(data)

        fieldnames = ['holiday','p-value','conclusion']
        writer = csv.DictWriter(writedata,fieldnames)
        writer.writeheader()

        for onelist in data:
                crime_data = []
                event_day = onelist[0]
                mu0= float(onelist[1]) #crime_per_day
                crime_data = [float(x) for x in onelist[2:]]
                t,p = st.ttest_1samp(crime_data, mu0)
                if p <=0.05:
                    conclusion = "REJECT NULL HYPOTHESIS"
                else:
                    conclusion = "fail to reject null hypothesis"
                writer.writerow({'holiday':event_day,'p-value':p,'conclusion':conclusion})

    '''


if __name__ == '__main__':
	ztest()
