#!/bin/bash -l

h=2
for i in {1..10}
do
    n=10000
	echo $h threads/block
	for j in {1..9}
	do
		echo $n items
		./a3 $n $h >> outfile
		n=$((n*2))
	done
	h=$((h*2))
done