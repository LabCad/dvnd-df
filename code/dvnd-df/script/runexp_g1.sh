#!/bin/bash
for i in {0..99}
do
	echo "dvnd_n1w3in0_1"
	time mpirun -np 1 --hostfile host_1 python main.py -mpi -n 3 -in 0 -s dvnd > "results/dvnd_n1w3in0_1.out" 2> "results/dvnd_n1w3in0_1.log"
done
for i in {0..99}
do
	echo "dvnd_n1w3in7_1"
	time mpirun -np 1 --hostfile host_1 python main.py -mpi -n 3 -in 7 -s dvnd > "results/dvnd_n1w3in7_1.out" 2> "results/dvnd_n1w3in7_1.log"
done
