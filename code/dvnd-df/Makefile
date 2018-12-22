all: src/wamca2016lib.so

src/wamca2016lib.so: src/*.py /home/rodolfo/git/wamca2016/source/*.cu /home/rodolfo/git/wamca2016/source/*.cpp
	rm src/wamca2016lib.so
	python src/main.py -c

run: all
	python src/main.py

clean:
	rm src/*.pyc src/*.log src/*.so

.PHONY: test
test: all
	#export DVND_HOME=`cd src && pwd`
	#export PYDF_HOME=`cd /home/rodolfo/git/Sucuri && pwd`
	# cd test
	python2 -m unittest discover

