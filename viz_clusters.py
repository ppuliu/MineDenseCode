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
		print d_name 
		names.append(d_name)
		d=os.path.join(clusterDir,d_name)

		files=os.listdir(d)
		fileNum=len(files)
		m=np.zeros(shape=(N,N))
		readNetN=0		
		for file_name in files:
			if not file_name.endswith('.cnet'):
				continue
			readNetN+=1
			filepath=os.path.join(d,file_name)
			with open(filepath) as f:
				for line in f:
					if len(line.strip())==0:
						continue
					t=line.split('\t')
					r=int(t[0])-1
					c=int(t[1])-1
					m[r,c]+=1.0/fileNum
		adjmatrix.append(m)
		print str(readNetN)+' networks read'


	# visualization section
	figN=int(math.ceil(math.sqrt(len(names))))
	fig, axes = plt.subplots(figN, figN, figsize=(12, 6),
                         subplot_kw={'xticks': [], 'yticks': []})
	fig.subplots_adjust(hspace=0.3, wspace=0.05)

	for i in range(len(names)):
		ax=axes[i/figN,i%figN]
		title=names[i]
		m=adjmatrix[i]
		ax.pcolor(m)
		ax.set_title(title)

	plt.show()
	#plt.savefig('a.pdf')



if __name__=='__main__':
	clusterDir=sys.argv[1]
	viz_clusters(clusterDir)
