all: src/wamca2016lib.so

src/wamca2016lib.so: /home/rodolfo/git/wamca2016/source/*.cu /home/rodolfo/git/wamca2016/source/*.cpp
	rm -f src/wamca2016lib.so
	python src/main.py -c

run: all
	python src/main.py

clean:
	rm src/*.pyc src/*.log src/*.so

.PHONY: test syncHomeUff exec_dvnd_4_24 stop

test: all
	#export DVND_HOME=`cd src && pwd`
	#export PYDF_HOME=`cd /home/rodolfo/git/Sucuri && pwd`
	# cd test
	python2 -m unittest discover

syncHomeUff:
	sh script/dvnd_home_uff.sh

exec_dvnd_4_24: all
	nohup script/runexp.sh 4 24 1_4 dvnd "0 1 2 3 4 5 6 7" > dvnd_n4w24h1_4dc2opin0_7.txt 2>&1 &

stop:
	pkill runexp.sh
	pkill mpirun
	pkill python
