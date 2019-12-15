#!/usr/bin/python
# -*- coding: utf-8 -*-
if __name__ == '__main__':
    # signal.signal(signal.SIGSEGV, sig_handler)
    import os
    if os.getcwd().endswith("dvnd_df"):
        os.chdir("..")
    print("Actual working dir: {}".format(os.getcwd()))

    from src.dataflow.vnd import *
    from src.util.cmdparam import CommandParams
    from src.print_data import print_final_solution
    from src.solver import create_solver
    from src.lib_connection import create_lib_connection

    # Command line parameters
    param = CommandParams(solver="dvnd", solution_index=0, single_output_gate=True, number_of_moves=12)
    print "param: {}".format(param)

    mylib, ini_solution, neigh_op, goal = create_lib_connection(param)

    if not param.only_compile:
        print "\nValue - initial: {} - {}".format(ini_solution, ini_solution.value)
    is_use_metadata = True

    solver = create_solver(param, mylib, is_use_metadata)

    if not param.only_compile:
        print "Solver: {}, number of workers: {}".format(param.solver.upper(), param.workers)
        start_time = time.time()
        solver.run(param.workers, ini_solution, neigh_op,
                   lambda args, metadata, inisol=ini_solution:
                   print_final_solution(args, inisol, start_time, metadata, param))
