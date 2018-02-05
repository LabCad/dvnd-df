#!/bin/bash
for filei in 3 4
do
	for i in {0..99}
	do
	   echo "vnd_in"$filei"_"$i
	   time python mainvnd.py -in $filei > results/"vnd_in"$filei"_"$i.out 2> results/"vnd_in"$filei"_"$i.log
	done
done

