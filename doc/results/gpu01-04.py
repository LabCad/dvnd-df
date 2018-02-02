import os
import re
import fnmatch


folder_to_look = "./gpu01-04/"
file_name_pattern = "vnd_*.out"

for file_name in fnmatch.filter(os.listdir(folder_to_look), file_name_pattern):
	last_line = None
	for line in open(folder_to_look + file_name, "r"):
		if "Fim time:" in line:
			r = re.compile("[a-z ]*: ([0-9.]*)s - [a-z]*: ([0-9]*)", re.IGNORECASE)
			time_value = r.search(line)
			print "{};{};{}".format(file_name, time_value.group(1), time_value.group(2))
			break
		elif "finished rvnd" in line:
			r = re.compile("[a-z ]* ([0-9.]*)s", re.IGNORECASE)
			time_text = r.search(line)

			rl = re.compile(".*\s*->\s*([0-9.]*)", re.IGNORECASE)
			value_text = rl.search(last_line)
			print "{};{};{}".format(file_name, time_text.group(1), value_text.group(1))
			break
		last_line = line
