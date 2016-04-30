

class Node:

	reference = ""
	coordinates = ""

	def __init__(self,reference,coordinates):
		self.reference = reference
		self.coordinates = coordinates

class Edge:
	
	reference = ""
	node1 = None
	node2 = None
	crimeWeight = 0

	def __init__(self,node1,node2):
		self.node1 = node1
		self.node2 = node2
		self.reference = node1.reference + node2.reference


class Graph:

	nodes = set()
	edges = set()

	def __init__(self,nodes,edges):
		self.nodes = nodes
		self.edges = edges

