#!/usr/bin/python
# -*- coding: UTF-8 -*-
import math


def calcular_valor(dist, s, name=""):
	s_ini = s
	print "{}={}".format(name, s)
	s = s.replace(" ", "").upper()
	pacos = []
	for i in xrange(len(s)):
		pacos.append(dist[s[i]][s[(i + 1) % len(s)]])
	lpacos = len(pacos)
	tsp, mlp = sum(pacos), sum([(lpacos - i) * pacos[i] for i in xrange(lpacos)])
	print "tsp: {:.0f}, mlp: {:.0f} - {}".format(tsp, mlp, [int(round(x)) for x in pacos])
	return tsp, mlp, s_ini, name


def subtrair(s, s2, name=""):
	return s[0] - s2[0], s[1] - s2[1], "", name


def escrever(s):
	return "{} = {:.0f}/{:.0f}".format(s[3], s[0], s[1])


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


if __name__ == "__main__":
	pontos = dict()
	pontos['A'] = 2, 2
	pontos['B'] = 1, 4
	pontos['C'] = 2, 8
	pontos['D'] = 4, 9
	pontos['E'] = 6, 7
	pontos['F'] = 9, 6
	pontos['G'] = 10, 4
	pontos['H'] = 7, 1
	pontos['I'] = 5, 2

	print "pontos"
	print pontos

	fator = 100
	for k, v in pontos.items():
		pontos[k] = v[0] * fator, v[1] * fator

	print "\npontos * " + str(fator)
	print pontos

	sorted_keys = sorted(pontos.keys())
	dist = dict()
	max_dis = 0
	for k in sorted_keys:
		dist[k] = dict()
		for j in sorted_keys:
			x = pontos[k][0] - pontos[j][0]
			y = pontos[k][1] - pontos[j][1]
			dist[k][j] = round(math.sqrt(x * x + y * y))
			max_dis = max(max_dis, dist[k][j])

	imprimir_tabela(dist, max_dis, sorted_keys)

	print "\nsolucoes "
	soltext = dict()
	soltext["s1"] = "A   B   C   D   E   F   G   H   I"
	soltext["m1 o s1"] = "A   H   G   F   E   D   C   B   I"
	soltext["m2 o s1"] = "A   B   C   D   E   G   F   H   I"
	soltext["m3 o s1"] = "A   D   C   B   E   F   G   H   I"
	soltext["m1 o m3 o s1"] = "A   H   G   F   E   B   C   D  I"
	soltext["m2 o m1 o s1"] = "A   H   G   F   E   C   D   B   I"
	soltext["m2 o m3 o s1"] = "A   D   C   B   E   G   F   H   I"
	soltext["m3 o m1 o s1"] = "A   F   G   H   E   D   C   B   I"
	soltext["m1 o m2 o s1"] = "A  H  F  G  E  D  C  B  I"

	solvalue = dict()
	for key, value in soltext.items():
		solvalue[key] = calcular_valor(dist, value, key)

	for key in soltext.keys():
		keyT = key.replace(" ", "")
		if keyT.endswith("os1"):
			addmovs = []
			addmovs += [("{} - {}".format(key, keyT[-2:]), keyT[-2:], key)]

			splited = keyT.split("o")
			if len(splited) > 2:
				addmovs += [("{} - {}".format(key, key[5:]), key[5:], key)]

			for addmov in addmovs:
				solvalue[addmov[0]] = subtrair(solvalue[addmov[2]], solvalue[addmov[1]], addmov[0])

	print "\nlimpo"
	for x in sorted(solvalue.keys()):
		print escrever(solvalue[x])
