

class Node:

	reference = ""
	coordinates = ""

	def __init__(self,reference,coordinates):
		self.reference = reference
		self.coordinates = coordinates

class Edge:
	
	node1 = None
	node2 = None

	def __init__(self,node1,node2):
		self.node1 = node1
		self.node2 = node2


class Graph:

	nodes = set()
	edges = set()

	def __init__(self,nodes,edges):
		self.nodes = nodes
		self.edges = edges

