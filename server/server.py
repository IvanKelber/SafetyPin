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
                # print(coordinate)
            except:
                continue

    # For every street, order the intersections so that each is connected.
    for street,bag in streets.items():
        streets[street] = findOrder(bag,intersection_coordinates)
    # print intersection_coordinates


    nodes = set()
    for ref in intersections:
        nodes.add(Node(ref,intersection_coordinates[ref]))

    edges = set()
    for street,bag in streets.items():
        for i in range(len(bag) - 1):
            try:
                intersections[bag[i]]
                intersections[bag[i+1]]                             
                edges.add(Edge(bag[i],bag[i+1],scipy.spatial.distance.euclidean(eval(intersection_coordinates[bag[i+1]]),eval(intersection_coordinates[bag[i]]))))
            except KeyError:
                continue

    # print(len(nodes),len(edges))
    # graph = Graph(nodes,edges)
    # nodes = list(nodes)
    # print intersection_coordinates[nodes[0].reference],intersection_coordinates[nodes[len(nodes)-1].reference]
    # print dijkstras(graph,nodes[0],nodes[len(nodes)-1])

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




# returns four lat-long pairs between two input 
def getCrimeArea(coord1, coord2):
    tradeOffVer = 0.00003
    tradeOffHor = 0.003

    slope = calcLineSlope(coord1[0],coord1[1],coord2[0],coord2[1])
    center = getMidpoint(coord1,coord2)
    # print center,"CENTER"

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

    # print verCoords,"VERTICAL"
    distance = scipy.spatial.distance.euclidean(center,coord1) + tradeOffHor

    intercept = calcLineIntercept(slope,center[0],center[1])
    a = 1 + slope**2
    b = 2 * (slope*(intercept - center[1]) - center[0])
    c = center[0]**2 + intercept**2 + center[1]**2 - (2*intercept*center[1]) - distance**2
    xcoords = numpy.roots([a,b,c])

    horCoords = [(xcoords[0],xcoords[0]*slope+intercept),(xcoords[1],xcoords[1]*slope+intercept)]
    # print horCoords,"HORIZONTAL"

    # crimeLocs = getCrimes(horCoords)
    # crimeTypes = {}
    

    # for loc in crimeLocs:
    #     if str(loc[3])+" "+str(loc[4]) not in crimeTypes:
    #         crimeTypes[str(loc[3])+" "+str(loc[4])] = 1
    #         continue
    #     crimeTypes[str(loc[3])+" "+str(loc[4])] += 1

    # print crimeTypes

    # return crimeLocs
    return [horCoords,verCoords]



# get crimes in the given perimeter
def getCrimes(area):
    # print hor[1][0],hor[0][0],ver[0][1],ver[1][1]
    conn = sqlite3.connect('data/all_cities/crime.db')
    c = conn.cursor()
    # print area[0][0],area[1][0],area[0][1],area[1][1]
    c.execute("SELECT T.LID,T.LATITUDE,T.LONGITUDE,T.OFFENSE_ID,O.TYPE FROM OFFENSE O,(SELECT L.ID LID,LATITUDE,LONGITUDE,OFFENSE_ID FROM LOCATION L,FACT F WHERE (LATITUDE BETWEEN "\
        +str(min(area[0][0],area[1][0]))+" AND "+str(max(area[0][0],area[1][0]))+" ) AND (LONGITUDE BETWEEN "+str(min(area[0][1],area[1][1]))+" AND "+str(max(area[0][1],area[1][1]))+\
        " AND L.ID = F.LOCATION_ID)) AS T WHERE T.OFFENSE_ID = O.ID")
    crimeLocs = []
    for row in c:       
        crimeLocs.append(row)
    conn.close()

    return crimeLocs

# def linePoint(bounds,loc):
#   slope = calcLineSlope(bounds[0][0],bounds[0][1],bounds[1][0],bounds[1][1])
#   return (slope - (loc[1]-bounds[1][1])/(loc[0]-bounds[1][0]))

