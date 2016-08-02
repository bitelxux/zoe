rm -f coverage.xml
rm -f *.db
rm -f ./src/*.db
rm -f ./src/tests/*.db
nosetests --with-xcoverage --with-xunit --cover-package=zoe --cover-erase 
pylint --rcfile=pylint.rc -f parseable src | tee pylint.out
/usr/bin/sloccount --duplicates --wide --details src > sloccount.sc
