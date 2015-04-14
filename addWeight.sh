
for p in `ls $1`
do
	cat $1/$p | awk '{print $0 "\t" 1}' > $2/$p
done 
