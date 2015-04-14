import sys
import os
import networkx as nx
import matplotlib.pyplot as plt

def readGraph(file_name):
	g=nx.Graph()
	with open(file_name) as f:
		for line in f:
			t=line.split()
			g.add_edge(int(t[0]),int(t[1]))
	return g

def drawgraph(g):

	nx.draw_shell(g,with_labels=True)

if __name__=='__main__':
	
	file=sys.argv[1]
	g=readGraph(file)
	drawgraph(g)
	plt.show()