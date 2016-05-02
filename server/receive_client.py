#!/usr/bin/env python

import osmapi,socket,os
from get_osm import *
from server import *

def main():
    s = socket.socket()
    host = os.gethostname()

    api = osmapi.OsmApi()
    while True:
        try:
            port = int(input("Enter the port"))
            s.bind((host,port))
            break;
        except IOError:
            print("Port %d already in use" % port)
            continue

    s.listen(5)


    while True:
         c, addr = s.accept()
        print("Got connection from", addr)
        data = c.recv(1024)
        latLngs = eval(data.encode('utf-8'))
        xml = getOSM(api,latLngs(0),latLngs(1))
        path = (xml)


        c.send("I come in peace.".encode('utf-8'))
        c.close()





if __name__== "__main__":
	main()