#!/usr/bin/env python

import scipy
from Graphs import *
import operator
from scipy import spatial

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
    #print("Parsing osm file into tree...",datetime.now().time())
    tree = ET.parse(osm)
    #print(datetime.now().time())
    root = tree.getroot()
    counter = {}
    typesOfHighways = {}
    acceptedTypesOfHighway = ['residential','primary','secondary']
    totalChildren = str(len(root))
    streets = {}

    curChild = 0
    for child in root:
        curChild += 1
        #print(str(curChild) + "/" + totalChildren,datetime.now().time())
        if child.tag == 'way':
            name = ""
            childIsHighway = False
            for item in child:
                if item.tag == 'tag':
                    if item.attrib['k'] == 'name':
                        name = item.attrib['v']
                    if item.attrib['k'] == 'highway':
                        if item.attrib['v'] in acceptedTypesOfHighway:    
                            childIsHighway = True
            if childIsHighway:
                try:
                    streets[name]
                except KeyError:
                    streets[name] = set()
                for item in child:
                    if item.tag == 'nd':
                        nd_ref = item.attrib['ref']
                        if not nd_ref in counter:
                            counter[nd_ref] = 0
                        counter[nd_ref] += 1
                        streets[name].add(nd_ref)

    # # Find nodes that are shared with more than one way, which
    # # might correspond to intersections
    #intersections = filter(lambda x: counter[x] > 1,  counter)

    ## This is a map that contains all of the intersections within the boundaries.
    intersections = {}
    for ref in counter.keys():
        if counter[ref] > 1:
            intersections[ref] = counter[ref]

    # Extract intersection coordinates
    # You can plot the result using this url.
    # http://www.darrinward.com/lat-long/
    # This map contains the coordinates of every reference in the original osm file
    intersection_coordinates = {}
    for child in root:
        if child.tag == 'node':
            try:
                inIntersections = counter[child.attrib['id']]
                coordinate = child.attrib['lat'] + ',' + child.attrib['lon']
                intersection_coordinates[child.attrib['id']]=coordinate
                #print(coordinate)
            except:
                continue

    # For every street, order the intersections so that each is connected.
    for street,bag in streets.items():
        streets[street] = findOrder(bag,intersection_coordinates)


    nodes = set()
    for ref in intersections:
        nodes.add(Node(ref,intersection_coordinates[ref]))

    edges = set()
    for street,bag in streets.items():
        for i in range(len(bag) - 1):
            try:
                intersections[bag[i]]
                intersections[bag[i+1]]
                edges.add(Edge(bag[i],bag[i+1]))
            except KeyError:
                continue

    print(len(nodes),len(edges))
    graph = Graph(nodes,edges)

    return intersection_coordinates

# N^2 booooo
def findEndPoints(bag,coordinates):
    biggest = 0
    biggestEndpoints = []
    for int1 in bag:
        for int2 in bag:
            if int1 != int2:
                coord1success = False  
                try:                 
                    coord1 = eval(coordinates[int1])
                    coord1success = True
                    coord2 = eval(coordinates[int2])
                    distance = scipy.spatial.distance.euclidean(coord1,coord2)
                    biggest = max(distance,biggest)
                    if biggest == distance:
                        biggestEndpoints = [int1,int2]
                except KeyError:
                    if biggest == 0:
                        biggestEndpoints = [int1,int2]
                    continue        
    return biggestEndpoints
      
def findOrder(bag,coordinates):
    endPoints = findEndPoints(bag,coordinates)
    try:
        endCoordinate = eval(coordinates[endPoints[0]])
    except KeyError:
        endCoordinate = eval(coordinates[endPoints[1]])
    orderedDict = {}
    finalOrder = []
    for intersection in bag:
        try:
            coord = eval(coordinates[intersection])        
            distance = scipy.spatial.distance.euclidean(coord,endCoordinate)
            orderedDict[intersection] = distance
        except KeyError:
            continue
    for intersection,distance in sorted(orderedDict.items(),key=operator.itemgetter(1),reverse=False):
        finalOrder.append(intersection)

    return finalOrder


def main():
    extract_intersections('./OSM_data/test_streets4.osm')


main()