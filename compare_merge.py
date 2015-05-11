import sys
import os
import subprocess
from sets import Set

COMPT=0.5

def getPatternList(inDir):

	child=subprocess.Popen(['find',inDir,'-name','*.PATTERN'],stdout=subprocess.PIPE)
	(stdoutdata, stderrdata)=child.communicate()

	return stdoutdata.split()

def readPatterns(files):
	res=[]
	for file_path in files:
		with open(file_path) as f:
			prevNodes=Set()
			for line in f:
				if len(line.strip())==0:
					continue
				t=line.split(']')
				t=t[0][1:].split(',')
				currNodes=Set()
				for node in t:
					currNodes.add(int(node))
				if len(currNodes&prevNodes)!=len(prevNodes):
					res.append(currNodes)
				prevNodes=currNodes
	return res

def readOnePattern(file_path):
	res=[]
	with open(file_path) as f:
		prevNodes=Set()
		for line in f:
			if len(line.strip())==0:
				continue
			t=line.split(']')
			t=t[0][1:].split(',')
			currNodes=Set()
			for node in t:
				currNodes.add(int(node))
			if len(currNodes&prevNodes)!=len(prevNodes):
				res.append(currNodes)
			prevNodes=currNodes
	return res


def mergePatterns(patterns):
	#res=[]
	signs=[0]*len(patterns)

	for i in range(len(patterns)):
		for j in range(i+1,len(patterns)):
			if signs[i]:
				break
			if signs[j]:
				continue
			li=len(patterns[i])
			lj=len(patterns[j])
			lo=len(patterns[i]&patterns[j])
			if float(lo)/min(li,lj)>=0.8:
				if li>lj:
					signs[j]=1
				else:
					signs[i]=1
					break
		if not signs[i]:
			#res.append(patterns[i])
			print list(patterns[i])
	#return res

def comparePatterns(p1,p2):
	recall=0
	total_ratio=0.0
	for nodes_i in p1:
		li=len(nodes_i)
		for nodes_j in p2:
			lj=len(nodes_j)
			lo=len(nodes_i&nodes_j)
			ratio=float(lo)/min(li,lj)
			if ratio>=COMPT:
				recall+=1
				total_ratio+=ratio
				print list(nodes_i), list(nodes_j), ratio
				break
	print 'total number of patterns recalled: {0}'.format(recall)
	print 'average overlap ratio: {0}'.format(total_ratio/recall)

def readOnePatternNew(file_path):
	res={}
	with open(file_path) as f:
		for line in f:
			if len(line.strip())==0:
				continue
			t=line.split(']')
			t=t[0][1:].split(',')

			for i in range(len(t)):
				for j in range(i,len(t)):
					minNode=min(int(t[i]),int(t[j]))
					maxNode=max(int(t[i]),int(t[j]))
					hashCode=str(minNode)+'_'+str(maxNode)
					if hashCode not in res:
						res[hashCode]=1
					else
						res[hashCode]+=1
	return res


def comparePatternsNew(p1,p2):

	precision=0
	recall=0

	origionPairNum=len(p1)
	targetPairNum=len(p2)

	p=0.0
	for i in p2:
		p2Count=p2[i]
		p1Count=0
		if i in p1:
			p1Count=p1[i]
		p+=float(min(p1Count,p2Count))/p2Count
	precision=p/targetPairNum

	p=0.0
	for i in p1:
		p1Count=p1[i]
		p2Count=0
		if i in p2:
			p2Count=p2[i]
		p+=float(min(p1Count,p2Count))/p1Count

	recall=p/origionPairNum


	print 'precision: {0}'.format(precision)
	print 'recall: {0}'.format(recall)

if __name__=='__main__':
	param=sys.argv[1]

	if param=='-merge':
		inDir=sys.argv[2]

		files=getPatternList(inDir)
		#print len(files),' files read'
		patterns=readPatterns(files)
		#print len(patterns),' patterns read'
		mergePatterns(patterns)
	
	if param=='-compare':
		file1=sys.argv[2]
		file2=sys.argv[3]

		p1=readOnePattern(file1)
		p2=readOnePattern(file2)
		comparePatterns(p1,p2)

	if param=='-compareNew':
		file1=sys.argv[2]
		file2=sys.argv[3]

		p1=readOnePatternNew(file1)
		p2=readOnePatternNew(file2)
		comparePatternsNew(p1,p2)
