#!/usr/bin/env python

import scipy
from graphs import *
import operator
from scipy import spatial
import math
from datetime import datetime
import numpy
import sqlite3
import time

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
                        # print nd_ref
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
                # print(coordinatesdinate)
            except:
                continue

    # print intersection_coordinates
    # print "###########################"
    newStreets = {}

    # For every street, order the intersections so that each is connected.
    for street in streets:
        temp = list(streets[street])
        newStreets[street] = []
        for node in range(len(temp)):
            for intersection,coordinates in intersection_coordinates.items():
                if temp[node] == intersection:
                    newStreets[street].append((intersection,coordinates))
    # print newStreets
    # t = newStreets
    # print newStreets


    # print newStreets
    finalStreets = {}
    for street,bag in newStreets.items():
        # print bag == findOrder(bag,intersection_coordinates)
        finalStreets[street] = findOrder(bag,intersection_coordinates)
        # print "#############"
        # print newStreets[street]
    # print intersection_coordinates
    # print finalStreets == t

    # print newStreets
    # print t == newStreets

    # nodes = set()
    # for ref in intersections:
    #     nodes.add(Node(ref,intersection_coordinates[ref]))

    # edges = set()
    # for street,bag in streets.items():
    #     for i in range(len(bag) - 1):
    #         try:
    #             intersections[bag[i]]
    #             intersections[bag[i+1]]                             
    #             edges.add(Edge(bag[i],bag[i+1],1))#scipy.spatial.distance.euclidean(eval(intersection_coordinates[bag[i+1]]),eval(intersection_coordinates[bag[i]]))))
    #         except KeyError:
    #             continue

    # print(len(nodes),len(edges))
    
    # graph = Graph(nodes,edges)
    # nodes = list(nodes)
    # print intersection_coordinates[nodes[0].reference],intersection_coordinates[nodes[len(nodes)-1].reference]
    # print dijkstras(graph,nodes[0],nodes[len(nodes)-1])
    # print intersection_coordinates
    # print edges
    # print intersection_coordinates.keys()
    # print "*******"
    # print finalStreets
    return intersection_coordinates,finalStreets

# N^2 booooo
def findEndPoints(bag,coordinates):
    biggest = 0
    biggestEndpoints = []
    # print coordinates
    # pass
    for int1 in bag:
        for int2 in bag:
            if int1 != int2:
                coord1success = False  
                try:                 
                    coord1 = eval(coordinates[int1[0]])
                    # print coord1
                    coord1success = True
                    coord2 = eval(coordinates[int2[0]])
                    distance = scipy.spatial.distance.euclidean(coord1,coord2)
                    biggest = max(distance,biggest)
                    if biggest == distance:
                        biggestEndpoints = [int1[0],int2[0]]
                except KeyError:
                    if biggest == 0:
                        biggestEndpoints = [int1[0],int2[0]]
                    continue        
    return biggestEndpoints
      
def findOrder(bag,coordinates):
    endPoints = findEndPoints(bag,coordinates)
    try:
        endCoordinate = eval(coordinates[endPoints[0]])
    except KeyError:
        endCoordinate = eval(coordinates[endPoints[1]])
    except IndexError:
        (i,) = bag
        return [i]
    orderedDict = {}
    finalOrder = []
    for intersection in bag:
        try:
            coord = eval(coordinates[intersection[0]])        
            distance = scipy.spatial.distance.euclidean(coord,endCoordinate)
            orderedDict[intersection] = distance
        except KeyError:
            continue
    for intersection,distance in sorted(orderedDict.items(),key=operator.itemgetter(1),reverse=False):
        finalOrder.append(intersection)

    return finalOrder




# returns four lat-long pairs between two inputs 
def getArea(coord1, coord2,tradeOffVer,tradeOffHor):

    slope = calcLineSlope(coord1[0],coord1[1],coord2[0],coord2[1])
    center = getMidpoint(coord1,coord2)

    if slope != 0:
        if slope != "infinite":
            slopeP = -1/float(slope)
        else:
            slopeP = 0

        intercept = calcLineIntercept(slopeP,center[0],center[1])
        a = 1 + slopeP**2
        b = 2 * (slopeP*(intercept - center[1]) - center[0])
        c = center[0]**2 + intercept**2 + center[1]**2 - (2*intercept*center[1]) - tradeOffVer
        xcoords = numpy.roots([a,b,c])

        verCoords = [(xcoords[0],xcoords[0]*slopeP+intercept),(xcoords[1],xcoords[1]*slopeP+intercept)]
    else:
        verCoords = [(center[0],center[1] + tradeOffVer),(center[0],center[1] - tradeOffVer)]

    distance = scipy.spatial.distance.euclidean(center,coord1) + tradeOffHor

    intercept = calcLineIntercept(slope,center[0],center[1])
    a = 1 + slope**2
    b = 2 * (slope*(intercept - center[1]) - center[0])
    c = center[0]**2 + intercept**2 + center[1]**2 - (2*intercept*center[1]) - distance**2
    xcoords = numpy.roots([a,b,c])

    horCoords = [(xcoords[0],xcoords[0]*slope+intercept),(xcoords[1],xcoords[1]*slope+intercept)]

    return [horCoords,verCoords]




