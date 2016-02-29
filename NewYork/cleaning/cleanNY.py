#!/usr/bin/env python
import sys
import csv
import operator

def main():
	with open('../NewYorkMajorCrime.csv', 'rb') as ny, \
	 open('../fact_table.csv','wb') as fact, \
	 open('../time_table.csv', 'wb') as time, \
	 open('../location_table.csv','wb') as location, \
	 open('../offense_table.csv','wb') as offense:
		reader = csv.reader(ny)
		fact_writer = csv.writer(fact)
		time_writer = csv.writer(time)
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
		xcoord_index = header.index("XCoordinate")
		ycoord_index = header.index("YCoordinate")
		location_index = header.index("Location 1")

		#Headers
		fact_writer.writerow(["ID","Date_ID","Offense_ID","Location_ID"])
		time_writer.writerow(["Date_ID","Date","Day of Week","Month","Day","Year","Hour"])
		offense_writer.writerow(["Offense_ID","Offense","Classification"])
		location_writer.writerow(["Location_ID","Xcoord","Ycoord","Latitude","Longitude"])

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

		date_list = {}
		offense_list = {}
		location_list = {}


		for row in reader:
			ID = row[id_index]
			#time
			Date = row[date_index]
			Day_of_Week = row[dow_index]
			Month = row[month_index]
			Day = row[day_index]
			Year = row[year_index]
			Hour = row[hour_index]
			date_key = ','.join([Date,Day_of_Week,Month,Day,Year,Hour])
			date_id = -1
			try:
				date_id = date_list[date_key]
			except KeyError:
				date_list[date_key] = len(date_list)
				date_id = date_list[date_key]
				time_writer.writerow([date_id,Date,Day_of_Week,Month,Day,Year,Hour])

			
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
			Xcoord = row[xcoord_index]
			Ycoord = row[ycoord_index]
			Location = eval(row[location_index])
			Latitude = Location[0]
			Longitude = Location[1]
			location_key = ','.join([Xcoord,Ycoord,str(Location)])
			location_id = -1
			try:
				location_id = location_list[location_key]
			except KeyError:
				location_list[location_key] = len(location_list)
				location_id = location_list[location_key]
				location_writer.writerow([location_id,Xcoord,Ycoord,Latitude,Longitude])


			#need to remove occurrences before 2015 because of small sample size
			#also need to remove Boroughs that are nil
			if(eval(Year) >= 2015): 
				fact_writer.writerow([ID,date_id,offense_id,location_id])
			

	

if __name__ == '__main__':
	main()