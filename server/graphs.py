

"""
This file contains the classes used to create our simple Graph implementations.
"""

import scipy


"""
class Node simply stores a unique reference id and a tuple of coordinates.
"""
class Node:

	reference = ""
	coordinates = ""

	def __init__(self,reference,coordinates):
		self.reference = reference
		self.coordinates = coordinates

"""
class Edge simply contains the references to both nodes as well
as their locations. In addition it contains the euclidean length of the edge.
Each edge has a crimeWeight field that is updated later according to crimes in the 
vicinity.
"""
class Edge:
	
	# reference = ""
	node1 = None
	node2 = None
	coord1 = None
	coord2 = None
	crimeWeight = 0
	length = 0

	def __init__(self,node1,coord1,node2,coord2,length):
		self.node1 = node1
		self.node2 = node2
		self.coord1 = coord1
		self.coord2 = coord2
		# self.reference = reference
		self.length = length


"""
class Graph simply contains a set of nodes and a set of edges between those
nodes.
"""

class Graph:

	nodes = set()
	edges = set()

	def __init__(self,nodes,edges):
		self.nodes = nodes
		self.edges = edges

