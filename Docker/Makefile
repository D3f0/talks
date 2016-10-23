ifeq ($(OS),Windows_NT)
    OPEN = start
else
    UNAME_S := $(shell uname -s)
    ifeq ($(UNAME_S),Linux)
        OPEN = xdg-open
    endif
    ifeq ($(UNAME_S),Darwin)
        OPEN = open
    endif
endif

%.pdf: %.md
	pandoc -t beamer -s $^ -o $@

all: docker.pdf
	$(OPEN) *.pdf