# get crimes in the given perimeter
def getCrimes(area):
    conn = sqlite3.connect('data/all_cities/crime.db')
    c = conn.cursor()
    # print area
    # print area[0][0],area[1][0],area[0][1],area[1][1]
    c.execute("SELECT T.LID,T.LATITUDE,T.LONGITUDE,T.OFFENSE_ID,O.TYPE FROM OFFENSE O,(SELECT L.ID LID,LATITUDE,LONGITUDE,OFFENSE_ID FROM LOCATION L,FACT F WHERE (LATITUDE BETWEEN "\
        +str(min(area[0][0],area[1][0]))+" AND "+str(max(area[0][0],area[1][0]))+" ) AND (LONGITUDE BETWEEN "+str(min(area[0][1],area[1][1]))+" AND "+str(max(area[0][1],area[1][1]))+\
        " AND L.ID = F.LOCATION_ID)) AS T WHERE T.OFFENSE_ID = O.ID")
    crimeLocs = []
    for row in c:       
        crimeLocs.append(row)
    conn.close()

    return crimeLocs




# get intersections in given perimeter
def getIntersections(area):
    conn = sqlite3.connect('server/intersection.db')
    c = conn.cursor()
    c.execute("SELECT REF1, REF2, LAT1, LONG1, LAT2, LONG2, LENGTH FROM EDGES WHERE (LAT1 BETWEEN "\
        +str(min(area[0][0],area[1][0]))+" AND "+str(max(area[0][0],area[1][0]))+" ) AND (LONG1 BETWEEN "+str(min(area[0][1],area[1][1]))+" AND "\
        +str(max(area[0][1],area[1][1]))+") AND (LAT2 BETWEEN " +str(min(area[0][0],area[1][0]))+" AND "+str(max(area[0][0],area[1][0]))+" ) AND (LONG2 BETWEEN "+str(min(area[0][1],area[1][1]))+" AND "\
        +str(max(area[0][1],area[1][1]))+")")
    intersectionLocs = []
    for row in c:       
        intersectionLocs.append(row)
    conn.close()

    return intersectionLocs




# given a line and a point check where the point is w.r.t the line
def linePoint(bounds,loc):
  slope = calcLineSlope(bounds[0][0],bounds[0][1],bounds[1][0],bounds[1][1])
  intercept = calcLineIntercept(slope,bounds[0][0],bounds[0][1])
  
  return (loc[1] - (slope*loc[0] + intercept))



# draw parallelogram given two points
def drawParallelogram(area,loc):
  # line one h[0]-v[0]
  if linePoint([area[0][0],area[1][0]],loc) > 0:
      return False
  # line two h[0]-v[1]
  elif linePoint([area[0][0],area[1][1]],loc) < 0:
      return False
  # line three v[0]-h[1]
  elif linePoint([area[1][0],area[0][1]],loc) > 0:
      return False
  # line four v[1]-h[1]
  elif linePoint([area[1][1],area[0][1]],loc) <  0:
      return False
  else:
      return True




# calculate line slope
def calcLineSlope(x1, y1, x2, y2):
    if x1 == x2:
        return "infinite"
    return (y1 - y2)/float(x1 - x2)


# calculate line intercept
def calcLineIntercept(m,x,y):
    if m != "infinite":
            return y - m*x
    return 0


# find midpoint    
def getMidpoint(A, B):
    return ((A[0]+B[0])/float(2),(A[1]+B[1])/float(2))



# dijkstra's algorithm
def dijkstras(mapGraph,start,end):
    distance = {}
    path = {}
    for node in mapGraph.nodes:
        if node.reference != start.reference:
            distance[node.reference] = float("inf")
            continue
        distance[start.reference] = 0

    visitedNodes = []
    nodeQueue = mapGraph.nodes

    while len(nodeQueue):
        safestNode = shortestPath(nodeQueue,distance)
        visitedNodes.append(safestNode[0].reference)
        nodeQueue.remove(safestNode[0])

        for edge in mapGraph.edges: 
            weight = distance[safestNode[0].reference] + edge.crimeWeight

            if safestNode[0].reference == edge.node1:
                if distance[edge.node2] > weight:
                    distance[edge.node2] = weight
                    path[edge.node2] = safestNode[0]

            elif safestNode[0].reference == edge.node2:
                if distance[edge.node1] > weight:
                    distance[edge.node1] = weight
                    path[edge.node1] = safestNode[0]

    latLngs = [end.coordinates]
    temp = end.reference

    while temp is not start.reference:
      latLngs.append(path[temp].coordinates)
      temp = path[temp].reference
    return latLngs



