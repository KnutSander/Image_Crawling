#!usr/bin/env python3

"""
" A program to test and explore how to filter and export images from
" the articles on The Independent.
" The current problem is that most image objects have several links for 
" different page sizes, so need to filter out urls that lead to similar images
"""

#-------------------------------------------------------------------------------
# Imports and Global Variables
#-------------------------------------------------------------------------------

# Standard imports
import sys, requests, time, csv, json, validators

# BeautifulSoup, html handling
from bs4 import BeautifulSoup as bs

#-------------------------------------------------------------------------------
# Class and Methods
#-------------------------------------------------------------------------------


def extract_images(url):
    "Gets all image links from the given url"

    # Extract the html of the given url
    html = requests.get(url).text

    # Make the html into soup
    soup = bs(html, 'html.parser')

    # Extract the 'frameInner', article main content
    soup = soup.find(id='frameInner')

    
    # Get all images on the page
    all_images = soup.find_all(['img', 'amp-img'])

    # List of image urls
    im_urls = []
        
    for image in all_images:

        # Images with links as parents link to other pages, so disregard them
        link_parent = image.find_parent('a')
        if link_parent == None:

            # Make sure the src link is a valid web link
            src = image.get('src')
            if "http" in src:
                im_urls.append(src)


    # Look for the stems of the image links
    stems = []
    for url in im_urls:
        split = url.split('?')
        stems.append(split[0])
    
    # Removes duplicate entries from the list
    stems = list(dict.fromkeys(stems))    
    
    print(stems)
    
    
#-------------------------------------------------------------------------------
# Main Program
#-------------------------------------------------------------------------------

# Ensure we were invoked with a single argument
if len (sys.argv) != 2:
    print ("Usage: %s <article-link>" % sys.argv[0], file=sys.stderr)
    exit (1)

# Ensure the link is a valid url
if not validators.url(sys.argv[1]):
    print("Provided input was not a valid url")
    exit(2)

# Extract the images
extract_images(sys.argv[1])

#-------------------------------------------------------------------------------
# End of image_filtering.py
#-------------------------------------------------------------------------------
