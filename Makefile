all: dvnd_df/wamca2016lib.so

dvnd_df/wamca2016lib.so: wamca2016/source/*.cu wamca2016/source/*.cpp
	rm -f dvnd_df/wamca2016lib.so
	python dvnd_df/main.py -c

run: all
	python dvnd_df/main.py

clean_sucuri:
	find dvnd_df -type f -name '*.pyc' -delete

clean_simple_pycuda:
	find simple-pycuda -type f -name '*.pyc' -delete

clean:
	find dvnd_df -type f -name '*.pyc' -delete
	find dvnd_df -type f -name '*.log' -delete
	find dvnd_df -type f -name '*.so' -delete

.PHONY: test syncHomeUff exec_dvnd_4_4 exec_dvnd_4_8 exec_dvnd_4_12 exec_dvnd_4_24 stop

test: all
	#export DVND_HOME=`cd src && pwd`
	#export PYDF_HOME=`cd /home/rodolfo/git/Sucuri && pwd`
	# cd test
	python2 -m unittest discover

syncHomeUff:
	sh script/dvnd_home_uff.sh

exec_rvnd_4_4: all
	nohup script/runexp.sh 4 4 1_4 fvnd "0 1 2 3 4 5 6 7" > rvnd_n4w4h1_4dc2opin0_50.txt 2>&1 &

exec_dvnd_4_4: all
	nohup script/runexp.sh 4 4 1_4 dvnd "0 1 2 3 4 5 6 7" > dvnd_n4w4h1_4dc2opin0_50.txt 2>&1 &

exec_rest: all
	rm -f dvnd_n4w24h1_4dc2opin6_7.txt
	rm -f dvnd_n4w12h1_4dc2opin6_7.txt
	rm -f ../../doc/results/dvnd_n4w12in5*
	nohup script/runexp.sh 4 12 1_4 dvnd "0 1 2 3 4 5" > dvndMv12_n4w12h1_4dc2opin0_5.txt 2>&1 &

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
