#!/bin/bash


if [ $# -eq 0 ]; then
 echo "no unity project directory specified"
 echo "./scene_search.sh /Users/ssiva/github/SebastienSiva/GITHUB_CLASSROOM_TOOLS/temp_grading/ITEC4650/d_735286/week2demo-submissions/week2demo-Tripp_Barker_cbarker7"
 exit 0
fi


all_scenes=$(find $1 -name "*.unity")
target_scene="Game.unity"

scene_file=""
for i in $all_scenes; do
	if echo $i | grep -q "/$target_scene"; then
		echo "Using Scene: $i"
		scene_file=$i
	fi
done

# try first scene that is not SampleScene.unity
if [[ ! -n $scene_file ]]; then
	echo "WARNING: Failed to find $target_scene"
	for i in $all_scenes; do
		if ! echo $i | grep -q "SampleScene.unity"; then
			echo "Found alternative scene: $i" 
			scene_file=$i
			break
		fi
	done
fi

# try SampleScene.unity
if [[ ! -n $scene_file ]]; then
	echo "WARNING: Failed to any alternative scene"
	
	for i in $all_scenes; do
		if echo $i | grep -q "SampleScene.unity"; then
			echo "Found SampleScene scene: $i" 
			scene_file=$i
			break
		fi
	done
fi

if [[ ! -n $scene_file ]]; then
	echo "WARNING: No valid scene found"
	exit 0
elif ! echo $scene_file | grep -q "/$target_scene"; then
	echo "Renaming Scene $i to $target_scene"
	d=$(dirname $i)
	mv $i $d/$target_scene
fi


#if echo "$all_scenes" | grep "/SimpleMove.cs"; then
#  echo "String found!"
#else
#  echo "String not found."
#fi




