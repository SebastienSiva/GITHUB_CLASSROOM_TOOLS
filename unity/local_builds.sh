#!/bin/bash

export PATH=/Applications/Unity/Hub/Editor/2022.3.17f1/Unity.app/Contents/MacOS/:$PATH

if [ $# -eq 0 ]; then
 echo "no asg directory specified"
 exit 1
fi

for i in $1/*/*; do
	echo $i
	cp -r Editor $i/Assets
	Unity -quit -batchmode -nographics -executeMethod Builder.BuildProject -projectPath $i > $i/build_log.txt
done



