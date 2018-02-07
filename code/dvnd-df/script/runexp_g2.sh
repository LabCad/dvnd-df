#!/bin/bash
for i in {0..99}
do
	echo "rvnd_n1w2in7_2"
	time mpirun -np 1 --hostfile host_2 python main.py -mpi -n 2 -in 7 -s rvnd > "results/rvnd_n1w2in7_2.out" 2> "results/rvnd_n1w2in7_2.log"
done
for i in {0..99}
do
	echo "rvnd_n1w3in7_2"
	time mpirun -np 1 --hostfile host_2 python main.py -mpi -n 3 -in 7 -s rvnd > "results/rvnd_n1w3in7_2.out" 2> "results/rvnd_n1w3in7_2.log"
done
