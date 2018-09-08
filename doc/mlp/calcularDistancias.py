import math


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


pading = int(math.floor(math.log(max_dis, 10))) + 1
formato = '{:>' + str(pading) + '}&'
print "\nTabela"
print "   & " + " ".join([formato.format(x) for x in sorted_keys])
formato = '{:' + str(pading) + '.0f}'
for k in sorted_keys:
	linha = " %s & " % k
	for j in sorted_keys:
		if k == j:
			linha += " " * (pading) + "& "
		else:
			linha += formato.format(dist[k][j]) + "& "
	print linha


def calcular_valor(s, name=""):
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


print "\nsolucoes "


def subtrair(s, s2, name=""):
	return s[0] - s2[0], s[1] - s2[1], "", name


s1 = calcular_valor("A   B   C   D   E   F   G   H   I", "s1")
m1s1 = calcular_valor("A   H   G   F   E   D   C   B   I", "m1 o s1")
m1 = subtrair(m1s1, s1, "m1")
m2s1 = calcular_valor("A   B   C   D   E   G   F   H   I", "m2 o s1")
m2 = subtrair(m2s1, s1, "m2")
m3s1 = calcular_valor("A   D   C   B   E   F   G   H   I", "m3 o s1")
m3 = subtrair(m3s1, s1, "m3")
m2m3s1 = calcular_valor("A   D   C   B   E   G   F   H   I", "m2 o m3 o s1")
m2m3 = subtrair(m2m3s1, s1, "m2m3")
m1m3s1 = calcular_valor("A   H   G   F   E   B   C   D  I", "m1 o m3 o s1")
m1m3 = subtrair(m1m3s1, s1, "m1m3")
m3m1s1 = calcular_valor("A   F   G   H   E   D   C   B   I", "m3 o m1 o s1")
m3m1 = subtrair(m3m1s1, s1, "m3m1")
m2m1s1 = calcular_valor("A   H   G   F   E   C   D   B   I", "m2 o m1 o s1")
m2m1 = subtrair(m2m1s1, s1, "m2m1")


def escrever(s):
	return "{} = {:.0f}/{:.0f}".format(s[3], s[0], s[1])


print "\nlimpo"
movsSols = [s1,
	m1, m1s1, m2, m2s1,
	m3, m3s1, m1m3, m1m3s1,
	m2m3, m2m3s1, m3m1, m3m1s1,
	m2m1, m2m1s1]
for x in movsSols:
	print escrever(x)
