'''
Simple Pipeline - Sucuri Version
Leandro Marzulo <leandro.marzulo@flatlabs.com.br>

Usage:
python pipeline.sucuri.py <numer_of_workers>
'''
import sys
import os
from include_lib import *


#need this environment variable if Sucuri is installed manually.
# sys.path.append(os.environ['SUCURIHOME'])
# from sucuri import *

include_pydf()


from pyDF import *


def print_line(args):
	line = args[0]
	print "-- " + line[:-1] + " --"

def mostrando_line(args):
	line = args[0].value
	print "++ " + line[:-1] + " ++"

# nprocs = int(sys.argv[1])
nprocs = 4

graph = DFGraph()
sched = Scheduler(graph, nprocs, mpi_enabled=False)
fp = open("text.txt", "r")

src = Source(fp)
printer = Serializer(print_line, 1)
mostrar = Node(mostrando_line, 1)

printer.pin([0])
graph.add(src)
graph.add(printer)
graph.add(mostrar)

src.add_edge(printer, 0)
src.add_edge(mostrar, 0)

sched.start()