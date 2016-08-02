#ejecutar en directorio de tests
rm -rf cover
nosetests  --with-coverage --cover-erase --cover-html --cover-package=console,node,core,utils,net,plubins,storage
python-coverage report --omit=/usr/*
