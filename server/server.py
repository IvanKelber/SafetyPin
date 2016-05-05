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
    tree = ET.parse(osm)
    root = tree.getroot()
    counter = {}
    typesOfHighways = {}
    acceptedTypesOfHighway = ['residential','primary','secondary']
    totalChildren = str(len(root))
    streets = {}

    curChild = 0
    for child in root:
        curChild += 1
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

            except:
                continue

    newStreets = {}

    # For every street, order the intersections so that each is connected.
    for street in streets:
        temp = list(streets[street])
        newStreets[street] = []
        for node in range(len(temp)):
            for intersection,coordinates in intersection_coordinates.items():
                if temp[node] == intersection:
                    newStreets[street].append((intersection,coordinates))

    finalStreets = {}
    for street,bag in newStreets.items():
        finalStreets[street] = findOrder(bag,intersection_coordinates)

    return intersection_coordinates,finalStreets



# find the two most distant intersections on a street
def findEndPoints(bag,coordinates):
    biggest = 0
    biggestEndpoints = []
    for int1 in bag:
        for int2 in bag:
            if int1 != int2:
                coord1success = False  
                try:                 
                    coord1 = eval(coordinates[int1[0]])
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
      


# find order of the intersections for a street
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
    # print "getArea" ,[horCoords,verCoords]
    # print [horCoords,verCoords]
    return [horCoords,verCoords]



# get crimes in the given perimeter
def getCrimes(area):
    conn = sqlite3.connect('../data/all_cities/crime.db')
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
    conn = sqlite3.connect('./intersection.db')
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
    count = 0
    for node in mapGraph.nodes:
        count += 1

        if node.reference != start.reference:
            distance[node.reference] = float("inf")
            continue
        distance[start.reference] = 0

    print("NUMBER OF NODES COUNTED:",count)
    visitedNodes = []
    nodeQueue = mapGraph.nodes
    print("LENGTH OF MAP:",len(mapGraph.nodes),len(mapGraph.edges))
    count = 0
    while len(nodeQueue):
        safestNode = shortestPath(nodeQueue,distance)
        visitedNodes.append(safestNode[0].reference)
        nodeQueue.remove(safestNode[0])

        for edge in mapGraph.edges: 
            weight = distance[safestNode[0].reference] + edge.crimeWeight

            if safestNode[0].reference == edge.node1:
                count += 1
                # print("BEFORE FIRST IF STATEMENT:",distance[edge.node1],weight)

                if distance[edge.node2] > weight:
                    distance[edge.node2] = weight
                    path[edge.node2] = safestNode[0]
                    # print("AFTER FIRST IF STATEMENT",edge.node1,weight)


            elif safestNode[0].reference == edge.node2:
                count += 1
                # print("BEFORE SECOND IF STATEMENT:",distance[edge.node1],weight)
                if distance[edge.node1] > weight:
                    distance[edge.node1] = weight
                    path[edge.node1] = safestNode[0]
                    # print("AFTER SECOND IF STATEMENT",edge.node1,weight)

    # print("COUNT:",count)

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



