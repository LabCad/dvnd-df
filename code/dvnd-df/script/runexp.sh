#!/bin/bash
if [ $# -gt 3 ]; then
	hostname

	num_proc=$1
	num_workes=$2
	host_num=$3
	host_file="host_"$host_num
	solver_name=$4
	file_list=()
	problem=

	if [ $# -lt 5 ]; then
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
	else
		file_numbers="inicio $5 fim"
		# Códigos das instâncias
		for i in {0..21}
		do
			if [[ $file_numbers = *" $i "* ]]; then
				file_list+=($i)
			fi
		done
	fi
	
	if [ $# -gt 5 ]; then
		problem=$5
	else
		problem="ml"
	fi

	for filei in "${file_list[@]}"
	do
		for i in {0..99}
		do
			file_name=$solver_name"_n"$num_proc"w"$num_workes"in"$filei"_"$i
			echo $file_name
			if [ "$solver_name" = "rvnd_no_df" ]; then
				# echo rvnd_no_df
				time python mainvnd.py -in $filei > "results/"$file_name".out" 2> "results/"$file_name".log"
			elif [ "$solver_name" = "rvnd_no_mpi" ]; then
				python main.py -n $num_workes -in $filei -s $solver_name -p $problem > "results/"$file_name".out" 2> "results/"$file_name".log"
			else
				# echo $solver_name
				time mpirun -np $num_proc --hostfile $host_file python main.py -mpi -n $num_workes -in $filei -s $solver_name -p $problem > "results/"$file_name".out" 2> "results/"$file_name".log"
			fi
		done
	done
else
	echo "Use: $0 <num_proc> <num_workes> <host_num> <solver_name> [<file_list>] [<problem>]"
fi
