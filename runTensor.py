import sys
import os
import shutil
import subprocess

def moveFiles(dataDir,outDir):
	dic={}
	clusterFile=os.path.join(outDir,'clusters.txt')

	with open(clusterFile) as f:
		i=0
		for line in f:
			i+=1
			if line.strip()=='':
				continue
			else:
				clusterDir=os.path.join(outDir,'clusters',str(i))
				os.makedirs(clusterDir)

				netidFile=os.path.join(clusterDir,'network_ids.txt')
				with open(netidFile,'w') as f:
					for s in line.split():
						file_name=s
						sourceFile=os.path.join(dataDir,file_name)
						targetFile=os.path.join(clusterDir,file_name)
						shutil.copyfile(sourceFile,targetFile)

						if file_name not in dic:
							dic[file_name]=1
						f.write(file_name.split('.')[0]+'\n')

	files=os.listdir(dataDir)			
	clusterDir=os.path.join(outDir,'clusters','0')
	os.makedirs(clusterDir)

	netidFile=os.path.join(clusterDir,'network_ids.txt')
	with open(netidFile,'w') as f:
		for file_name in files:
			if file_name not in dic:
				sourceFile=os.path.join(dataDir,file_name)
				targetFile=os.path.join(clusterDir,file_name)
				shutil.copyfile(sourceFile,targetFile)

				f.write(file_name.split('.')[0]+'\n')

def runTensor(outDir,geneN):
	'''
	run multiple tensor instances for each partition
	'''
	print '---------------------------'
	tDir=os.path.join(outDir,'tensor')
	if os.path.isdir(tDir):
		shutil.rmtree(tDir)
	print "creating "+tDir
	os.makedirs(tDir)

	child=subprocess.Popen(['ls',os.path.join(outDir,'clusters')],stdout=subprocess.PIPE)
	(stdoutdata, stderrdata)=child.communicate()

	clus_dirs=stdoutdata.split()
	start=0
	end=25
	if end<len(clus_dirs):
		print "too many clusters. Tensor will be run sequentially with 25 instances in each group"
	else:
		end=len(clus_dirs)
	while  start<len(clus_dirs):
		t_files=clus_dirs[start:end]
		print "running Tensor for clusters {0}-{1}".format(start+1,end)
		start+=25
		end+=25
		if end>len(clus_dirs):
			end=len(clus_dirs)


		print 'running tensor with command: '
		childs=[]
		for sfile in t_files:
			if os.path.exists('unweightedNetsTensor'):
				command=['./unweightedNetsTensor']
			else:
				command=['unweightedNetsTensor']
		
			command+=['--geneTotalNumber='+geneN]
			currPar=os.path.join(outDir,'clusters',sfile)
			netidFile=os.path.join(currPar,'network_ids.txt')
			command+=['--selectedDatasetsListFile='+netidFile]	
			command+=['--minGene='+'4']
			command+=['--maxGene='+'30']
			command+=['--minNet='+'100']
			command+=['--minDensity='+'0.8']
			command+=['--networksPath='+currPar]
			resDir=os.path.join(tDir,sfile)
			os.makedirs(resDir)
			command+=['--resultPath='+resDir]
			command+=['--prefixResultFilename='+sfile]
			command+=['-r']

			f=open(os.path.join(tDir,sfile+'.out'),'w+')
			print ' '.join(command)
			child=subprocess.Popen(command,stdout=f,stderr=f)
			childs.append(child)

		print 'waiting for tensor to finish...'
		isfinish=False
		while not isfinish:
			isfinish=True
			for child in childs:
				returncode=child.poll()
				if returncode is None:
					isfinish=False
					break
				elif returncode<0:
					print 'tensor run into error: '+str(-returncode)
					sys.exit(-1)
		print '...done'

if __name__=='__main__':
	
	dataDir=sys.argv[1]
	outDir=sys.argv[2]
	geneN=sys.argv[3]

	#moveFiles(dataDir,outDir)
	runTensor(outDir,geneN)
