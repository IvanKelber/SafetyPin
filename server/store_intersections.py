#!/usr/bin/env python

import scipy
from server import *
import sys
import csv
import sqlite3
import time

def main():
    start = time.clock()
    print "Extracting intersections and streets..."
    intersections, streets = extract_intersections(sys.argv[1])
    print "break here"
    conn = sqlite3.connect("intersection.db")
    c = conn.cursor()


    if c.execute("\
        SELECT name from sqlite_master \
        WHERE type='table' \
        AND name='coords'").fetchone() is None:
        c.execute("CREATE TABLE nodes \
            (ref INT PRIMARY KEY, latitude REAL, longitude REAL)")
        c.execute("CREATE TABLE edges \
            (ref1 INT, ref2 INT, lat1 REAL, long1 REAL, lat2 REAL, long2 REAL,length REAL, PRIMARY KEY(ref1,ref2))")

    print "Storing intersections as nodes..."
    for intersection,coordinates in intersections.items():
        coord = eval(coordinates)
        try:
            c.execute("INSERT into nodes\
                VALUES(?,?,?)", (intersection,coord[0],coord[1]))

        except sqlite3.IntegrityError:
            print "Not unique:",intersection,coordinates
            continue
    print "Splitting streets and storing edges..."
    # edges = set()
    beverley = streets["Beverley Road"]
    for i in beverley:
        print i[1]
    for street,bag in streets.items():
        print("=======================STREET",street,"=====================")
        print("=======================BAG",bag,"=====================")
        for item in bag:
            print item[1]
    return
    # for street,bag in streets.items():
    #     for item in bag:
    #         print item[1]
    # return

    for street,bag in streets.items():
        print("=======================STREET",street,"=====================")
        print("=======================BAG",bag,"=====================")
        for i in range(len(bag) - 1):
            try:



                coord1 = eval(bag[i][1])
                coord2 = eval(bag[i+1][1])
                distance = scipy.spatial.distance.euclidean(coord1,coord2) ** (0.5)
                # print ""distance
                if distance > 0.03210958510321036: #average distance between two nodes * 2
                    continue
                # print("POINTS:",coord1,coord2)                             

                c.execute("INSERT into edges\
                    VALUES(?,?,?,?,?,?,?)",(bag[i][0],bag[i+1][0],coord1[0],coord1[1],coord2[0],coord2[1],distance))
                # prompt = str(coord1[0]) + "," + str(coord1[1]) +"\n"+ str(coord2[0]) + ","+ str(coord2[1])
                # print prompt

            except KeyError:
                continue
            except sqlite3.IntegrityError:
                continue

    conn.commit()
    end = time.clock()
    print end - start, "seconds have elapsed."


    # x = c.fetchone()
    # print(x)


if __name__=="__main__":
    if len(sys.argv) == 2:
        main()
    else:
        print ("Expected 1 argument, received %d arguments", len(sys.argv) - 1)