#!/usr/bin/env python3

import sys, glob, time, datetime, os.path, shutil, subprocess, csv, os

from git import Repo

print_time_format = "%x %a %I:%M %p"

if len(sys.argv) < 6:
	print("USAGE:   ./get_asg.py working_dir asg_id m/d/yy h:m [A|P]M")
	print("EXAMPLE: ./get_asg.py temp_grading/DATA1501 642427 8/26/24 11:59 PM")
	print("Asg Id can be found in website under Download/Clone with CLI")
	sys.exit(0)

working_dir = sys.argv[1]
asg_id = sys.argv[2]
repos_dir = f'{working_dir}/d_{asg_id}'
due_date = datetime.datetime.strptime(
	' '.join((sys.argv[3], sys.argv[4], sys.argv[5])), 
	"%m/%d/%y %I:%M %p")
due_date += datetime.timedelta(minutes=1)

#read roster
roster = {} # {'gh_userid1': 'firstname_lastname', ...}
with open(f'{working_dir}/classroom_roster.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
    	id = row['identifier']
    	if '@ggc.edu' in id: # skip non-ggc entries in roster (test gmail accounts...)
    		last_name, first_name, email = id.split(",")
    		roster[row['github_username']]  = '_'.join((
    			first_name.replace(" ", ""), 
    			last_name.replace(" ", ""), 
    			email.replace('@ggc.edu', '')))

# CLEAN OLD DIR
if os.path.isdir(repos_dir):
	if(input(f"Confirm delete {repos_dir} (y/n): ") == 'y'):
		shutil.rmtree(repos_dir)

# GRAB STUDENT REPOS
# Note: requires github classroom cli and gh auth login
# gh classroom clone student-repos -a 642427 -d repos_dir
if not os.path.isdir(repos_dir):
	subprocess.run(
		["gh", "classroom", "clone", "student-repos", "-a", asg_id, "-d", repos_dir]) 

	# RENAME REPO FOLDERS USING ROSTER NAMES
	for path in glob.glob(f'{repos_dir}/*/*'):
		dir_name = os.path.basename(path)
		for id in roster:
			if id in dir_name:
				# replace last occurence of id with real name
				new_path = roster[id].join(path.rsplit(id, 1)) 
				os.rename(path, new_path)
				break
		else:
			shutil.rmtree(path)

# for each repo in the directory check data and propose rollback options
for path in sorted(glob.glob(f'{repos_dir}/*/*')):
	repo = Repo(path)
	repo_name = os.path.basename(repo.working_dir)
	commits = list(repo.iter_commits(all=True, max_count=100))
	dt = datetime.datetime.fromtimestamp(commits[0].committed_date)
	if dt > due_date:
		#LATE
		print(repo_name, "Requires Rollback")	
		for i in range(len(commits)):
			c = commits[i]
			dt = datetime.datetime.fromtimestamp(c.committed_date) 
			print("\t%s. %s %s '%s' %s" % (
				len(commits)-(i+1),
				'LATE' if dt > due_date else 'ONTIME',
				dt.strftime(print_time_format),
				c.message.strip(), 
				c.hexsha[0:6]))
				
		c_id = int(input("Rollback ID: "))
		target_commit = commits[len(commits) - (c_id+1)]
		dt = datetime.datetime.fromtimestamp(target_commit.committed_date) 
		print("roll back to: " + dt.strftime(print_time_format))
		repo.git.checkout(target_commit.hexsha)
	else:
		print(repo_name, "Submitted:", 
			" " * (40 - len(repo_name)), 
			dt.strftime(print_time_format))

