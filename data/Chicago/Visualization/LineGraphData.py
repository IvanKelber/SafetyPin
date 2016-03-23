import csv
import datetime
import collections

def linegraphdata():
        with open("../CrimeChicago2015.csv") as data:
                parser = list(csv.reader(data))
                dates = {}
                for data in parser:
                        if data[3] not in dates:
                                dates[data[3]] = 0
                
                dates = collections.OrderedDict(sorted(dates.items()))

                for data in parser:
                        if data[3] in dates:
                                dates[data[3]] += 1
                                
        with open("linegraphdata.csv","wb") as date_crime:
                fields = ['Date','Crimes']
                writer = csv.DictWriter(date_crime,fields)
                writer.writeheader()
                for date in dates:
                        writer.writerow({'Date':date,'Crimes':dates[date]})
linegraphdata() 
