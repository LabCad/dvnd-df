#!/bin/bash
if [ $# -gt 0 ]; then
	hostname

	num_proc=$1
	num_workes=$2
	host_num=$3
	host_file="host_"$host_num
	solver_name=$4
	file_list=

	if [ "$host_num" = '1' ]; then
		file_list=(0 7)
	fi
	if [ "$host_num" = "2" ]; then
		file_list=(1 6)
	fi
	if [ "$host_num" = "3" ]; then
		file_list=(2 5)
	fi
	if [ "$host_num" = "4" ]; then
		file_list=(3 4)
	fi
	if [ "$host_num" = "1_2" ]; then
		file_list=(0 3 4 7)
	fi
	if [ "$host_num" = "3_4" ]; then
		file_list=(1 2 5 6)
	fi
	if [ "$host_num" = "1_4" ]; then
		file_list=(0..7)
	fi

	for filei in "${file_list[@]}"
	do
		for i in {0..99}
		do
			file_name=$solver_name"_np"$num_proc"w"$num_workes"in"$filei"_"$i
			echo $file_name
			if [ "$solver_name" = "vnd_no_df" ]; then
				time python mainvnd.py -in $filei > "results/"$file_name".out" 2> "results/"$file_name".log"
			else
				time mpirun -np $num_proc --hostfile $host_file python main.py -mpi -n $num_workes -in $filei -s $solver_name > "results/"$file_name".out" 2> "results/"$file_name".log"
			fi
		done
	done
fi
