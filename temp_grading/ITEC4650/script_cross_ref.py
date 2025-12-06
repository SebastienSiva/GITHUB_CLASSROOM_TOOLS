#!/usr/bin/env python3

import os, sys

from glob import glob



top_dir = sys.argv[1]

for stud in glob(f'{top_dir}/*'):
	stud_files = {}
	for cs_file_path in glob(f'{stud}/**/*.cs', recursive=True):
		if 'Assets' in cs_file_path:
			cs_class_name = os.path.basename(cs_file_path)[0:-3]
			stud_files[cs_class_name] = cs_file_path
	
	cross_ref_found = False
	for classA in stud_files:
		for classB in stud_files:
			if classA != classB:
				if classA in open(stud_files[classB], 'r').read():
					cross_ref_found = True
	
	if cross_ref_found == False:
		print("No Cross Ref For " + stud)
