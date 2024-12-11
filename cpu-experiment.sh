#!/bin/bash -l

h=1000
c=1
rm outfile-cpu
touch outfile-cpu

for i in {1..6}
do
	n=10000
	echo $c cores
	export OMP_NUM_THREADS=$c
	for j in {1..8}
	do
		echo $n items
		./a3 $n $h >> outfile
		n=$((n*2))
	done
	c=$((c*2))
done
python graph.py
cat outfile.csv