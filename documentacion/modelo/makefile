#!/bin/sh

TEMPLATES := $(wildcard *.tpl)
TXT  := $(TEMPLATES:.tpl=.txt)
IMAGES  := $(TXT:.txt=.png)

all: $(IMAGES)

%.txt: %.tpl makefile
	sed 's/<BGCOLOR>/#FFFFAA/g' $< > temp;
	sed 's/<ARROWCOLOR>/Orange/g' temp > temp1;
	sed 's/<BORDERCOLOR>/Orange/g' temp1 > temp2;
	sed 's/<COLOR>/#FFFFCA/g' temp2 > $@;
	rm temp*

%.png: %.txt
	java -jar /usr/share/plantuml/plantuml.jar  $<;
	cp $@ images;

clean: 
	rm -f *.png
	rm -f images/*.png

