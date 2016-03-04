from datetime import datetime
import csv



# Cleaning data for Chicago Crime
def cleanCH():
	with open('../CrimeChicago.csv','rb') as crimedata:
		crimes = list(crimedata.read().splitlines())

	with open('../CrimeChicago2015.csv','wb') as crimedata:
		fieldnames = ['ObjectID','Offense','Day of week','Date','Time','Latitude','Longitude']
		new_writer = csv.DictWriter(crimedata,fieldnames)
		new_writer.writeheader()

		Category = ['THEFT','BATTERY','ASSAULT','WEAPONS VIOLATION','CRIM SEXUAL ASSAULT','OFFENSE INVOLVING CHILDREN',\
		'ROBBERY','BURGLARY','HOMICIDE','HUMAN TRAFFICKING','CRIM SEX OFFENSE','ARSON'] #Categories we care about

		crimes = crimes[1:] #Excluding the header
		index = 1
		for crime in range(len(crimes)): 
			crimes[crime] = crimes[crime].split(',')
			datime = crimes[crime][2].split()
			weekday = datetime.strptime(datime[0],"%m/%d/%Y").strftime('%A') #Compute day of week

			if (crimes[crime][19] != '' or crimes[crime][20] != '') and crimes[crime][5] in Category:
				new_writer.writerow({'ObjectID':index,'Offense':crimes[crime][5],'Day of week':weekday,'Date':datime[0],\
					'Time':datime[1][:len(datime)+2],'Latitude':crimes[crime][19],'Longitude':crimes[crime][20]}) #Write row to csv
				index += 1

	offenses = {}
	locations = {}
	dates = {}
	times = {}

	offense_id = 0
	location_id = 0
	date_id = 0
	time_id = 0

	# Creating tables based on schema
	with open('../CrimeChicago2015.csv','rb') as crimedata,\
	open('../offense_table.csv','wb') as offense,\
	open('../location_table.csv','wb') as location,\
	open('../date_table.csv','wb') as date,\
	open('../time_table.csv','wb') as time,\
	open('../fact_table.csv','wb') as fact:

		offense_fields = ["Offense_ID","Offense"]
		location_fields = ["Location_ID","Latitude","Longitude"]
		date_fields = ["Date_ID","Day of Week","Month","Day","Year"]
		time_fields = ["Time_ID","Hour","Minute"]
		fact_fields = ["ID","Time_ID","Date_ID","Offense_ID","Location_ID"]

		offense_writer = csv.DictWriter(offense,offense_fields)
		location_writer = csv.DictWriter(location,location_fields)
		date_writer = csv.DictWriter(date,date_fields)
		time_writer = csv.DictWriter(time,time_fields)
		fact_writer = csv.DictWriter(fact,fact_fields)

		offense_writer.writeheader()
		location_writer.writeheader()
		date_writer.writeheader()
		time_writer.writeheader()
		fact_writer.writeheader()

		crimes = list(crimedata.read().splitlines())
		crimes = crimes[1:]

		for crime in range(len(crimes)):
			crimes[crime] = crimes[crime].split(',')

			locationpair = crimes[crime][5]+' '+crimes[crime][6] #Latitude, Longitude pair
			dateobj = datetime.strptime(crimes[crime][3],"%m/%d/%Y") #Date object to get Day, Month, Year
			month = dateobj.strftime('%b')
			day = int(dateobj.strftime('%d'))
			year = dateobj.strftime('%Y')
			date_entry = ','.join([crimes[crime][2],month,str(day),str(year)]) #Entry as required by date_table

			timeobj = crimes[crime][4].split(':') # Time object for hours and minutes
			hour = str(int(timeobj[0])*100)
			minute = timeobj[1]
			time_entry = ','.join([hour,minute]) #Entry as required by time_table

			if crimes[crime][1] not in offenses: #List of offenses 
				offenses[crimes[crime][1]] = offense_id
				offense_writer.writerow({'Offense_ID':offense_id,'Offense':crimes[crime][1]})
				offense_id += 1

			if locationpair not in locations: #List of locations
				locations[locationpair] = location_id
				location_writer.writerow({'Location_ID':location_id,'Latitude':locationpair.split()[0],'Longitude':locationpair.split()[1]})
				location_id += 1

			if date_entry not in dates: #List of dates
				dates[date_entry] = date_id
				date_writer.writerow({'Date_ID':date_id,'Day of Week':crimes[crime][2],'Month':month,'Day':day,'Year':year})
				date_id += 1

			if time_entry not in times: #List of times
				times[time_entry] = time_id
				time_writer.writerow({'Time_ID':time_id,'Hour':hour,'Minute':minute})
				time_id += 1


			fact_offenseid = offenses[crimes[crime][1]]
			fact_locationid = locations[locationpair]
			fact_dateid = dates[date_entry]
			fact_timeid = times[time_entry]
			fact_writer.writerow({'ID':crimes[crime][0],'Time_ID':fact_timeid,'Date_ID':fact_dateid,'Offense_ID':fact_offenseid,'Location_ID':fact_locationid}) #Write into fact table








cleanCH()
