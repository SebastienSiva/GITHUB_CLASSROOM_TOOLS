#!/bin/bash

export PATH=/Applications/Unity/Hub/Editor/2022.3.17f1/Unity.app/Contents/MacOS/:$PATH


for i in *; do
	echo $i
	cp -r ../scripts/Editor $i/Assets
	Unity -quit -batchmode -nographics -executeMethod Builder.BuildProject -projectPath $i > $i/build_log.txt
done



