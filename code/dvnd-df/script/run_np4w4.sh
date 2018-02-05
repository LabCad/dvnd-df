#!/bin/bash
for filei in {0..7}
do
	for i in {0..99}
	do
	   echo "np4w4in"$filei"_"$i
	   time mpirun -np 4 --hostfile host_1_4 python main.py -mpi -n 4 -in $filei > results/"np4w4in"$filei"_"$i.out 2> results/"np4w4in"$filei"_"$i.log
	done
done

