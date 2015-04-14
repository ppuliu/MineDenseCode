import sys
import os
import shutil

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
		files=os.listdir(in_dir)
		for file_name in files[:100]:
			in_file=os.path.join(t_dir,file_name)
			out_file=os.path.join(out_dir,file_name)
			shutil.copyfile(in_file,out_file)

if __name__=='__main__':
	
	inDir=sys.argv[1]
	outDir=sys.argv[2]
	sample(inDir,outDir)



