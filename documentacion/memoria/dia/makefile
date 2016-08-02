#!/bin/sh

SOURCES := $(wildcard *.dia)
IMAGES  := $(SOURCES:.dia=.png)

all: $(IMAGES) 

%.png: %.dia
	#dia $< -e $@; 
	dia -t png-libart $<

clean: 
	rm -f *.png

