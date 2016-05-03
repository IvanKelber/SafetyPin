import scipy

class Node:

	reference = ""
	coordinates = ""

	def __init__(self,reference,coordinates):
		self.reference = reference
		self.coordinates = coordinates

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


class Graph:

	nodes = set()
	edges = set()

	def __init__(self,nodes,edges):
		self.nodes = nodes
		self.edges = edges

