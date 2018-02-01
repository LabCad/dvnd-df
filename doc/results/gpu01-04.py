import os
import re


folder_to_look = "./gpu01-04/"

for file_name in os.listdir(folder_to_look):
	for line in open(folder_to_look + file_name, "r"):
		if "Fim time:" in line:
			r = re.compile("[a-z ]*: ([0-9.]*)s - [a-z]*: ([0-9]*)", re.IGNORECASE)
			time_value = r.search(line)
			print "{};{};{}".format(file_name, time_value.group(1), time_value.group(2))
			break
