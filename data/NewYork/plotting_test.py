#!/usr/bin/env python
import sys
import csv
import re
import operator
import requests
import json
import googlemaps
import datetime
import responses
import urllib
from apiclient.discovery import build

api_key = ''

def main():
    with open('../../api_keys/google_api_key.txt', 'rb') as api:
        api_key = api.readline()
    #reverseGeocode((0,0))
    gmaps = googlemaps.Client(api_key)
    geocoding(gmaps)


@responses.activate
def geocoding(gmaps):
    # geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
    # print(geocode_result)
    with open('./location_table.csv', 'rb') as f, open('./geocode_results.csv', 'wb') as w:
        reader = csv.reader(f)
        writer = csv.writer(w)
        next(reader,None)
        count = 0
        for row in reader:
            lat = eval(row[1])
            lng = eval(row[2])

            responses.add(responses.GET,
                          'https://maps.googleapis.com/maps/api/geocode/json',
                          body='{"status":"OK","results":[]}',
                          status=200,
                          content_type='application/json')
            results = gmaps.reverse_geocode((lat,lng))
            stuff = json.loads(urllib.urlopen(responses.calls[count].request.url).read())
            results = stuff['results']
            writer.writerow([row[0],results[0]['formatted_address'].encode('utf-8')])
            count += 1

main()