# dijkstra's shortest path
def shortestPath(queue,distance):
    minWeight = float("inf")
    reqNode = 0
    for node in queue:
        if minWeight >= distance[node.reference]:
            minWeight = distance[node.reference]
            reqNode = node

    return (reqNode,minWeight) 



# calculate weight for each crime
def setcrimeWeights(count):
    crimeType = {'Personal':['HOMICIDE','CRIM SEXUAL ASSAULT','HATECRIME','OFFENSE INVOLVING CHILDREN','CRIM SEX OFFENSE',\
                'WEAPONS VIOLATION','ASSAULT'],'Property':['ROBBERY','BURGLARY','THEFT','BATTERY','']}
    crimeWeights = {}
    for crime in count:
        if crime not in crimeWeights:
            crimeWeights[crime] = 1

    return crimeWeights



def spitCoords(start,end):
	### CRIMES
	# determine perimeter for crimes
	print "fetching crime perimeter"
	distanceAB = scipy.spatial.distance.euclidean(start,end)
	tradeOffHor = 0.25*distanceAB
	tradeOffVer = 0.125*distanceAB

	# obtain vertices of the parallelogram
	crimeArea = getArea(start,end,tradeOffVer,tradeOffHor)

	# check for larger dimension and get crimes
	horDistance = scipy.spatial.distance.euclidean(crimeArea[0][0],crimeArea[0][1])
	verDistance = scipy.spatial.distance.euclidean(crimeArea[1][0],crimeArea[1][1])
	if horDistance > verDistance:
		crimeLocs = getCrimes(crimeArea[0])
	else:
		crimeLocs = getCrimes(crimeArea[1])	
	print "crime area fetched"

	print "fetching intersection perimeter"
	### INTERSECTIONS
	# determine perimeter for intersections
	distanceAB = scipy.spatial.distance.euclidean(start,end)
	tradeOffHor = 0.25*distanceAB
	tradeOffVer = 0.125*distanceAB

	# obtain vertices of the parallelogram
	intersectionArea = getArea(start,end,tradeOffVer,tradeOffHor)

	# check for larger dimension and get Intersections
	horDistance = scipy.spatial.distance.euclidean(intersectionArea[0][0],intersectionArea[0][1])
	verDistance = scipy.spatial.distance.euclidean(intersectionArea[1][0],intersectionArea[1][1])
	if horDistance > verDistance:
		intersectionLocs = getIntersections(intersectionArea[0])
	else:
		intersectionLocs = getIntersections(intersectionArea[1])

	# make graphs from the db
	edges = set()
	for edge in intersectionLocs:
		edges.add(Edge(edge[0],(edge[2],edge[3]),edge[1],(edge[4],edge[5]),edge[6]))

	nodesDict = {}
	for edge in intersectionLocs:
		nodesDict[edge[0]] = (edge[2],edge[3])
		nodesDict[edge[1]] = (edge[4],edge[5])

	nodes = set()
	for node in nodesDict:
		nodes.add(Node(node,nodesDict[node]))
		if nodesDict[node] == start:
			startNode = Node(node,start)
		if nodesDict[node] == end:
			endNode = Node(node,end)
	graph = Graph(nodes,edges)
	print "graph created"
	# weight edges based on crimes
	print "starting to weight"
	weightedGraph = setedgeWeights(graph,crimeLocs)
	print "weighting complete"
	# for node in graph.nodes:
	# 	print str(node.coordinates[0])+','+str(node.coordinates[1])

	# obtain intersections on the way
	latlongs = dijkstras(graph,startNode,endNode)
	for latLng in latlongs:
		print str(latLng[0])+','+str(latLng[1])




# calculate weight for each edge
def setedgeWeights(mapGraph,crimeLocs):
	for edge in mapGraph.edges:
		intersection1 = edge.coord1
		intersection2 = edge.coord2
		distance = scipy.spatial.distance.euclidean(intersection1,intersection2)
		print distance
		# calculate region around the edge
		tradeOffVer = 0.25*distance
		tradeOffHor = 0*distance
		area = getArea(intersection1,intersection2,tradeOffVer,tradeOffHor)
		for loc in crimeLocs:
			# check for larger dimension and get crimes
			horDistance = scipy.spatial.distance.euclidean(area[0][0],area[0][1])
			verDistance = scipy.spatial.distance.euclidean(area[1][0],area[1][1])
			if horDistance > verDistance:
				reqLocs = getCrimes(area[0])
			else:
				reqLocs = getCrimes(area[1])

		edge.crimeWeight = len(reqLocs)
		print edge.crimeWeight
	return graph




def main():
    start = (40.633204,-73.951)
    end = (40.65057,-73.9548)
    spitCoords(start,end)

if __name__=="__main__":
    main()