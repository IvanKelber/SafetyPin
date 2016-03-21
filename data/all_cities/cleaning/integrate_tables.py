#!/usr/bin/env python
import sys
import csv
import re
import operator
from apiclient.discovery import build


first = 'merged4'
second = 'bo'
out = 'all'


def main():
	

	#open fact tables

	with open('../facts/' + first + '_fact_table.csv', "rb") as city1_fact, \
	open('../facts/' + second + '_fact_table.csv', "rb") as city2_fact, \
	open('../facts/' + out + '_fact_table.csv','a+') as output_fact:

		#determine which tables we update
		#TODO this part ^^
		#open determined tables
		date_dict = {}
		time_dict = {}
		offense_dict = {}
		location_dict = {}

		#old id values mapped to new id values
		date_old_new_id = {}
		time_old_new_id = {}
		offense_old_new_id = {}
		location_old_new_id = {}

		date_id = -1
		time_id = -1
		offense_id = -1
		location_id = -1

		###CLEANING DATE
		with open('../date/' + first + '_date_table.csv', "rb") as city1_date, \
		open('../date/' + second + '_date_table.csv', "rb") as city2_date, \
		open('../date/' + out + '_date_table.csv', 'wb') as output_date:

	  		city1_reader = csv.reader(city1_date)

			#skip header
			next(city1_reader,None)
			count = 0
			for row in city1_date:
				r = row.split(',')
				r[-1] = r[-1].strip()
				date_dict[str(r[1:])] = count
				count += 1

	  		city2_reader = csv.reader(city2_date)

			output_date_writer = csv.writer(output_date)

			output_date_writer.writerow(next(city2_reader,None))
			for row in city2_date:
				r = row.split(',')
				r[-1] = r[-1].strip()
				try:
					date_old_new_id[r[0]] = date_dict[str(r[1:])]
				except KeyError:
					date_dict[str(r[1:])] = count
					date_old_new_id[r[0]] = count
					count += 1


			for key,value in sorted(date_dict.items(), key=operator.itemgetter(1)):
				k = eval(key)
				output_date_writer.writerow([value] + k)		




		###CLEANING TIME
		with open('../time/' + first + '_time_table.csv', "rb") as city1_time, \
		open('../time/' + second + '_time_table.csv', "rb") as city2_time, \
		open('../time/' + out + '_time_table.csv', 'wb') as output_time:
	  		city1_reader = csv.reader(city1_time)

			
			next(city1_reader,None)
			count = 0
			for row in city1_time:
				r = row.split(',')
				r[-1] = r[-1].strip()
				time_dict[str(r[1:])] = count
				count += 1

	  		city2_reader = csv.reader(city2_time)
			output_time_writer = csv.writer(output_time)

			output_time_writer.writerow(next(city2_reader,None))
			for row in city2_time:
				r = row.split(',')
				r[-1] = r[-1].strip()
				try:
					time_old_new_id[r[0]] = time_dict[str(r[1:])]
				except KeyError:
					time_dict[str(r[1:])] = count
					time_old_new_id[r[0]] = count
					count += 1


			for key,value in sorted(time_dict.items(), key=operator.itemgetter(1)):
				k = eval(key)
				output_time_writer.writerow([value] + k)		




		###CLEANING OFFENSE
		with open('../offense/' + first + '_offense_table.csv', "rb") as city1_offense, \
		open('../offense/' + second + '_offense_table.csv', "rb") as city2_offense, \
		open('../offense/' + out + '_offense_table.csv', 'wb') as output_offense:
	  		city1_reader = csv.reader(city1_offense)

			
			next(city1_reader,None)
			count = 0
			for row in city1_offense:
				r = row.split(',')
				r[-1] = r[-1].strip()
				offense_dict[str(r[1:])] = count
				count += 1

	  		city2_reader = csv.reader(city2_offense)
			output_offense_writer = csv.writer(output_offense)

			output_offense_writer.writerow(next(city2_reader,None))
			for row in city2_offense:
				r = row.split(',')
				r[-1] = r[-1].strip()
				try:
					offense_old_new_id[r[0]] = offense_dict[str(r[1:])]
				except KeyError:
					offense_dict[str(r[1:])] = count
					offense_old_new_id[r[0]] = count
					count += 1


			for key,value in sorted(offense_dict.items(), key=operator.itemgetter(1)):
				k = eval(key)
				output_offense_writer.writerow([value] + k)




		###CLEANING LOCATION
		with open('../location/' + first + '_location_table.csv', "rb") as city1_location, \
		open('../location/' + second + '_location_table.csv', "rb") as city2_location, \
		open('../location/' + out + '_location_table.csv', 'wb') as output_location:
	  		city1_reader = csv.reader(city1_location)

			
			next(city1_reader,None)
			count = 0
			for row in city1_location:
				r = row.split(',')
				r[-1] = r[-1].strip()
				location_dict[str(r[1:])] = count
				count += 1

	  		city2_reader = csv.reader(city2_location)
			output_location_writer = csv.writer(output_location)

			output_location_writer.writerow(next(city2_reader,None))
			for row in city2_location:
				r = row.split(',')
				r[-1] = r[-1].strip()
				try:
					location_old_new_id[r[0]] = location_dict[str(r[1:])]
				except KeyError:
					location_dict[str(r[1:])] = count
					location_old_new_id[r[0]] = count
					count += 1


			for key,value in sorted(location_dict.items(), key=operator.itemgetter(1)):
				k = eval(key)
				output_location_writer.writerow([value] + k)		

		city1_fact_reader = csv.reader(city1_fact)
		output_fact_writer = csv.writer(output_fact)

		size = -1
		for row in city1_fact_reader:
			size += 1
			output_fact_writer.writerow(row)

		city2_fact_reader = csv.reader(city2_fact)
		next(city2_fact_reader,None)



		### WRITING TO FACT TABLE
		for row in city2_fact_reader:
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
			output_fact_writer.writerow([size+1,row[1],time_id,date_id,offense_id,location_id])
			size += 1



	# with open('../date/city1_date_table.csv', 'rb') as city1, \
	#  open('../date/city2_date_table.csv','rb') as city2, \
	#  open('../date/date_table.csv',"wb") as date_output:
	#  city1_reader = csv.reader(city1)
	#  city2_reader = csv.reader(city2)
	#  fieldnames = ['Date_ID','Day of Week','Month','Day','Year']
	#  date_writer = csv.DictWriter(date_output,fieldnames)

	#  next(city1_reader,None)
	#  next(city2_reader,None)

	#  find_writer.writeheader()
	#   = {}
	#  for row in city1_reader:
	#  	if row not in output:
	#  		output[row] = row.split(',')[0]	



			

	

if __name__ == '__main__':
	main()