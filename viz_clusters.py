import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import math

N=428

def viz_clusters(clusterDir):
	
	names=[]
	adjmatrix=[]

	clusters=os.listdir(clusterDir)
	for d_name in clusters:
		names.append(d_name)
		d=os.path.join(clusterDir,d_name)

		files=os.listdir(d)
		fileNum=len(files)
		m=np.zeros(N,N)		
		for file_name in files:
			filepath=os.path.join(d,file_name)
			with open(filepath) as f:
				for line in f:
					t=line.split('\t')
					r=int(t[0])-1
					c=int(t[1])-1
					m[r,c]+=1.0/fileNum
		adjmatrix.append(adjmatrix)


	# visualization section
	figN=math.ceil(math.sqrt(len(names)))
	fig, axes = plt.subplots(figN, figN, figsize=(12, 6),
                         subplot_kw={'xticks': [], 'yticks': []})
	fig.subplots_adjust(hspace=0.3, wspace=0.05)

	for i in range(names):
		ax=axes[i/figN,i%figN]
		title=names[i]
		m=adjmatrix[i]
		ax.pcolor(m)
		ax.set_title(title)

	plt.show()