#!/bin/bash

URL="http://localhost:8000"


for i in */WebGL; do
	open -a "Google Chrome" "$URL/$i/index.html"
done


# open -a "Google Chrome" "https://stackoverflow.com"

# http://localhost:8000/finalexam-ABDeni811/WebGL/index.html