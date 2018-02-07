#!/bin/bash
for i in {0..99}
do
	echo "dvnd_n2w1in7_34"
	time mpirun -np 2 --hostfile host_3_4 python main.py -mpi -n 1 -in 7 -s dvnd > "results/dvnd_n2w1in7_34.out" 2> "results/dvnd_n2w1in7_34.log"
done

file_list=(0 3 4 7)
for filei in "${file_list[@]}"
do
	for i in {0..99}
	do
		echo "dvnd_n2w2in"$filei"_34"
		time mpirun -np 2 --hostfile host_3_4 python main.py -mpi -n 2 -in $filei -s dvnd > "results/dvnd_n2w2in"$filei"_34.out" 2> "results/dvnd_n2w2in"$filei"_34.log"
	done

	for i in {0..99}
	do
		echo "dvnd_n2w3in"$filei"_34"
		time mpirun -np 2 --hostfile host_3_4 python main.py -mpi -n 3 -in $filei -s dvnd > "results/dvnd_n2w3in"$filei"_34.out" 2> "results/dvnd_n2w3in"$filei"_34.log"
	done

	for i in {0..99}
	do
		echo "dvnd_n2w4in"$filei"_34"
		time mpirun -np 2 --hostfile host_3_4 python main.py -mpi -n 4 -in $filei -s dvnd > "results/dvnd_n2w4in"$filei"_34.out" 2> "results/dvnd_n2w4in"$filei"_34.log"
	done
done

