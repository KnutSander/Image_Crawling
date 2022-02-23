#!usr/bin/env python3

#-------------------------------------------------------------------------------
# Imports and global variables.
#-------------------------------------------------------------------------------

import sys, requests, validators
from bs4 import BeautifulSoup as bs

#-------------------------------------------------------------------------------
# Routines.
#-------------------------------------------------------------------------------

class ImageCrawlAndLabel:

    def __init__(self, url):
        # List of visited and not visited urls
        self.visUrls = []
        self.notVisUrls = []

        # Save the url, so only urls on the domain and site are gathered
        self.baseUrl = url

        # Store the images in a dictonary, based on their sport
        self.imageLinks = {}

        
    # Returns the main content part of the given url
    # Specifically constructed for The Independent website
    # This disregards any links in headers, footers, etc.
    def getContentSoup(url):
        # Get the website content, turn it into soup and extract frameInner/main content
        html = requests.get(url).text
        soup = bs(html, 'html.parser')
        return soup.find_all(id='frameInner')


    def getImages(self, url, soup):
        # Group the images based on what is next in the link after /sport/
        # Label the images based on their alt text or maybe article title, both?
    
    def getRelatedLinks(self, soup):
        # Extracts every link in the soup
        links = soup('a')
        
        for link in links:
            path = link.get('href')
            # Make sure the path is under the same domain as the base
            # Also make sure it exists
            if path and path.startswith(self.baseUrl):
                # Don't add the path if it is in the list to be explored
                # Don't add it if it's been explored already
                if path not in self.visUrls and path not in self.notVisUrls:
                    self.notVisUrls.append(path)

                    
    # Main crawling function that calls everything else
    def crawl(self, url):
        # Get the soup, the main webpage content
        soup = self.getContentSoup(url)

        # Extract all the images from the url
        self.getImages(url, soup)

        # Extract any page links
        self.getRelatedLinks(soup)
        
    
    # Main function that runs the crawling
    def start(self):
        # Get the urls on the base page
        self.getRelatedLinks(self.getContentSoup(self.baseUrl))

        # Set depth to limit crawl depth
        count = 0
        depth = 1
        
        # Main loop
        while self.notVisUrls:
            url = self.notVisUrls.pop(0)
            self.crawl(url)
            self.visUrls.append(url)

            count += 1
            if count >= 10:
                break

        self.outputResult()


# Remember to sleep the crawling to avoid being aggressive
# Disregard pictures on the base page
# Extract the content div only, with id frameInner
        
#-------------------------------------------------------------------------------
# Main program.
#-------------------------------------------------------------------------------

url = "https://www.independent.co.uk/sport"

# Validate url, just in case
if validators.url(url):
    icl = ImageCrawlAndLabel(url)
else:
    print("Url not valid, please provide a valid url")
