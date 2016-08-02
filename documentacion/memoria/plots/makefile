#!/bin/sh

SOURCES := $(wildcard *.plot)
IMAGES  := $(SOURCES:.plot=.png)

all: $(IMAGES) 

%.png: %.plot %.data
	rm -f  $@; \
	rm -f  ./images/$@; \
	gnuplot $<; \
	cp $@ ./images

clean: 
	rm -f *.png
	rm -f images/*.png

