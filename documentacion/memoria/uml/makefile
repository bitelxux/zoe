#!/bin/sh

SOURCES := $(wildcard *.ts)
IMAGES  := $(SOURCES:.ts=.png)

all: $(IMAGES) 

%.png: %.ts ../../../tools/sequence_diagram.py
	python ../../../tools/sequence_diagram.py $<; \
	cp $@ ./images

clean: 
	rm -f *.png

