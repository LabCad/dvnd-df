#!/usr/bin/python
# -*- coding: UTF-8 -*-
import math
import random


def calc_dist(dist, sol):
	pacos = []
	for x in xrange(len(sol)):
		pacos.append(dist[sol[x]][sol[(x + 1) % len(sol)]])
	lpacos = len(pacos)
	return sum(pacos), sum([(lpacos - i) * pacos[i] for i in xrange(lpacos)])


def imprimir_tabela(dist, max_dis, sorted_keys):
	pading = int(math.floor(math.log(max_dis, 10))) + 1
	formato = '{:>' + str(pading) + '}&'
	print "\nTabela"
	print "   & " + " ".join([formato.format(x) for x in sorted_keys])
	formato = '{:' + str(pading) + '.0f}'
	for k in sorted_keys:
		linha = " %s & " % k
		for j in sorted_keys:
			if k == j:
				linha += " " * pading + "& "
			else:
				linha += formato.format(dist[k][j]) + "& "
		print linha


def print_sol_value(dist, name, sol):
	print "%s - %s = %s" % (sol, name, calc_dist(dist, sol))


if __name__ == "__main__":
	dist = dict()

	lastone = 10
	assert lastone > 4, "Troca até a posição 4"
	for x in xrange(lastone):
		dist[x] = dict()
		dist[x][x] = 0

	for x in dist.keys():
		for y in xrange(x + 1, lastone):
			dist[x][y] = random.randint(0, lastone ** 2)
			dist[y][x] = random.randint(0, lastone ** 2)
			# dist[y][x] = dist[x][y]

	# Estabelecendo distâncias
	# dist[0][1], dist[3][4] = dist[0][3], dist[1][4]
	# dist[0][2], dist[3][4] = dist[0][3], dist[2][4]
	dist[1][3], dist[3][1] = 1, 2
	dist[0][2], dist[0][3] = 4, 3
	dist[0][1] = 5
	dist[3][4] = dist[2][4]
	dist[1][4] = dist[2][4]
	# teste igual
	valor_igual = random.randint(0, lastone ** 2)
	dist[0][1] = dist[0][2] = dist[0][3] = valor_igual
	dist[1][2] = dist[1][3] = dist[1][4] = valor_igual
	dist[2][1] = dist[2][3] = dist[2][4] = valor_igual
	dist[3][1] = dist[3][2] = dist[3][4] = valor_igual
	assert dist[0][2] + dist[2][1] + dist[1][3] + dist[3][4] == dist[0][3] + dist[3][1] + dist[1][2] + dist[2][4], "^m1(s1) = ^m1(m2(s1))"
	assert dist[0][1] + dist[1][3] + dist[3][2] + dist[2][4] == dist[0][2] + dist[2][3] + dist[3][1] + dist[1][4], "^m2(s1) = ^m2(m1(s1))"

	imprimir_tabela(dist, max([max(x.values()) for x in dist.values()]), sorted(dist.keys()))

	print ""

	sols = dict()
	sols["s1"] = [x for x in xrange(lastone)]

	sols["m1(s1)"] = [x for x in xrange(lastone)]
	sols["m1(s1)"][1], sols["m1(s1)"][2] = sols["m1(s1)"][2], sols["m1(s1)"][1]

	sols["m2(s1)"] = [x for x in xrange(lastone)]
	sols["m2(s1)"][2], sols["m2(s1)"][3] = sols["m2(s1)"][3], sols["m2(s1)"][2]

	sols["m2 o m1(s1)"] = [x for x in xrange(lastone)]
	sols["m2 o m1(s1)"][1], sols["m2 o m1(s1)"][2] = sols["m2 o m1(s1)"][2], sols["m2 o m1(s1)"][1]
	sols["m2 o m1(s1)"][2], sols["m2 o m1(s1)"][3] = sols["m2 o m1(s1)"][3], sols["m2 o m1(s1)"][2]

	sols["m1 o m2(s1)"] = [x for x in xrange(lastone)]
	sols["m1 o m2(s1)"][2], sols["m1 o m2(s1)"][3] = sols["m1 o m2(s1)"][3], sols["m1 o m2(s1)"][2]
	sols["m1 o m2(s1)"][1], sols["m1 o m2(s1)"][2] = sols["m1 o m2(s1)"][2], sols["m1 o m2(s1)"][1]

	for k, v in sols.items():
		print_sol_value(dist, k, v)
		sols[k] = v, calc_dist(dist, v)

	for mov in ["m1", "m2", "m1 o m2", "m2 o m1"]:
		sols["^" + mov] = None, (sols[mov + "(s1)"][1][0] - sols["s1"][1][0], sols[mov + "(s1)"][1][1] - sols["s1"][1][1])
	sols["^m2(m1(s1))"] = None, (sols["m2 o m1(s1)"][1][0] - sols["m1(s1)"][1][0], sols["m2 o m1(s1)"][1][1] - sols["m1(s1)"][1][1])
	sols["^m1(m2(s1))"] = None, (sols["m1 o m2(s1)"][1][0] - sols["m2(s1)"][1][0], sols["m1 o m2(s1)"][1][1] - sols["m2(s1)"][1][1])

	print ""
	for k, v in sols.items():
		print "%s: %s" % (k, v[1])

	assert sols["m1 o m2(s1)"][0] != sols["m2 o m1(s1)"][0], "Não são fortemente independentes"
	assert sols["m1 o m2(s1)"][1][0] == sols["m2 o m1(s1)"][1][0], "Não são independentes - PCV"
	assert sols["m1 o m2(s1)"][1][1] == sols["m2 o m1(s1)"][1][1], "Não são independentes - PML"
	# assert sols["m1"][1][0] == sols["m1 o m2(s1)"][1][0] - sols["m2(s1)"][1][0]
