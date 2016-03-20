import csv
import math

# TO DO: Account for daylight savings times
# TO DO: Change to allow input of date and time

def main():

    with open('sun.csv','rb') as sun:
        sun = csv.reader(sun)

        months = ['Jan','Feb','Mar','Apr','May','Jun','Jul', \
        'Aug','Sep','Oct','Nov','Dec']

        columns_rise = {'Jan':1,'Feb':3,'Mar':5,'Apr':7,'May':9,'Jun':11,'Jul':13, \
        'Aug':15,'Sep':17,'Oct':19,'Nov':21,'Dec':23}

        columns_set = {'Jan':2,'Feb':4,'Mar':6,'Apr':8,'May':10,'Jun':12,'Jul':14, \
        'Aug':16,'Sep':18,'Oct':20,'Nov':22,'Dec':24}

        sunrise = {'Jan':{}, 'Feb':{},'Mar':{},'Apr':{},'May':{},'Jun':{},'Jul':{}, \
        'Aug':{},'Sep':{},'Oct':{},'Nov':{},'Dec':{}}

        sunset = {'Jan':{}, 'Feb':{},'Mar':{},'Apr':{},'May':{},'Jun':{},'Jul':{}, \
        'Aug':{},'Sep':{},'Oct':{},'Nov':{},'Dec':{}}

        for row in sun:
            day = row[0]

            for m in months:
                if row[columns_rise[m]] != '':
                    sunrise[m][day] = row[columns_rise[m]]
                    sunset[m][day] = row[columns_set[m]]

if __name__ == '__main__':
    main()