#!/usr/bin/env python
import sys
import csv
import re
import operator
import sqlite3



def main():
	conn = sqlite3.connect("../crime.db")
	cursor = conn.cursor();

	crimes = {}
	cursor.execute("select * from offense")
	for crime in cursor.fetchall():
		crimes[crime[0]] = crime[1].encode('utf-8')

	cities = {}
	cursor.execute("select * from city")
	for city in cursor.fetchall():
		cities[city[0]] = city[1].encode('utf-8')

	heatmap_data = {}
	for crime in crimes:
		for city in cities:
			sql_command = "select count(*) from fact \
				where offense_id = " + str(crime) + \
				" and city_id = " + str(city) + \
				" group by offense_id;"
			cursor.execute(sql_command)
			result = cursor.fetchone()
			try:
				heatmap_data[(cities[city], crimes[crime])] = result[0]
			except TypeError:
				heatmap_data[(cities[city], crimes[crime])] = 0


	with open('heat_data.csv','wb') as heat:
		writer = csv.writer(heat);
		writer.writerow(["City","Offense","Count"])

		for k,v in sorted(heatmap_data.items(), key=lambda x: (x[0][0], x[0][1])):
			writer.writerow([k[0],k[1],v])

	


if __name__ == '__main__':
	main()