# function gives all the required intersection coordinates
def spitCoords(start,end):
    ### CRIMES
    # determine perimeter for crimes
    # print(start,end)
    distanceAB = math.sqrt(scipy.spatial.distance.euclidean(start,end))
    tradeOffHor = 0.00025*distanceAB
    tradeOffVer = 0.000125*distanceAB

    # obtain vertices of the parallelogram
    start_time = time.clock()
    crimeArea = getArea(start,end,tradeOffVer,tradeOffHor)
    print ("Calculating crime area took:",time.clock() - start_time, "seconds.")

    # check for larger dimension and get crimes
    start_time = time.clock()
    horDistance = scipy.spatial.distance.euclidean(crimeArea[0][0],crimeArea[0][1])
    verDistance = scipy.spatial.distance.euclidean(crimeArea[1][0],crimeArea[1][1])
    if horDistance > verDistance:
        crimeLocs = getCrimes(crimeArea[0])
    else:
        crimeLocs = getCrimes(crimeArea[1]) 
    print ("Getting crimes took:",time.clock() - start_time, "seconds.")


    for loc in crimeLocs:
        print str(loc[1])+','+str(loc[2])
        # break
    ### INTERSECTIONS
    # determine perimeter for intersections
    distanceAB = math.sqrt(scipy.spatial.distance.euclidean(start,end))
    tradeOffHor = 0.0025*distanceAB
    tradeOffVer = 0.0025*distanceAB

    # obtain vertices of the parallelogram
    start_time = time.clock()
    intersectionArea = getArea(start,end,tradeOffVer,tradeOffHor)
    print ("Calculating intersection area took:",time.clock() - start_time, "seconds.")

    # check for larger dimension and get Intersections
    start_time = time.clock()
    horDistance = scipy.spatial.distance.euclidean(intersectionArea[0][0],intersectionArea[0][1])
    verDistance = scipy.spatial.distance.euclidean(intersectionArea[1][0],intersectionArea[1][1])
    if horDistance > verDistance:
        intersectionLocs = getIntersections(intersectionArea[0])
    else:
        intersectionLocs = getIntersections(intersectionArea[1])
    print ("Getting intersections took:",time.clock() - start_time, "seconds.")


    # make graphs from the db
    start_time = time.clock()
    edges = set()
    for edge in intersectionLocs:
        edges.add(Edge(edge[0],(edge[2],edge[3]),edge[1],(edge[4],edge[5]),edge[6]))
    print ("Creating edges took:",time.clock() - start_time, "seconds.")

    start_time = time.clock()
    nodesDict = {}
    for edge in intersectionLocs:
        nodesDict[edge[0]] = (edge[2],edge[3])
        nodesDict[edge[1]] = (edge[4],edge[5])
    print ("Creating nodes dict took:",time.clock() - start_time, "seconds.")

    start_time= time.clock()
    nodes = set()
    startMinimum = float("inf")
    endMinimum = float("inf")
    for node in nodesDict:
        nodes.add(Node(node,nodesDict[node]))
        startDiff = scipy.spatial.distance.euclidean(nodesDict[node],start)
        endDiff = scipy.spatial.distance.euclidean(nodesDict[node],end)

        if startDiff < startMinimum:
            startMinimum = startDiff
            startNode = Node(node,start)
        elif endDiff < endMinimum:
            endMinimum = endDiff
            endNode = Node(node,end)
    print ("Creating nodes took:",time.clock() - start_time, "seconds.")

    graph = Graph(nodes,edges)

    # weight edges based on crimes
    start_time= time.clock()
    weightedGraph = setedgeWeights(graph,crimeLocs)
    print ("Weighting edges took:",time.clock() - start_time, "seconds.")


    # obtain intersections on the way
    start_time= time.clock()
    latlongs = dijkstras(graph,startNode,endNode)
    print ("Dijkstras took:",time.clock() - start_time, "seconds.")

    # for latLng in latlongs:
    #     print str(latLng[0])+','+str(latLng[1])

    start_time= time.clock()
    latlongs.reverse()
    print ("Reversing waypoints:",time.clock() - start_time, "seconds.")

    return latlongs



# calculate weight for each edge
def setedgeWeights(mapGraph,crimeLocs):
    trackCount = [0]
    for edge in mapGraph.edges:
        intersection1 = edge.coord1
        intersection2 = edge.coord2
        center = getMidpoint(intersection1,intersection2)
        distance = math.sqrt(scipy.spatial.distance.euclidean(intersection1,intersection2))

        if intersection1[0] == intersection2[0]:
            continue        
        
        count = 1
        for loc in crimeLocs:
            locDistance = math.sqrt(scipy.spatial.distance.euclidean(center,(loc[1],loc[2])))
            if locDistance <= distance:
                count += 1
        trackCount.append(count)
        edge.crimeWeight = count
    
    maxWeight = max(trackCount)
    minWeight = min(trackCount)

    NEW_MAX = 3
    NEW_MIN = 1

    for edge in mapGraph.edges:
        try:
            edge.crimeWeight = (((edge.crimeWeight - minWeight) / float(maxWeight - minWeight))
             *(NEW_MAX-NEW_MIN)) + 1
            # print(maxWeight,minWeight,edge.crimeWeight)
        except ZeroDivisionError:
            continue
    return mapGraph




def main():
    pass
# <<<<<<< HEAD
#     start = (40.647335,-73.968420)
#     end = (40.643175,-73.968584)
# =======
#     start = (40.633204,-73.951)
#     end = (40.64010457, -73.9559158)
# >>>>>>> 9ab3491d055e5af37855a19bcc6459be5f63a441
#     spitCoords(start,end)

if __name__=="__main__":
    main()