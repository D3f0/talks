TARGET = KivyAndroid.pdf
PWD=$(shell pwd)

all: ${TARGET}

%.pdf: %.md
	pandoc -s -N -t beamer $^ -o $@

clean:
	rm -rf ${TARGET}
re: clean all
