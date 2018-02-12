time mpirun -np 1 --hostfile host_3_4 python main.py -mpi -n 1 -in 7 -s dvnd > "results/nocache/dvnd_n1w1i7_0.out" 2> "results/nocache/dvnd_n1w1i7_0.log"
time mpirun -np 1 --hostfile host_3_4 python main.py -mpi -n 1 -in 7 -s dvnd > "results/nocache/dvnd_n1w1i7_1.out" 2> "results/nocache/dvnd_n1w1i7_1.log"
time mpirun -np 1 --hostfile host_3_4 python main.py -mpi -n 1 -in 7 -s dvnd > "results/nocache/dvnd_n1w1i7_2.out" 2> "results/nocache/dvnd_n1w1i7_2.log"

time mpirun -np 2 --hostfile host_3_4 python main.py -mpi -n 1 -in 7 -s dvnd > "results/nocache/dvnd_n2w1i7_0.out" 2> "results/nocache/dvnd_n2w1i7_0.log"
time mpirun -np 2 --hostfile host_3_4 python main.py -mpi -n 1 -in 7 -s dvnd > "results/nocache/dvnd_n2w1i7_1.out" 2> "results/nocache/dvnd_n2w1i7_1.log"
time mpirun -np 1 --hostfile host_3_4 python main.py -mpi -n 1 -in 7 -s dvnd > "results/nocache/dvnd_n2w1i7_2.out" 2> "results/nocache/dvnd_n2w1i7_2.log"

time mpirun -np 1 --hostfile host_3_4 python main.py -mpi -n 2 -in 7 -s dvnd > "results/nocache/dvnd_n1w2i7_0.out" 2> "results/nocache/dvnd_n1w2i7_0.log"
time mpirun -np 1 --hostfile host_3_4 python main.py -mpi -n 2 -in 7 -s dvnd > "results/nocache/dvnd_n1w2i7_1.out" 2> "results/nocache/dvnd_n1w2i7_1.log"
time mpirun -np 1 --hostfile host_3_4 python main.py -mpi -n 2 -in 7 -s dvnd > "results/nocache/dvnd_n1w2i7_2.out" 2> "results/nocache/dvnd_n1w2i7_2.log"

time mpirun -np 2 --hostfile host_3_4 python main.py -mpi -n 2 -in 7 -s dvnd > "results/nocache/dvnd_n2w2i7_0.out" 2> "results/nocache/dvnd_n2w2i7_0.log"
time mpirun -np 2 --hostfile host_3_4 python main.py -mpi -n 2 -in 7 -s dvnd > "results/nocache/dvnd_n2w2i7_1.out" 2> "results/nocache/dvnd_n2w2i7_1.log"
time mpirun -np 2 --hostfile host_3_4 python main.py -mpi -n 2 -in 7 -s dvnd > "results/nocache/dvnd_n2w2i7_2.out" 2> "results/nocache/dvnd_n2w2i7_2.log"
