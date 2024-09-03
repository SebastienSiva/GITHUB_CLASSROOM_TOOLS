#!/usr/bin/env python3

import sys, glob, time, datetime, os.path
from git import Repo

print_time_format = "%x %a %I:%M %p"

repos_dir = sys.argv[1]
due_date = datetime.datetime.strptime(
	' '.join((sys.argv[2], sys.argv[3], sys.argv[4])), 
	"%m/%d/%y %I:%M %p")
due_date += datetime.timedelta(minutes=1)
print("DUE DATE", due_date)

# for each repo in the directory check data and propose rollback options
for path in glob.glob(f'{repos_dir}/*'):
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
	#tree = prev_commits[0].tree
