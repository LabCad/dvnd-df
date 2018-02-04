#mpirun --hostfile host_gpu optirun python main.py -mpi -n 1 -in 1
mpirun -np 1 --hostfile host_gpu optirun python main.py -mpi -n 4 -in 1

