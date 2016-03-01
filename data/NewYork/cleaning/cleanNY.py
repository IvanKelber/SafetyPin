#!/usr/bin/env python
import sys
import csv
import re
import operator
from apiclient.discovery import build

api_key = ''

def main():
	with open('../../../api_keys/google_api_key.txt', 'rb') as api:
		api_key = api.readline()

	
	with open('../NewYorkMajorCrime.csv', 'rb') as ny, \
	 open('../fact_table.csv','wb') as fact, \
	 open('../time_table.csv', 'wb') as time, \
	 open('../date_table.csv', 'wb') as date, \
	 open('../location_table.csv','wb') as location, \
	 open('../offense_table.csv','wb') as offense:
		reader = csv.reader(ny)
		fact_writer = csv.writer(fact)
		time_writer = csv.writer(time)
		date_writer = csv.writer(date)
		location_writer = csv.writer(location)
		offense_writer = csv.writer(offense)


		header = next(reader,None)
		id_index = header.index("OBJECTID")
		date_index = header.index("Occurrence Date")
		dow_index = header.index("Day of Week")
		hour_index = header.index("Occurrence Hour")
		year_index = header.index("Occurrence Year")
		month_index = header.index("Occurrence Month")
		day_index = header.index("Occurrence Day")
		offense_index = header.index("Offense")
		classification_index = header.index("Offense Classification")
		borough_index = header.index("Borough")
		location_index = header.index("Location 1")

		#Headers
		fact_writer.writerow(["ID","Time_ID","Date_ID","Offense_ID","Location_ID"])
		time_writer.writerow(["Time_ID","Hour","Minute"])
		date_writer.writerow(["Date_ID","Day of Week","Month","Day","Year"])
		offense_writer.writerow(["Offense_ID","Offense","Classification"])
		location_writer.writerow(["Location_ID","Latitude","Longitude"])

		#list of unique fields (for use in snowflake schema)
		# date_list = {}
		# dow_list = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
		# month_list = set(["January","February","March","April","May","June",\
		# "July","August","September","October","November","December"])

		# borough_list = ["Bronx","Brooklyn","Manhattan","Queens","Staten Island"]
		# x_list = []
		# y_list = []
		# lat_list = []
		# long_list = []

		time_list = {}
		date_list = {}
		offense_list = {}
		location_list = {}

		count = 0
		for row in reader:
			#need to remove occurrences before 2015 because of small sample size
			if(eval(row[year_index]) >= 2015):
				count += 1
				ID = count
				#time
				Date = row[date_index]
				Hour = row[hour_index]
				minute_pattern = re.compile(r'.*:(\d\d):\d\d.*')
				Minute = minute_pattern.search(Date).group(1)
				time_key = ','.join([Hour,Minute])
				time_id = -1
				try:
					time_id = time_list[time_key]
				except KeyError:
					time_list[time_key] = len(time_list)
					time_id = time_list[time_key]
					time_writer.writerow([time_id,Hour,Minute])

				
				#date
				Day_of_Week = row[dow_index]
				Month = row[month_index]
				Day = row[day_index]
				Year = row[year_index]
				date_key = ','.join([Day_of_Week,Month,Day,Year])
				date_id = -1
				try:
					date_id = date_list[date_key]
				except KeyError:
					date_list[date_key] = len(date_list)
					date_id = date_list[date_key]
					date_writer.writerow([date_id,Day_of_Week,Month,Day,Year])

				#offense (will be used for calculating severity)
				Offense = row[offense_index]
				Classification = row[classification_index]
				offense_key = ','.join([Offense,Classification])
				offense_id = -1
				try:
					offense_id = offense_list[offense_key]
				except KeyError:
					offense_list[offense_key] = len(offense_list)
					offense_id = offense_list[offense_key]
					offense_writer.writerow([offense_id,Offense,Classification])


				#location
				Location = eval(row[location_index])
				Latitude = Location[0]
				Longitude = Location[1]
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