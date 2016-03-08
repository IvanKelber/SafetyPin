#!/usr/bin/env python
import sys
import csv
import re
import operator
from apiclient.discovery import build



def main():
	

	#open fact tables

	with open('../facts/ny_fact_table.csv', "rb") as ny_fact, \
	open('../facts/chi_fact_table.csv', "rb") as chi_fact, \
	open('../facts/ny_chi_fact_table.csv','a+') as ny_chi_fact:

		#determine which tables we update
		#TODO this part ^^
		#open determined tables
		date_dict = {}
		time_dict = {}
		offense_dict = {}
		location_dict = {}



		date_old_new_id = {}
		time_old_new_id = {}
		offense_old_new_id = {}
		location_old_new_id = {}

		date_id = -1
		time_id = -1
		offense_id = -1
		location_id = -1

		###CLEANING DATE
		with open('../date/ny_date_table.csv', "rb") as ny_date, \
		open('../date/chi_date_table.csv', "rb") as chi_date, \
		open('../date/ny_chi_date_table.csv', 'wb') as ny_chi_date:

	  		ny_reader = csv.reader(ny_date)

			
			next(ny_reader,None)
			count = 0
			for row in ny_date:
				r = row.split(',')
				r[-1] = r[-1].strip()
				date_dict[str(r[1:])] = count
				count += 1

	  		chi_reader = csv.reader(chi_date)

			ny_chi_date_writer = csv.writer(ny_chi_date)

			ny_chi_date_writer.writerow(next(chi_reader,None))
			for row in chi_date:
				r = row.split(',')
				r[-1] = r[-1].strip()
				try:
					date_old_new_id[r[0]] = date_dict[str(r[1:])]
				except KeyError:
					date_dict[str(r[1:])] = count
					date_old_new_id[r[0]] = count
					count += 1


			for key in date_dict:
				k = eval(key)
				ny_chi_date_writer.writerow([date_dict[key]] + k)		

			ny_fact_reader = csv.reader(ny_fact)
			ny_chi_fact_writer = csv.writer(ny_chi_fact)



		###CLEANING TIME
		with open('../time/ny_time_table.csv', "rb") as ny_time, \
		open('../time/chi_time_table.csv', "rb") as chi_time, \
		open('../time/ny_chi_time_table.csv', 'wb') as ny_chi_time:
	  		ny_reader = csv.reader(ny_time)

			
			next(ny_reader,None)
			count = 0
			for row in ny_time:
				r = row.split(',')
				r[-1] = r[-1].strip()
				time_dict[str(r[1:])] = count
				count += 1

	  		chi_reader = csv.reader(chi_time)
			ny_chi_time_writer = csv.writer(ny_chi_time)

			ny_chi_time_writer.writerow(next(chi_reader,None))
			for row in chi_time:
				r = row.split(',')
				r[-1] = r[-1].strip()
				try:
					time_old_new_id[r[0]] = time_dict[str(r[1:])]
				except KeyError:
					time_dict[str(r[1:])] = count
					time_old_new_id[r[0]] = count
					count += 1


			for key in time_dict:
				k = eval(key)
				ny_chi_time_writer.writerow([time_dict[key]] + k)		

			ny_fact_reader = csv.reader(ny_fact)
			ny_chi_fact_writer = csv.writer(ny_chi_fact)



		###CLEANING OFFENSE
		with open('../offense/ny_offense_table.csv', "rb") as ny_offense, \
		open('../offense/chi_offense_table.csv', "rb") as chi_offense, \
		open('../offense/ny_chi_offense_table.csv', 'wb') as ny_chi_offense:
	  		ny_reader = csv.reader(ny_offense)

			
			next(ny_reader,None)
			count = 0
			for row in ny_offense:
				r = row.split(',')
				r[-1] = r[-1].strip()
				offense_dict[str(r[1:])] = count
				count += 1

	  		chi_reader = csv.reader(chi_offense)
			ny_chi_offense_writer = csv.writer(ny_chi_offense)

			ny_chi_offense_writer.writerow(next(chi_reader,None))
			for row in chi_offense:
				r = row.split(',')
				r[-1] = r[-1].strip()
				try:
					offense_old_new_id[r[0]] = offense_dict[str(r[1:])]
				except KeyError:
					offense_dict[str(r[1:])] = count
					offense_old_new_id[r[0]] = count
					count += 1


			for key in offense_dict:
				k = eval(key)
				ny_chi_offense_writer.writerow([offense_dict[key]] + k)		

			ny_fact_reader = csv.reader(ny_fact)
			ny_chi_fact_writer = csv.writer(ny_chi_fact)


		###CLEANING LOCATION
		with open('../location/ny_location_table.csv', "rb") as ny_location, \
		open('../location/chi_location_table.csv', "rb") as chi_location, \
		open('../location/ny_chi_location_table.csv', 'wb') as ny_chi_location:
	  		ny_reader = csv.reader(ny_location)

			
			next(ny_reader,None)
			count = 0
			for row in ny_location:
				r = row.split(',')
				r[-1] = r[-1].strip()
				location_dict[str(r[1:])] = count
				count += 1

	  		chi_reader = csv.reader(chi_location)
			ny_chi_location_writer = csv.writer(ny_chi_location)

			ny_chi_location_writer.writerow(next(chi_reader,None))
			for row in chi_location:
				r = row.split(',')
				r[-1] = r[-1].strip()
				try:
					location_old_new_id[r[0]] = location_dict[str(r[1:])]
				except KeyError:
					location_dict[str(r[1:])] = count
					location_old_new_id[r[0]] = count
					count += 1


			for key in location_dict:
				k = eval(key)
				ny_chi_location_writer.writerow([location_dict[key]] + k)		

			ny_fact_reader = csv.reader(ny_fact)
			ny_chi_fact_writer = csv.writer(ny_chi_fact)

		size = -1
		for row in ny_fact_reader:
			size += 1
			ny_chi_fact_writer.writerow(row)

		chi_fact_reader = csv.reader(chi_fact)
		next(chi_fact_reader,None)



		### WRITING TO FACT TABLE
		for row in chi_fact_reader:
			date_id = row[3]
			try:
				date_id = date_old_new_id[row[3]]
			except KeyError:
				pass
			time_id = row[2]
			try:
				time_id = time_old_new_id[row[2]]
			except KeyError:
				pass
			offense_id = row[4]
			try:
				offense_id = offense_old_new_id[row[4]]
			except KeyError:
				pass
			location_id = row[5]
			try:
				location_id = location_old_new_id[row[5]]
			except KeyError:
				pass
			ny_chi_fact_writer.writerow([size+1,row[1],time_id,date_id,offense_id,location_id])
			size += 1



	# with open('../date/ny_date_table.csv', 'rb') as ny, \
	#  open('../date/chi_date_table.csv','rb') as chi, \
	#  open('../date/date_table.csv',"wb") as date_output:
	#  ny_reader = csv.reader(ny)
	#  chi_reader = csv.reader(chi)
	#  fieldnames = ['Date_ID','Day of Week','Month','Day','Year']
	#  date_writer = csv.DictWriter(date_output,fieldnames)

	#  next(ny_reader,None)
	#  next(chi_reader,None)

	#  find_writer.writeheader()
	#   = {}
	#  for row in ny_reader:
	#  	if row not in output:
	#  		output[row] = row.split(',')[0]	



			

	

if __name__ == '__main__':
	main()