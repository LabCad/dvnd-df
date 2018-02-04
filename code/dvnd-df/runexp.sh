#!/bin/bash
for filei in {0..7}
do
	for i in {0..99}
	do
	   echo "in_"$filei"_"$i
	   time mpirun -np 4 --hostfile host_gpu python main.py -mpi -n 4 -in $filei > results/"in_"$filei"_"$i.out 2> results/"in_"$filei"_"$i.log
	done
done

