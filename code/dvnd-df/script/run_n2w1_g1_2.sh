#!/bin/bash
for filei in 0 2 5 7
do
	for i in {0..99}
	do
	   echo "np2w1in"$filei"_"$i
	   time mpirun -np 1 --hostfile host_1_2 python main.py -mpi -n 1 -in $filei > results/"np2w1in"$filei"_"$i.out 2> results/"np2w1in"$filei"_"$i.log
	done
done

