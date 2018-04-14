import os
import csv
import fnmatch
import re


rfn = re.compile("n(\d*)w(\d*)(\w*).csv", re.IGNORECASE)
folder_to_look = "."
file_name_pattern = "n*.csv"
titles_new = ["initial", "final", "count", "time"]
titles = ["in{}{}".format(y, x) for x in titles_new for y in xrange(8)]
titles_new += ["imp", "inum", "n", "w", "type"]
with open("compNoIndMov.csv", 'wb') as novo_csvfile:
	writer = csv.writer(novo_csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
	writer.writerow(titles_new)

	for file_name in fnmatch.filter(os.listdir(folder_to_look), file_name_pattern):
		nome_separado = rfn.search(file_name)
		test_n = int(nome_separado.group(1))
		test_w = int(nome_separado.group(2))
		test_type = nome_separado.group(3)
		# print file_name
		with open(file_name, 'rb') as csvfile:
			spamreader = csv.DictReader(csvfile, delimiter=';')
			for row in spamreader:
				for y in xrange(8):
					linha_atual = [int(row["in{}initial".format(y)]), int(row["in{}final".format(y)]),
						int(row["in{}count".format(y)]), float(row["in{}time".format(y)])]
					linha_atual += [1.0 * linha_atual[0] / linha_atual[1], y, test_n, test_w, test_type]
					writer.writerow(linha_atual)
