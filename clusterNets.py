import sys
import os
import networkx as nx
import numpy as np
import spams
import shutil
import timeit

NNODE=428
NCLUSTER=500
ITER=-7200

def readGraph(file_name):
	g=nx.Graph()
	with open(file_name) as f:
		for line in f:
			t=line.split()
			g.add_edge(int(t[0]),int(t[1]))
	return g

def getClusterCoefficient(inputDir):
	files=os.listdir(inputDir)
	nsamples=len(files)
	coff=np.zeros(shape=(NNODE,nsamples))
	for i in range(nsamples):
		G=readGraph(os.path.join(inputDir,files[i]))
		clusterings=nx.clustering(G)
		for k,v in clusterings.items():
			coff[k-1][i]=v	# store the clustering coefficient v for node k, file i
		print '---{0}---'.format(i)
	mean=np.mean(coff,axis=1)
	mean=mean.reshape((NNODE,1))
	one=np.ones((1,nsamples))
	coff=coff-np.dot(mean,one)
	return coff

def sparseCoding(X):
    X = np.asfortranarray(X)
    param = { 'K' : NCLUSTER,	# size of the dictionary 
          'lambda1' : 0.15, 
          #'posD' : True,	# dictionary positive constrain
          #'modeD' : 1,	# L1 regulization regularization on D
          'iter' : ITER} # runtime limit 15mins
    
    D = spams.trainDL_Memory(X,**param)
    lparam = _extract_lasso_param(param)
    print 'genrating codes...'
    alpha = spams.lasso(X,D = D,**lparam)
    return D, alpha


def _extract_lasso_param(f_param):
    lst = [ 'L','lambda1','lambda2','mode','pos','ols','numThreads','length_path','verbose','cholesky']
    l_param = {'return_reg_path' : False,'pos' : True, 'verbose' : True} 
    for x in lst:
        if x in f_param:
            l_param[x] = f_param[x]
    return l_param

def groupNets(alpha):
	res=[]
	nclusters,nsamples=alpha.shape
	for i in range(nclusters):
		t=[]
		for j in range(nsamples):
			if alpha[i,j]>0:
				t.append(j)		# starting from 0
		res.append(t)
	return res

def getClusters(inputDir,outputDir):
	
	if os.path.isdir(outputDir):
		shutil.rmtree(outputDir)
	print "creating "+outputDir
	os.makedirs(outputDir)

	files=os.listdir(inputDir)
	codeIndexFile=os.path.join(outputDir,'codeIndex.txt')
	with open(codeIndexFile,'w') as f:
		f.write(' '.join(files))

	print 'calculating clustering coefficients...'
	start=timeit.default_timer()
	X=getClusterCoefficient(inputDir)
	end=timeit.default_timer()
	print 'time: {0} seconds'.format(end-start)
	
		
	print 'saving clustering coefficients...'
	clusCoeffFile=os.path.join(outputDir,'clusCoeff.txt')
	np.savetxt(clusCoeffFile,X)

	print 'doing sparse coding...'
	start=timeit.default_timer()
	D,alpha=sparseCoding(X)
	end=timeit.default_timer()
	print 'time: {0} seconds'.format(end-start)

	print 'saving dictionary...'
	dicFile=os.path.join(outputDir,'dic.txt')
	np.savetxt(dicFile,D)
	print 'saving codings...'
	codeFile=os.path.join(outputDir,'code.txt')
	np.savetxt(codeFile,alpha.toarray())

	# codeFile=os.path.join(outputDir,'code.txt')
	# alpha=np.loadtxt(codeFile)
	print 'grouping networks...'
	groups=groupNets(alpha)
	clusterFile=os.path.join(outputDir,'clusters.txt')
	with open(clusterFile,'w') as f:
		for nets in groups:
			 f.write(' '.join(map(str,nets)))
			 f.write('\n')

if __name__=='__main__':

	inputDir=sys.argv[1]
	outputDir=sys.argv[2]

	getClusters(inputDir,outputDir)

