#!/usr/bin/env python
import sys
import csv
import re
import operator

def main():    
    with open('PPD_Crime_Incidents_2012-2014.csv', 'rb') as philly, \
     open('fact_table.csv','wb') as fact, \
     open('time_table.csv', 'wb') as time, \
     open('date_table.csv', 'wb') as date, \
     open('location_table.csv','wb') as location, \
     open('offense_table.csv','wb') as offense:
        reader = csv.reader(philly)
        fact_writer = csv.writer(fact)
        time_writer = csv.writer(time)
        date_writer = csv.writer(date)
        location_writer = csv.writer(location)
        offense_writer = csv.writer(offense)

        header = next(reader,None)
        #id_index = header.index("OBJECTID") # Philly CSV doesn't include
        date_index = header.index("Dispatch Date/Time")
        #dow_index = header.index("Day of Week")  # Philly CSV doesn't include
        #hour_index = header.index("Occurrence Hour")  # Philly CSV doesn't include
        #year_index = header.index("Occurrence Year")  # Philly CSV doesn't include
        #month_index = header.index("Occurrence Month")  # Philly CSV doesn't include
        #day_index = header.index("Occurrence Day")  # Philly CSV doesn't include
        offense_index = header.index("General Crime Category")
        #classification_index = header.index("Classification" # Philly CSV doesn't include
        #borough_index = header.index("Borough") # Philly CSV doesn't include
        location_index = header.index("Coordinates")

        #Headers
        fact_writer.writerow(["ID","Time_ID","Date_ID","Offense_ID","Location_ID"])
        time_writer.writerow(["Time_ID","Hour","Minute"])
        date_writer.writerow(["Date_ID","Day of Week","Month","Day","Year"])
        offense_writer.writerow(["Offense_ID","Offense","Classification"])
        location_writer.writerow(["Location_ID","Latitude","Longitude"])

        time_list = {}
        date_list = {}
        offense_list = {}
        location_list = {}

        count = 0
        for row in reader:
            count += 1
            ID = count

            #time
            datetime = row[date_index].split()
            time = datetime[1].split(':')
            flag = datetime[2]
            datetime = ' '.join(datetime)

            if flag == 'AM':
                Hour = str(int(time[0])*100)
            elif flag == 'PM':
                Hour = str((int(time[0])+12)*100)
            Minute = time[1]
            time_key = ','.join([Hour,Minute])
            time_id = -1
            try:
                time_id = time_list[time_key]
            except KeyError:
                time_list[time_key] = len(time_list)
                time_id = time_list[time_key]
                time_writer.writerow([time_id,Hour,Minute])

            #date
            #Day_of_Week = row[dow_index]
            Day_of_Week = -99 # DEBUG
            date_pattern = re.compile(r'([0-9]*)\/([0-9]*)\/([0-9]*)')
            Month = date_pattern.search(datetime).group(1)
            Day = date_pattern.search(datetime).group(2)
            Year = date_pattern.search(datetime).group(3)
            date_key = ','.join([str(Day_of_Week),str(Month),str(Day),str(Year)])
            date_id = -1
            try:
                date_id = date_list[date_key]
            except KeyError:
                date_list[date_key] = len(date_list)
                date_id = date_list[date_key]
                date_writer.writerow([date_id,Day_of_Week,Month,Day,Year])

            #offense (will be used for calculating severity)
            Offense = row[offense_index]
            #Classification = row[classification_index]
            Classification = -99 # DEBUG
            offense_key = ','.join([Offense,str(Classification)])
            offense_id = -1
            try:
                offense_id = offense_list[offense_key]
            except KeyError:
                offense_list[offense_key] = len(offense_list)
                offense_id = offense_list[offense_key]
                offense_writer.writerow([offense_id,Offense,Classification])

            #location
            Location = row[location_index]
            if Location != '': # Exclude records without location info # THIS IS NOT THE RIGHT PLACE FOR THIS
                coords_pattern = re.compile(r'\(([-0-9\.]*)\, ([-0-9\.]*)\)')
                Latitude = coords_pattern.search(Location).group(1)
                Longitude = coords_pattern.search(Location).group(2)
                location_key = ','.join([str(Location)])
                location_id = -1
                try:
                    location_id = location_list[location_key]
                except KeyError:
                    location_list[location_key] = len(location_list)
                    location_id = location_list[location_key]
                    location_writer.writerow([location_id,Latitude,Longitude])

            fact_writer.writerow([ID,time_id,date_id,offense_id,location_id])


    

if __name__ == '__main__':
    main()