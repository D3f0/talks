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

PANDOC_ARGS= -H make-code-snippet-footnote-size.tex

all: open commit_and_push

%.pdf: %.md
	pandoc -t beamer -s $^ $(PANDOC_ARGS) -o $@


open: docker.pdf
	$(OPEN) *.pdf

commit_and_push: docker.pdf
	git add -u .
	git add images
	git commit -m "Update `date`"
	git push
	echo $(UPDATE_MSG)

clean:
	rm docker.pdf

re: clean all
