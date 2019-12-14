# -*- coding: utf-8 -*-
import sys
import random


file_list = []
problem_name = sys.argv[sys.argv.index("-p") + 1] if "-p" in sys.argv else "ml"
number_of_files = int(sys.argv[sys.argv.index("-n") + 1] if "-n" in sys.argv else "1")
file_folder = "/home/rodolfo/git/dvnd-df/doc"
if "tt" == problem_name.lower():
	from ..wrapper.ttp import ttp_solution_instance_file
	file_list = ttp_solution_instance_file
else:
	from ..wrapper.wamca2016 import wamca_solution_instance_file
	file_list = wamca_solution_instance_file

	for it in file_list:
		sol = [str(x) for x in xrange(it[1])]
		for i in xrange(number_of_files):
			random.shuffle(sol)
			with open("{}/sol/{}_{}.in".format(file_folder, it[0][:-4], i), "w") as filesol:
				filesol.write("[{}]".format(",".join(sol)))
