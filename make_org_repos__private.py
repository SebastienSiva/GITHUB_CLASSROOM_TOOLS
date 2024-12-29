#!/usr/bin/env python3

import sys, subprocess, re

if len(sys.argv) < 2:
	print("Need org name. Use> gh org list")
	sys.exit(0)

repo_list = subprocess.check_output(
	["gh", "repo", "list", sys.argv[1], "--visibility", "public"])


for repo_line in repo_list.decode().split("\n"):
	repo_details =  repo_line.split("\t")
	if re.match(r"^.*/.*$", repo_details[0]):
		repo_name = repo_details[0]
		print(repo_name)
		# gh repo edit --visibility private
		cmd = ['gh', 'repo', 'edit', repo_name, 
			'--visibility', 'private', '--accept-visibility-change-consequences']
		subprocess.run(cmd)


"""
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
			
	
"""