# def drawParallelogram(area,loc):
#   # line one h[0]-v[0]
#   if linePoint([area[0][0],area[1][0]],loc) < 0:
#       return False
#   # line two h[0]-v[1]
#   elif linePoint([area[0][0],area[1][1]],loc) > 0:
#       return False
#   # line three v[0]-h[1]
#   elif linePoint([area[1][0],area[0][1]],loc) < 0:
#       return False
#   # line four v[1]-h[1]
#   elif linePoint([area[1][1],area[0][1]],loc) < 0:
#       return False
#   else:
#       return True



# def drawElipse(center,a,b,loc):
#     smallAxis = scipy.spatial.distance.euclidean(center,b)
#     bigAxis = scipy.spatial.distance.euclidean(center,a)
#     acceptCrime = (((loc[0]-center[0])**2)/((bigAxis)**2) + ((loc[1]-center[1])**2)/((smallAxis)**2)) <= 1
#     return acceptCrime



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
    print "start :",start.reference,start.coordinates
    print "end ",end.reference,end.coordinates
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
            # print "visiting edge",edge.node1,"-",edge.node2,"weight ",edge.crimeWeight
            weight = distance[safestNode[0].reference] + edge.crimeWeight
            if safestNode[0].reference == edge.node1:
                # if edge.node1 not in visitedNodes:
                if distance[edge.node2] >= weight:
                    distance[edge.node2] = weight
                    path[edge.node2] = safestNode[0]
            elif safestNode[0].reference == edge.node2:
                # if edge.node2 not in visitedNodes:
                if distance[edge.node1] >= weight:
                    distance[edge.node1] = weight
                    path[edge.node1] = safestNode[0]

    # if start.reference in path:
    #     path.remove(start.reference)

    # print visitedNodes,distance,path
    latLngs = [end.coordinates]
    temp = end.reference

    print len(path)

    # print temp,"temp"
    soFar = []
    # for k,v in path.items():
    #     print k,v.reference

    while temp is not start.reference:
      # print temp,start.reference,"inside"
      print path[temp].coordinates
      time.sleep(2)
      latLngs.append(path[temp].coordinates)
      temp = path[temp].reference

    # for lat in latLngs:
    #     print lat
    return latLngs.reverse()
    # for node in path:
    #     print node,path[node].reference,path[node].coordinates
    # return path



# dijkstra's shortest path
def shortestPath(queue,distance):
    minWeight = float("inf")
    reqNode = 0
    for node in queue:
        if minWeight >= distance[node.reference]:
            minWeight = distance[node.reference]
            reqNode = node

    return (reqNode,minWeight) 



# calculate weihgt for each crime
def setcrimeWeights(count):
    crimeType = {'Personal':['HOMICIDE','CRIM SEXUAL ASSAULT','HATECRIME','OFFENSE INVOLVING CHILDREN','CRIM SEX OFFENSE',\
                'WEAPONS VIOLATION','ASSAULT'],'Property':['ROBBERY','BURGLARY','THEFT','BATTERY','']}
    crimeWeights = {}
    for crime in count:
        if crime not in crimeWeights:
            crimeWeights[crime] = 1

    return crimeWeights
    

                





def main():
    extract_intersections('../../smallTest.osm')
    # getCrimeArea((40.6521768650001,-73.961050676),(40.6330714710001,-73.94972028))
    # nodes= [Node(1,(1,1)),Node(2,(2,2)),Node(3,(3,3)),Node(4,(4,4)),Node(5,(5,5))]#,Node(6,(6,6))]
    # edges = [Edge(1,Node(1,(1,1)),Node(2,(2,2)),3),Edge(2,Node(2,(2,2)),Node(4,(4,4)),1),Edge(3,Node(4,(4,4)),Node(5,(5,5)),2),Edge(4,Node(2,(2,2)),Node(3,(3,3)),1),Edge(5,Node(1,(1,1)),Node(3,(3,3)),1),Edge(6,Node(3,(3,3)),Node(5,(5,5)),4),Edge(7,Node(3,(3,3)),Node(4,(4,4)),3)]
    # graph = Graph(nodes,edges)
    # print "1"
    # print dijkstras(graph,Node(1,(1,1)),Node(5,(5,5)))
    # print "2"

if __name__=="__main__":
    main()