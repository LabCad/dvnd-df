#!/bin/bash
for filei in 2 5
do
	for i in {0..99}
	do
	   echo "rvnd_np1w1in"$filei"_"$i
	   time mpirun -np 1 --hostfile host_3 python main.py -mpi -n 1 -in $filei -s rvnd > results/"rvnd_np1w1in"$filei"_"$i.out 2> results/"rvnd_np1w1in"$filei"_"$i.log
	done
done

