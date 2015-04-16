import sys
import os
import shutil
import random

def sample(inDir,outDir):

	if os.path.isdir(outDir):
		shutil.rmtree(outDir)
	print "creating "+outDir
	os.makedirs(outDir)

	dirs=os.listdir(inDir)
	for d in dirs:
		in_dir=os.path.join(inDir,d)
		out_dir=os.path.join(outDir,d)
		os.makedirs(out_dir)
		netidFile=os.path.join(out_dir,'network_ids.txt')
		with open(netidFile,'w') as f:
			files=os.listdir(in_dir)
			for file_name in files[:100]:
				in_file=os.path.join(in_dir,file_name)
				out_file=os.path.join(out_dir,file_name)
				shutil.copyfile(in_file,out_file)
				f.write(file_name.split('.')[0]+'\n')

def random_sample(inDir,outDir,clusterN,sampleN):

	files=os.listdir(inDir)

	if os.path.isdir(outDir):
		shutil.rmtree(outDir)
	print "creating "+outDir
	os.makedirs(outDir)

	for i in range(clusterN):
		out_dir=os.path.join(outDir,str(i))
		os.makedirs(out_dir)
		netidFile=os.path.join(out_dir,'network_ids.txt')
		with open(netidFile,'w') as f:
			dic={}
			for k in range(sampleN):
				file_n=random.randint(0,len(files)-1)
				while file_n in dic:
					file_n=random.randint(0,len(files)-1)
				dic[file_n]=1
				file_name=files[file_n]
				
				in_file=os.path.join(inDir,file_name)
				out_file=os.path.join(out_dir,file_name)
				shutil.copyfile(in_file,out_file)
				f.write(file_name.split('.')[0]+'\n')


if __name__=='__main__':
	
	inDir=sys.argv[1]
	outDir=sys.argv[2]
	#sample(inDir,outDir)
	random_sample(inDir,outDir,500,100)


