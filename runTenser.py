import sys
import os
import shutil

def moveFiles(dataDir,outDir):
	dic={}
	clusterFile=os.path.join(outDir,'clusters.txt')
	indexFile=os.path.join(outDir,'codeIndex.txt')
	indices=[]
	with open(indexFile) as f:
		s=f.readline()
		indices=s.split()
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
						k=int(s)-1
						file_name=indices[k]
						sourceFile=os.path.join(dataDir,file_name)
						targetFile=os.path.join(clusterDir,file_name)
						shutil.copyfile(sourceFile,targetFile)

						if file_name not in dic:
							dic[file_name]=1
						f.write(file_name.split('.')[0]+'\n')

	files=os.listdir(dataDir)			
	clusterDir=os.path.join(outDir,'clusters','0')
	os.makedirs(clusterDir)
	for file_name in files:
		if file_name not in dic:
			sourceFile=os.path.join(dataDir,file_name)
			targetFile=os.path.join(clusterDir,'clusters',file_name)
			shutil.copyfile(sourceFile,targetFile)

if __name__=='__main__':
	
	dataDir=sys.argv[1]
	outDir=sys.argv[2]

	moveFiles(dataDir,outDir)
