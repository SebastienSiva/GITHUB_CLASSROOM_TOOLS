#!/bin/bash

if [ $# -eq 0 ]; then
 echo "no chapter number specified"
 echo "./open_all.sh 3"
 exit 1
fi



cd d_642427/pythonchapters-submissions

echo "ALL RELEVANT FILES"

find . | grep -e ".*$1.*html$" -e ".*$1.*ipynb$" | sort

echo
echo
echo "OPEN ALL HTML FILES BY CHAPTER NUMBER $1"
for i in `find . | grep "Chap$1.*html" | sort`; do
	echo $i
	open $i
done
