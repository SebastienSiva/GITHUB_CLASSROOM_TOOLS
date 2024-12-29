#!/usr/bin/env python3

import sys, subprocess, re

# get classroom id: gh classroom list   

if len(sys.argv) < 2:
	print("Need classroom id. Use> gh classroom list")
	sys.exit(0)

asg_list = subprocess.check_output(["gh", "classroom", "assignments", "-c", sys.argv[1]])

asg_ids_to_remove = []
for asg_line in asg_list.decode().split("\n"):
	asg_details =  asg_line.split("\t")
	if re.match(r"^\d+$", asg_details[0]):
		asg_id, asg_name = asg_details[0:2]
		a = input("Remove studdnts from asg ID: %s\tTitle: %s (y[n])? " % (asg_id, asg_name))
		if(a == 'y'): 
			asg_ids_to_remove.append(asg_id)

print("Removing student collaborators from asgs:", asg_ids_to_remove)

for asg_id in asg_ids_to_remove:
	print("\nProcessing Asg:", asg_id)
	repo_list = subprocess.check_output(["gh", "classroom", "accepted-assignments", "-a", asg_id])
	for repo_line in repo_list.decode().split("\n"):
		repo_details = repo_line.split("\t")
		if re.match(r"^\d+$", repo_details[0]):	
			stud_id = repo_details[-2]
			url = repo_details[-1]
			org, repo = re.match(r"^(.*)//(.*)/(.*)/(.*)$", url).groups()[-2:]
			print("Removing:", stud_id, "From:", repo)
			cmd = ["gh", "api", "--method", "DELETE", 
				"-H", "Accept: application/vnd.github+json", 
				"-H", "X-GitHub-Api-Version: 2022-11-28", 
				"/repos/%s/%s/collaborators/%s" % (org, repo, stud_id)]
			subprocess.run(cmd)
			
	
	
