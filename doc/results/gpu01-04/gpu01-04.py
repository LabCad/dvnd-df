import os
import re
import fnmatch


folder_to_look = "./rvnd_np1w1/"
file_name_pattern = "*in_7*.out"

rmy = re.compile("[a-z ]*: ([\d.]*)s - [a-z]*: ([\d]*)", re.IGNORECASE)
rtxt = re.compile("[a-z ]* ([\d.]*)s", re.IGNORECASE)
rvl = re.compile(".*\s*->\s*([\d.]*)", re.IGNORECASE)
rfn = re.compile("\w*in_*\d*", re.IGNORECASE)

tempos = {}
values = {}

for file_name in fnmatch.filter(os.listdir(folder_to_look), file_name_pattern):
	last_line = None
	time_str, value_str = None, None
	for line in open(folder_to_look + file_name, "r"):
		if "Fim time:" in line:
			time_value = rmy.search(line)
			time_str = time_value.group(1)
			value_str = time_value.group(2)
		elif "finished rvnd" in line:
			time_text = rtxt.search(line)
			value_text = rvl.search(last_line)
			time_str = time_text.group(1)
			value_str = value_text.group(1)

		if time_str is not None and value_str is not None:
			print "{};{};{}".format(file_name, time_str, value_str)
			file_name_m = rfn.search(file_name).group(0)
			tempos_list = tempos.get(file_name_m, [])
			tempos_list.append(time_str)
			tempos[file_name_m] = tempos_list
			values_list = values.get(file_name_m, [])
			values_list.append(value_str)
			values[file_name_m] = values_list
			break
		last_line = line

print "# R Commands"
for name, items in tempos.iteritems():
	print "time_{}=c({})".format(name, ",".join(items))

for name, items in values.iteritems():
	print "value_{}=c({})".format(name, ",".join(items))
