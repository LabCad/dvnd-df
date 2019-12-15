#!/usr/bin/python
# -*- coding: utf-8 -*-
if __name__ == '__main__':
    import os
    import re

    folders = [x for x in os.listdir(".") if os.path.isdir(x)]

    print("file_name;solver;size;initial_value;final_value;elapsed_time;imp_value;instance_num;num_workers")
    for folder in folders:
        # print("folder: {}".format(folder))
        solver = folder
        initial_value = "-1"
        final_value = "-1"
        elapsed_time = "-1"
        imp_value = "-1"
        instance_num = "-1"
        num_workers = "-1"

        for file_name in os.listdir(folder):
            # print("file: {}".format(file_name))

            size = 0
            instance = ""
            for line in open("{}/{}".format(folder, file_name)):
                line = line.replace('\n', '')

                if line.startswith("Size:"):
                    # Size: 51 - file name: eil51.tsp
                    values = re.match(r'\w*: (\d*) .*: (.*)', line, re.M | re.I)
                    size = values.group(1)
                    instance = values.group(2)

                elif line.startswith("data-line;"):
                    data = line.split(';')
                    initial_value = data[2]
                    final_value = data[4]
                    elapsed_time = data[6]
                    imp_value = data[14]
                    instance_num = data[18]
                    num_workers = data[20]

            print(";".join([file_name, solver, size, initial_value, final_value, elapsed_time, imp_value, instance_num,
                            num_workers]))
            # break
