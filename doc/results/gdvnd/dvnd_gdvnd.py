import csv
import fnmatch
import itertools
import os
import re

file_name_pattern = "*.out"
rfn = re.compile("(\w*)_n(\d*)w(\d*)in(\d*)_(\d*).out", re.IGNORECASE)
titles_new = ["initial", "final", "count", "time", "imp", "inum", "n", "w", "solver", "sample", "man_time"]
with open("dvndGdvnd.csv", 'wb') as novo_csvfile:
	writer = csv.writer(novo_csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
	writer.writerow(titles_new)
	content_folders = ["./dvnd_n1w6h1_1in0_7100sol/", "./dvnd_n2w6h1_2in0_7100sol/",
		"./dvnd_n3w6h1_3in0_7100sol/", "./dvnd_n4w6h1_4in0_7100sol/", "./dvndNoDf_n1w6h1_3in0_7100sol/"]
	content_folders = ["./dvnd_n4w6h1_4in0_7100sol/", "./gdvnd_n4w6h1_4in0_7100sol/"]
	for folder_to_look in content_folders:
		for file_name in fnmatch.filter(os.listdir(folder_to_look), file_name_pattern):
			nome_separado = rfn.search(file_name)
			test_type = nome_separado.group(1)
			test_n = nome_separado.group(2)
			test_w = nome_separado.group(3)
			test_inum = nome_separado.group(4)
			test_it = nome_separado.group(5)
			for line in open(folder_to_look + file_name, "r"):
				if "data-line;" in line:
					line = line.replace("\n", "").split(";")

					# data-line;i;558778;f;137704;t;2.54564595222;c;75;fv;[137704L, 137704L, 137704L, 137704L, 137704L];
					# cv;[10, 12, 18, 18, 17];imp;4.05781967118;age;75;type;dvnd;inum;0;w;1

					# data-line;i;558778;f;140654;t;4.76258206367;c;68;fv;[140654L, 140654L, 140654L, 140654L, 140654L];
					# cv;[18, 15, 13, 10, 12];imp;3.9727131827;age;68;mergecount;10;combine_count;[3, 4, 4, 3, 3];
					# combine_count_sum;17
					initial_value = line[2]
					final_value = line[4]
					time_value = line[6]
					count_value = line[8]
					final_list_value = line[10]
					count_list_value = line[12]
					type_value = None
					inum_value = None
					workers_value = None
					man_time = "NA"
					if len(line) > 14:
						imp_value = line[14]
						if len(line) > 16:
							age_value = line[16]
							if len(line) > 18 and "type" == line[17]:
								type_value = line[18]
								inum_value = line[20]
								workers_value = line[22]
							if len(line) > 22 and "man_time" == line[21]:
								man_time = line[22]
					else:
						imp_value = str(1.0 * int(initial_value) / int(final_value))
						age_value = "NA"

					type_value = type_value if type_value is not None else test_type
					inum_value = inum_value if inum_value is not None else test_inum
					workers_value = workers_value if workers_value is not None else test_w

					linha_atual = [initial_value, final_value, count_value, time_value, imp_value,
						inum_value, test_n, workers_value, type_value, test_it, man_time]
					writer.writerow(linha_atual)

					break
				elif "initial_solution" in line:
					# rvnd antigo
					line = re.split(";|=", line.replace("\n", ""))
					# initial_solution=786300;final_solution=171191;improveup=4.59311529228;time;1.30008196831
					initial_value = line[1]
					final_value = line[3]
					imp_value = line[5]
					time_value = line[7]

					# ["initial", "final", "count", "time", "imp", "inum", "n", "w", "solver", "sample"]
					writer.writerow([initial_value, final_value, "NA", time_value, imp_value, test_inum, test_n,
						test_w, "rvnd_no_df", test_it])

					break