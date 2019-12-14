all: dvnd_df/wamca2016lib.so

dvnd_df/wamca2016lib.so: ~/parco/dvnd-df/wamca2016/source/*.cu ~/parco/dvnd-df/wamca2016/source/*.cpp
	rm -f dvnd_df/wamca2016lib.so
	python dvnd_df/main.py -c

run: all
	python main.py

clean:
	rm dvnd_df/*.pyc dvnd_df/*.log dvnd_df/*.so

.PHONY: test syncHomeUff exec_dvnd_4_4 exec_dvnd_4_8 exec_dvnd_4_12 exec_dvnd_4_24 stop

test: all
	#export DVND_HOME=`cd src && pwd`
	#export PYDF_HOME=`cd /home/rodolfo/git/Sucuri && pwd`
	# cd test
	python2 -m unittest discover

syncHomeUff:
	sh script/dvnd_home_uff.sh

exec_dvnd_4_4: all
	nohup script/runexp.sh 4 4 1_4 dvnd "0 1 2 3 4 5 6 7" > dvnd_n4w4h1_4dc2opin0_7.txt 2>&1 &

exec_dvnd_4_11: all
	nohup script/runexp.sh 4 11 1_4 dvnd "0 1 2 3 4 5 6 7" > dvnd_n4w11h1_4dc2opin0_7.txt 2>&1 &

exec_dvnd_4_8: all
	nohup script/runexp.sh 4 8 1_4 dvnd "0 1 2 3 4 5 6 7" > dvnd_n4w8h1_4dc2opin0_7.txt 2>&1 &

exec_dvnd_4_12: all
	nohup script/runexp.sh 4 12 1_4 dvnd "0 1 2 3 4 5 6 7" > dvnd_n4w12h1_4dc2opin0_7.txt 2>&1 &

exec_dvnd_4_24: all
	nohup script/runexp.sh 4 24 1_4 dvnd "0 1 2 3 4 5 6 7" > dvnd_n4w24h1_4dc2opin0_7.txt 2>&1 &

exec_rest: all
	rm -f dvnd_n4w24h1_4dc2opin6_7.txt
	rm -f dvnd_n4w12h1_4dc2opin6_7.txt
	rm -f ../../doc/results/dvnd_n4w12in5*
	nohup script/runexp.sh 4 12 1_4 dvnd "0 1 2 3 4 5" > dvndMv12_n4w12h1_4dc2opin0_5.txt 2>&1 &

exec_0: all
	rm -f ../../doc/results/dvnd_n4w12in0*
	nohup script/runexp.sh 4 12 1_4 dvnd "0" > dvndMv12_n4w14h1_4dc2opin0.txt 2>&1 &

exec_1: all
	rm -f ../../doc/results/dvnd_n4w12in1*
	nohup script/runexp.sh 4 12 1_4 dvnd "1" > dvndMv12_n4w12h1_4dc2opin1.txt 2>&1 &

exec_2: all
	rm -f ../../doc/results/dvnd_n4w12in2*
	nohup script/runexp.sh 4 12 1_4 dvnd "2" > dvndMv12_n4w12h1_4dc2opin2.txt 2>&1 &

exec_3: all
	rm -f ../../doc/results/dvnd_n4w12in3*
	nohup script/runexp.sh 4 12 1_4 dvnd "3" > dvndMv12_n4w12h1_4dc2opin3.txt 2>&1 &

exec_4: all
	rm -f ../../doc/results/dvnd_n4w12in4*
	nohup script/runexp.sh 4 12 1_4 dvnd "4" > dvndMv12_n4w12h1_4dc2opin4.txt 2>&1 &

exec_5: all
	rm -f ../../doc/results/dvnd_n4w12in5*
	nohup script/runexp.sh 4 12 1_4 dvnd "5" > dvndMv12_n4w12h1_4dc2opin5.txt 2>&1 &

exec_6: all
	rm -f ../../doc/results/dvnd_n4w12in6*
	nohup script/runexp.sh 4 12 1_4 dvnd "6" > dvndMv12_n4w12h1_4dc2opin6.txt 2>&1 &

exec_7: all
	rm -f ../../doc/results/dvnd_n4w12in7*
	nohup script/runexp.sh 4 12 1_4 dvnd "7" > dvndMv12_n4w12h1_4dc2opin7.txt 2>&1 &

stop:
	pkill -ec runexp.sh
	pkill -ec mpirun
	pkill -ec mpirun.mpich
	pkill -ec python

stopCluster: stop
	ssh gpu01 pkill -ec python
	ssh gpu02 pkill -ec python
	ssh gpu03 pkill -ec python
	ssh gpu04 pkill -ec python
