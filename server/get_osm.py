#!/usr/bin/env python


"""
This program was designed to request local XML data from the OSM API.  We planned
on using this dynamically so that when the user selected where they were we would 
parse the intersection data, store it in a database for later use, and then continue
processing the user's request.  However, we soon realized that this is infeasible 
due to the data request limitation of the OSM API.  We then resorted to downloading
the XML offline and pre-processing.
"""


import osmapi


def getOSM(api,min_lon, min_lat, max_lon = None, max_lat = None):
    """
    Download data in bounding box.
    Returns list of dict
    {
        type: node|way|relation,
        data: {}
    }.
    """
    lat1 = min_lat
    lat2 = max_lat
    lng1 = min_lon
    lng2 = max_lon
    if (max_lon == None or max_lat == None):
    	lat1 = min_lon[0]
    	lat2 = min_lat[0]
    	lng1 = min_lon[1]
    	lng2 = min_lat[1]

    uri = (
        "/api/0.6/map?bbox=%f,%f,%f,%f"
        % (lng1, lat1, lng2, lat2)
    )
    data = api._get(uri)
    return data

    # def _get(self, path):
    #     return self._http('GET', path, False, None)


def main():
	api = osmapi.OsmApi()
	
#http://api.openstreetmap.org/api/0.6/map?bbox=15.55,-4.24,15.56,-4.23
	# k = getOSM(api,15.55,-4.24,15.56,-4.23)
	# v =getOSM(api,(-4.24,15.55),(-4.23,15.56))
	# if (k == v):
	# 	print True
	# else:
	# 	print False, len(k),len(v)
	# print v
	


if __name__=="__main__":
	main()