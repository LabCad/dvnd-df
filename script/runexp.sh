#!/bin/bash
if [[ $# -gt 3 ]]; then
	hostname

	num_proc=$1
	num_workers=$2
	host_num=$3
	host_file="host_${host_num}"
	solver_name=$4
	file_list=()
	problem=
	home_p="dvnd-df/"
	home_script="${home_p}dvnd_df/script/"
	home_src="${home_p}dvnd_df"
	home_doc="${home_p}doc/"

	if [[ $# -lt 5 ]]; then
		if [[ "$host_num" = '1' ]]; then
			file_list=(0 7)
		fi
		if [[ "$host_num" = "2" ]]; then
			file_list=(1 6)
		fi
		if [[ "$host_num" = "3" ]]; then
			file_list=(2 5)
		fi
		if [[ "$host_num" = "4" ]]; then
			file_list=(3 4)
		fi
		if [[ "$host_num" = "1_2" ]]; then
			file_list=(0 3 4 7)
		fi
		if [[ "$host_num" = "3_4" ]]; then
			file_list=(1 2 5 6)
		fi
		if [[ "$host_num" = "1_4" ]]; then
			file_list=(0..50)
		fi
	else
		file_numbers="inicio $5 fim"
		# Códigos das instâncias
		for i in {0..50}
		do
			if [[ ${file_numbers} = *" $i "* ]]; then
				file_list+=($i)
			fi
		done
	fi

	if [[ $# -gt 5 ]]; then
		problem=$5
	else
		problem="ml"
	fi

	echo "num_proc=${num_proc}, num_workers=${num_workers}, host_num=${host_num}, host_file=${host_file}"
	echo "solver_name=${solver_name}, file_list=${file_list} problem=${problem}"
	echo "home_p=${home_p}"
	echo "home_script=${home_script}"
	echo "home_src=${home_src}"
	echo "home_doc=${home_doc}"

	for filei in "${file_list[@]}"
	do
		for i in {0..99}
		do
			file_name="${solver_name}_n${num_proc}w${num_workers}in${filei}_${i}"
			echo "file_name=${file_name}"
			if [[ "${solver_name}" = "dvnd_sog" || "${solver_name}" = "gdvnd_sog" ]]
			then
				echo "SOG-${solver_name}"
				time mpirun.mpich -np ${num_proc} --hostfile "${home_script}${host_file}" python "${home_src}main.py" \
				    -sii ${i} -mpi -sog -n ${num_workers} -in ${filei} -dc 2 -s ${solver_name:0:4} -p ml > \
				    "${home_doc}results/${file_name}.out" 2> "${home_doc}results/${file_name}.log"
			elif [[ "${solver_name}" = "rvnd_no_mpi" ]]
			then
				echo "rvnd_no_mpi-${solver_name}"
				temp_solver_name="rvnd"
				python "${home_src}main.py" -n ${num_workers} -sii ${i} -in ${filei} -s ${temp_solver_name} \
				    -p ${problem} > "${home_doc}results/${file_name}.out" 2> "${home_doc}results/${file_name}.log"
			else
				file_out="${home_doc}results/${file_name}"
				echo "else-${solver_name} to ${file_out}"
				# python "${home_src}/main.py"
				time mpirun.mpich -np ${num_proc} --hostfile "${home_script}${host_file} python ${home_src}/main.py" \
				    -sii -2 -mpi -n ${num_workers} -in ${filei} -dc 2 -s ${solver_name} -p ml \
				    > ${file_out}".out" 2> ${file_out}".log"
			fi
		done
	done
	
	echo "num_proc=${num_proc}, num_workers=${num_workers}, host_num=${host_num}, host_file=${host_file}"
	echo "solver_name=${solver_name}, file_list=${file_list} problem=${problem}"
	echo "home_p=${home_p}"
	echo "home_script=${home_script}"
	echo "home_src=${home_src}"
	echo "home_doc=${home_doc}"
else
	echo "Use: $0 <num_proc> <num_workes> <host_num> <solver_name> [<file_list>] [<problem>]"
fi
