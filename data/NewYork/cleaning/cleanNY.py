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

	
<<<<<<< Updated upstream
	with open('../NewYorkMajorCrime.csv', 'rb') as ny, \
	 open('fact_table2.csv','wb') as fact, \
	 open('time_table2.csv', 'wb') as time, \
	 open('date_table2.csv', 'wb') as date, \
	 open('location_table2.csv','wb') as location, \
	 open('offense_table2.csv','wb') as offense:
=======
	with open('NewYorkMajorCrime.csv', 'rb') as ny, \
	 open('fact_table.csv','wb') as fact, \
	 open('time_table.csv', 'wb') as time, \
	 open('date_table.csv', 'wb') as date, \
	 open('location_table.csv','wb') as location, \
	 open('offense_table.csv','wb') as offense, \
	 open('CrimeNY.csv','wb') as crimeNY:

>>>>>>> Stashed changes
		reader = csv.reader(ny)
		fact_writer = csv.writer(fact)
		time_writer = csv.writer(time)
		date_writer = csv.writer(date)
		location_writer = csv.writer(location)
		offense_writer = csv.writer(offense)
		crime_writer = csv.writer(crimeNY)


		header = next(reader,None)
		id_index = header.index("OBJECTID")
		date_index = header.index("Occurrence Date")
		dow_index = header.index("Day of Week")
		hour_index = header.index("Occurrence Hour")
		year_index = header.index("Occurrence Year")
		month_index = header.index("Occurrence Month")
		day_index = header.index("Occurrence Day")
		offense_index = header.index("Offense")
		borough_index = header.index("Borough")
		location_index = header.index("Location 1")

		#Headers
		fact_writer.writerow(["ID","City_ID","Time_ID","Date_ID","Offense_ID","Location_ID"])
		time_writer.writerow(["Time_ID","Hour","Minute"])
		date_writer.writerow(["Date_ID","Day of Week","Month","Day","Year"])
		offense_writer.writerow(["Offense_ID","Offense"])
		location_writer.writerow(["Location_ID","Latitude","Longitude"])
		crime_writer.writerow(["ID","Offense","Day of Week","Date","Time"])

		time_list = {}
		date_list = {}
		offense_list = {}
		location_list = {}

		count = 0
		for row in reader:
			
			# #need to remove occurrences before 2015 because of small sample size
			if(eval(row[year_index]) >= 2014):
			# 	count += 1
			# 	ID = count
			# 	#time
			 	Date = row[date_index]
			 	print Date

			# 	Hour = row[hour_index]
			# 	if(Hour[0] == '0'):
			# 		Hour = Hour[1:]
			# 	minute_pattern = re.compile(r'.*:(\d\d):\d\d.*')
			# 	Minute = minute_pattern.search(Date).group(1)
			# 	time_key = ','.join([Hour,Minute])
			# 	time_id = -1
			# 	try:
			# 		time_id = time_list[time_key]
			# 	except KeyError:
			# 		time_list[time_key] = len(time_list)
			# 		time_id = time_list[time_key]
			# 		time_writer.writerow([time_id,Hour,Minute])

				
<<<<<<< Updated upstream
			# 	#date
			# 	Day_of_Week = row[dow_index]
			# 	Month = row[month_index]
			# 	print Month
			# 	Day = row[day_index]
			# 	Year = row[year_index]
			# 	date_key = ','.join([Day_of_Week,Month,Day,Year])
			# 	date_id = -1

			# 	try:
			# 		date_id = date_list[date_key]
			# 	except KeyError:
			# 		date_list[date_key] = len(date_list)
			# 		date_id = date_list[date_key]
			# 		date_writer.writerow([date_id,Day_of_Week,Month,Day,Year])

			# 	#offense (will be used for calculating severity)
			# 	Offense = row[offense_index]
			# 	if(Offense == 'RAPE'):
			# 		Offense = 'CRIM SEXUAL ASSAULT'
			# 	elif(Offense == 'FELONY ASSAULT'):
			# 		Offense = 'ASSAULT'
			# 	elif('LARCENY' in Offense):
			# 		Offense = 'THEFT'
			# 	elif(Offense == 'MURDER'):
			# 		Offense = 'HOMICIDE'
			# 	offense_key = ','.join([Offense])
			# 	offense_id = -1
			# 	try:
			# 		offense_id = offense_list[offense_key]
			# 	except KeyError:
			# 		offense_list[offense_key] = len(offense_list)
			# 		offense_id = offense_list[offense_key]
			# 		offense_writer.writerow([offense_id,Offense])


			# 	#location
			# 	Location = eval(row[location_index])
			# 	Latitude = Location[0]
			# 	Longitude = Location[1]
			# 	location_key = ','.join([str(Location)])
			# 	location_id = -1
			# 	try:
			# 		location_id = location_list[location_key]
			# 	except KeyError:
			# 		location_list[location_key] = len(location_list)
			# 		location_id = location_list[location_key]
			# 		location_writer.writerow([location_id,Latitude,Longitude])
	 
			# 	fact_writer.writerow([ID,1,time_id,date_id,offense_id,location_id])
=======
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
				if(Offense == 'RAPE'):
					Offense = 'CRIM SEXUAL ASSAULT'
				elif(Offense == 'FELONY ASSAULT'):
					Offense = 'ASSAULT'
				elif('LARCENY' in Offense):
					Offense = 'THEFT'
				elif(Offense == 'MURDER'):
					Offense = 'HOMICIDE'
				offense_key = ','.join([Offense])
				offense_id = -1
				try:
					offense_id = offense_list[offense_key]
				except KeyError:
					offense_list[offense_key] = len(offense_list)
					offense_id = offense_list[offense_key]
					offense_writer.writerow([offense_id,Offense,])


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

				datime = row[date_index].split()
				time = datime[1]+" "+ datime[2]
				in_time = datetime.strptime(time, "%I:%M:%S %p")
				out_time = datetime.strftime(in_time, "%H:%M")
	 
				fact_writer.writerow([ID,1,time_id,date_id,offense_id,location_id])
				crime_write.writerow([ID,offence,Day_of_Week,datime[0],out_time])
>>>>>>> Stashed changes
			

	

if __name__ == '__main__':
	main()