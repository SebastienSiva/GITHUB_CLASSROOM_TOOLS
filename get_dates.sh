#!/bin/bash
for i in *; do
	cd $i
	j=`git log -1 | grep "Date:" | cut -c 13-`
	echo $j $i
	cd ../
done | sort

