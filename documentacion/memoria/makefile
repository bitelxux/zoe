#!/bin/sh

memoria.pdf: memoria.rst requisitos.rst implementacion.rst faq.rst despues.rst todo.rst punch.rst ejecucion.rst
	make -C uml
	make -C plots
	make -C dia
	rm -f memoria.pdf; \
	rst2pdf -b1 -e preprocess memoria.rst -s estilo | grep -v line

clean:
	rm -f memoria.pdf
