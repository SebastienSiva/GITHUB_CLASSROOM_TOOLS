#!/usr/bin/env python3

import sys, csv, webbrowser, os

cwd = os.path.basename(os.getcwd())
repo_name = cwd[0:-1 * len("submissions")]
URL="https://ggc-itec4650-sp2024.github.io/" + repo_name

with open('../scripts/classroom_roster.csv') as csvfile:
    spamreader = csv.reader(csvfile)
    next(spamreader) # skip first row
    for row in spamreader:
        print(row[1])
        webbrowser.open_new_tab(URL + row[1] + "/")







