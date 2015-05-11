import sys
import os
import networkx as nx
import numpy as np
import spams
import shutil
import timeit

NNODE=428
NCLUSTER=50
ITER=-600

def readOneGraph(file_name):
	v=np.zeros(shape=(NNODE*NNODE,1))
	with open(file_name) as f:
		for line in f:
			t=line.split()
			row=int(t[0])-1
			col=int(t[1])-1
			v[col*NNODE+row]=1
	return v

def readFiles(inputDir):
	files=os.listdir(inputDir)
	nsamples=len(files)
	res=readOneGraph(os.path.join(inputDir,files[0]))
	for i in range(1,nsamples):
		v=readOneGraph(os.path.join(inputDir,files[i]))
		res=np.concatenate((res,v),axis=1)

	return res

def sparseCoding(X):
    X = np.asfortranarray(X)
    param = { 'K' : NCLUSTER,	# size of the dictionary 
          'lambda1' : 0.15, 
          #'posD' : True,	# dictionary positive constrain
          #'modeD' : 1,	# L1 regulization regularization on D
          'iter' : ITER} # runtime limit 15mins
    
    D = spams.trainDL_Memory(X,**param)
    # lparam = _extract_lasso_param(param)
    # print 'genrating codes...'
    # alpha = spams.lasso(X,D = D,**lparam)
    return D

def generateCode(X,D):
    X = np.asfortranarray(X)
    print X.shape
    D = np.asfortranarray(D)
    print D.shape
    param = { 'K' : NCLUSTER,	# size of the dictionary 
          'lambda1' : 0.15, 
          #'posD' : True,	# dictionary positive constrain
          #'modeD' : 1,	# L1 regulization regularization on D
          'iter' : ITER} # runtime limit 15mins

    lparam = _extract_lasso_param(param)
    print 'genrating codes...'
    alpha = spams.lasso(X,D = D,**lparam)
    return alpha


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

def getDictionary(inputDir,outputDir):

	if os.path.isdir(outputDir):
		shutil.rmtree(outputDir)
	print "creating "+outputDir
	os.makedirs(outputDir)

	files=os.listdir(inputDir)
	codeIndexFile=os.path.join(outputDir,'codeIndex.txt')
	with open(codeIndexFile,'w') as f:
		f.write(' '.join(files))

	print 'reading graphs..'
	start=timeit.default_timer()
	X=readFiles(inputDir)
	end=timeit.default_timer()
	print 'time: {0} seconds'.format(end-start)
	
		
	print 'saving raw input data...'
	adjMatrixFile=os.path.join(outputDir,'adjMatrix.txt')
	np.savetxt(adjMatrixFile,X)

	print 'doing sparse coding...'
	start=timeit.default_timer()
	D=sparseCoding(X)
	end=timeit.default_timer()
	print 'time: {0} seconds'.format(end-start)

	print 'saving dictionary...'
	dicFile=os.path.join(outputDir,'dic.txt')
	np.savetxt(dicFile,D)

def getAlpha(outputDir):
	X=np.loadtxt(os.path.join(outputDir,'adjMatrix.txt'))
	D=np.loadtxt(os.path.join(outputDir,'dic.txt'))
	alpha=generateCode(X,D)

	print 'saving codings...'
	codeFile=os.path.join(outputDir,'code.txt')
	np.savetxt(codeFile,alpha.toarray())	

if __name__=='__main__':

	inputDir=sys.argv[1]
	outputDir=sys.argv[2]

	#getDictionary(inputDir,outputDir)
	getAlpha(outputDir)

