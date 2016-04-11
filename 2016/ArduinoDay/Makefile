# Este es un makefile para compliar los diagramas
.PHONY: slides

slides: PlatformIO.slides.html

PlatformIO.slides.html: PlatformIO.ipynb
	jupyter-nbconvert --to slides $^
all: img/estructura.svg

img/estructura.svg: diags/estructura.rackdiag
	rackdiag -T svg $^ -o $@
