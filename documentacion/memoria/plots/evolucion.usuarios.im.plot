#!/usr/bin/gnuplot -persist
set terminal png nocrop size 1024, 768
set output 'evolucion.usuarios.im.png'
set style histogram
set style data histogram
set style fill solid 1.00 border 0
set title "Evolución de usuarios prevista entre años 2010 a 2013"
set xlabel "Año"
set ylabel "Millones de usuarios"
set yrange [0:2000]
set boxwidth 0.8
plot "./evolucion.usuarios.im.data" with boxes notitle linecolor rgb "#557A98"
