#!/usr/bin/env python



from server import *
import sys
import csv
import sqlite3
import time

def main():
    start = time.clock()
    print "Extracting intersections and streets..."
    intersections, streets = extract_intersections(sys.argv[1])
    conn = sqlite3.connect("intersection.db")
    c = conn.cursor()


    if c.execute("\
        SELECT name from sqlite_master \
        WHERE type='table' \
        AND name='coords'").fetchone() is None:
        c.execute("CREATE TABLE nodes \
            (ref INT PRIMARY KEY, location VARCHAR)")
        c.execute("CREATE TABLE edges \
            (ref1 INT, ref2 INT, PRIMARY KEY(ref1,ref2))")

    print "Storing intersections as nodes..."
    for intersection,coordinates in intersections.items():
        try:
            c.execute("INSERT into nodes\
                VALUES(?,?)", (intersection,coordinates))
        except sqlite3.IntegrityError:
            print "Not unique:",intersection,coordinates
            continue
    print "Splitting streets and storing edges..."
    # edges = set()
    for street,bag in streets.items():
        for i in range(len(bag) - 1):
            try:
                intersections[bag[i]]
                intersections[bag[i+1]]                             
                c.execute("INSERT into edges\
                    VALUES(?,?)",(bag[i],bag[i+1]))
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