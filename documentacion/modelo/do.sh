cp ./plantillas/*.txt .
grep -l '<COLOR>' *.txt | xargs sed -i 's/<COLOR>/#FFFFAA/g'
