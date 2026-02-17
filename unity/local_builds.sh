#!/bin/bash

# might need to edit scene name in Editor/Builder.cs

export PATH=/Applications/Unity/Hub/Editor/6000.3.4f1/Unity.app/Contents/MacOS/:$PATH

if [ $# -eq 0 ]; then
 echo "no asg directory specified"
 echo "./local_builds.sh ../temp_grading/ITEC4650/d_653730/asg2-flappy-dragon-submissions"
 exit 0
fi

for i in $1/*/*; do
	echo $i
	cp -r Editor $i/Assets
	# look for and rename scene.
	./scene_search.sh $i
	Unity -quit -batchmode -nographics -executeMethod Builder.BuildProject -projectPath $i > $i/build_log.txt
done



