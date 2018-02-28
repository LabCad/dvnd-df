import os
import re
import fnmatch
import itertools

rfn = re.compile("\w*in_*(\d*)", re.IGNORECASE)
folder_to_look = "./dvnd/n1w10/"
file_name_pattern = "*.out"

names_list = []
initial_map = {}
final_map = {}
time_map = {}
count_map = {}
final_list_map = {}
count_list_map = {}


def addtomap(map, key, value):
	map_list = map.get(key, [])
	map_list.append(value)
	map[key] = map_list


for file_name in fnmatch.filter(os.listdir(folder_to_look), file_name_pattern):
	for line in open(folder_to_look + file_name, "r"):
		if "data-line;" in line:
			line = line.split(";")

			initial_value = line[2]
			final_value = line[4]
			time_value = line[6]
			count_value = line[8]
			final_list_value = line[10]
			count_list_value = line[12]

			file_name_m = "in" + rfn.search(file_name).group(1)

			if file_name_m not in names_list:
				names_list.append(file_name_m)

			addtomap(initial_map, file_name_m, initial_value)
			addtomap(final_map, file_name_m, final_value)
			addtomap(time_map, file_name_m, time_value)
			addtomap(count_map, file_name_m, count_value)
			addtomap(final_list_map, file_name_m, final_list_value)
			addtomap(count_list_map, file_name_m, count_list_value)

			break

# for name, items in time_map.iteritems():
# 	print "time_{}=c({})".format(name, ",".join(items))

lencsv = len(time_map[file_name_m])

initial_line = ";".join(["{}initial".format(x) for x in names_list])
final_line = ";".join(["{}final".format(x) for x in names_list])
time_line = ";".join(["{}time".format(x) for x in names_list])
count_line = ";".join(["{}count".format(x) for x in names_list])
# print ";".join([initial_line, final_line, time_line, count_line, final_list_line, count_list_line])
print ";".join([initial_line, final_line, time_line, count_line])

for i in xrange(lencsv):
	initial_line = ";".join(initial_map[x][i] for x in names_list)
	final_line = ";".join(final_map[x][i] for x in names_list)
	time_line = ";".join(time_map[x][i] for x in names_list)
	count_line = ";".join(count_map[x][i] for x in names_list)
	# final_list_line = ";".join(final_list_map[x][i] for x in names_list)
	# count_list_line = ";".join(count_list_map[x][i] for x in names_list)

	# print ";".join([initial_line, final_line, time_line, count_line, final_list_line, count_list_line])
	print ";".join([initial_line, final_line, time_line, count_line])
