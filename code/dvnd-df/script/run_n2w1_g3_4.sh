#!/bin/bash
for filei in 1 3 4 6
do
	for i in {0..99}
	do
	   echo "np2w1in"$filei"_"$i
	   time mpirun -np 1 --hostfile host_3_4 python main.py -mpi -n 1 -in $filei > results/"np2w1in"$filei"_"$i.out 2> results/"np2w1in"$filei"_"$i.log
	done
done

