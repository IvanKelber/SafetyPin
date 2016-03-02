#!/usr/bin/env python

from datetime import datetime
try:
    from xml.etree import cElementTree as ET
except ImportError, e:
    from xml.etree import ElementTree as ET

def extract_intersections(osm, verbose=True):
    # This function takes an osm file as an input. It then goes through each xml 
    # element and searches for nodes that are shared by two or more ways.
    # Parameter:
    # - osm: An xml file that contains OpenStreetMap's map information
    # - verbose: If true, print some outputs to terminal.
    # 
    # Ex) extract_intersections('WashingtonDC.osm')
    #
    print("Parsing osm file into tree...",datetime.now().time())
    tree = ET.parse(osm)
    print(datetime.now().time())
    root = tree.getroot()
    counter = {}
    typesOfHighways = {}
    acceptedTypesOfHighway = ['residential','primary','secondary']
    totalChildren = str(len(root))

    curChild = 0
    for child in root:
        curChild += 1
        print(str(curChild) + "/" + totalChildren,datetime.now().time())
        if child.tag == 'way':
            childIsHighway = False
            for item in child:
                if item.tag == 'tag':
                #if item.tag == 'nd':
                    if item.attrib['k'] == 'highway':
                        if item.attrib['v'] in acceptedTypesOfHighway:    
                            childIsHighway = True
                            break
            if childIsHighway:
                for item in child:
                    if item.tag == 'nd':             
                        nd_ref = item.attrib['ref']
                        if not nd_ref in counter:
                            counter[nd_ref] = 0
                        counter[nd_ref] += 1

    # # Find nodes that are shared with more than one way, which
    # # might correspond to intersections
    #intersections = filter(lambda x: counter[x] > 1,  counter)

    print("Initializing intersection hashmap...",datetime.now().time())
    intersections = {}
    for ref in counter.keys():
        if counter[ref] > 1:
            intersections[ref] = counter[ref]

    # Extract intersection coordinates
    # You can plot the result using this url.
    # http://www.darrinward.com/lat-long/
    intersection_coordinates = []
    print("Extracting latitude and longitude from intersections...",datetime.now().time())
    for child in root:
        if child.tag == 'node':
            try:
                inIntersections = intersections[child.attrib['id']]
                coordinate = child.attrib['lat'] + ',' + child.attrib['lon']
                intersection_coordinates.append(coordinate)
                print(coordinate)
            except:
                continue


    return intersection_coordinates


api_key = ''

def main():
    extract_intersections('./OSM_data/brooklyn_new-york.osm')


main()