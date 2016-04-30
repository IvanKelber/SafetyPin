#!/usr/bin/env python

import osmapi


def getOSM(api,min_lon, min_lat, max_lon, max_lat):
    """
    Download data in bounding box.
    Returns list of dict
    {
        type: node|way|relation,
        data: {}
    }.
    """
    uri = (
        "/api/0.6/map?bbox=%f,%f,%f,%f"
        % (min_lon, min_lat, max_lon, max_lat)
    )
    data = api._get(uri)
    return data

    # def _get(self, path):
    #     return self._http('GET', path, False, None)

def main():
	api = osmapi.OsmApi()
	
#http://api.openstreetmap.org/api/0.6/map?bbox=15.55,-4.24,15.56,-4.23
	print(getOSM(api,15.55,-4.24,15.56,-4.23))


if __name__=="__main__":
	main()