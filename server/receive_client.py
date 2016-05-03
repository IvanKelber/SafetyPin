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
            port = int(input("Enter the port"))
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
        latLngs = data.encode('utf-8')

        print(latLngs)

        c.send("40,-73".encode('utf-8'))
        c.close()





if __name__== "__main__":
	main()