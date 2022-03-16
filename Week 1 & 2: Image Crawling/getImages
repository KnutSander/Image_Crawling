#!/usr/bin/env python3

import sys, requests
from bs4 import BeautifulSoup as bs

"Takes a link as an argument, and outputs a list of direct image links and their description"

# Take input from command line
if len(sys.argv) < 2:
    print("Usage:", sys.argv[0], "<url>", file=sys.stderr)
    sys.exit(1)

# The get method of requests returns the given webpage
# The .text extracts the information as a string
request = requests.get(sys.argv[1]).text

# Using BeautifulSoup, make the plain text into a complex tree of Python objects
# The soup variable can be queried to extract various information
soup = bs(request, 'html.parser')

# Using find_all in the soup will return a list containing all matching objects
images = soup.find_all('img')

# Put the image links and alt text into a dictionary
imgDict = {}
for im in images:
    imgDict[im.get('alt')] = im.get('src')

# Output the dictionary to a file
out = open("singleOutput.txt", "w")
for key, value in imgDict.items():
    out.write(str(key) + ": " + str(value) + "\n")
out.close()
