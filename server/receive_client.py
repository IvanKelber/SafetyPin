#!/usr/bin/env python

import osmapi,socket,os
from get_osm import *
from server import *

def main():
    s = socket.socket()
    host = socket.gethostbyname(socket.gethostname())

    api = osmapi.OsmApi()
    while True:
        try:
            port = int(input("Enter the port: "))
            s.bind((host,port))
            break;
        except IOError:
            print("Port %d already in use" % port)
            continue

    print("Listening on %s:%s" % (host,port))
    s.listen(5)


    while True:
        c, addr = s.accept()
        print("Got connection from", addr)
        data = c.recv(1024)

        try:
            # print("Data:",data.encode('utf-8'))
            latLngs = eval(data.encode('utf-8'))
            A = latLngs[0]
            B = latLngs[1]

        except SyntaxError:
            #input isn't successful
            print("Unexpected Syntax")
            pass
        try:
        # print("A:",A,"B:",B);
            coords = spitCoords(A,B)
            # print("outputted Coords:",coords)
            out=repr(coords).encode('utf-8')
            print "RESPONDING WITH:", out
            c.send(out)

        except UnboundLocalError:
            print("UnboundLocalError:  Perhaps someone clicked really far out.");
            c.send("[]")
            pass
            

        c.close()





if __name__== "__main__":
	main()