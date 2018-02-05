#!/bin/bash
for filei in 0 7
do
	for i in {0..49}
	do
	   echo "np1w2in"$filei"_"$i
	   time mpirun -np 1 --hostfile host_1 python main.py -mpi -n 2 -in $filei > results/"np1w2in"$filei"_"$i.out 2> results/"np1w2in"$filei"_"$i.log
	done
done

