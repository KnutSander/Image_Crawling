#!/usr/bin/env python3

import sys, requests, validators
from bs4 import BeautifulSoup as bs

"Program that gets direct images links iteratively by exploring links on the webpage"

class ImageLinkCrawler:

    # Initalise variables
    def __init__(self, url, depth=1):
        # Number values used by the program
        self.searchDepth = int(depth)
        self.count = 0

        # Lists of urls visited and that needs to be visited
        self.visitedUrls = []
        self.urlsToVisit = [url]

        # Dictionary that will contain lists of picture links
        self.imageLinks = {}
       

    # Returns a list of all image links in the given soup
    def getImages(self, soup):
        # Using find_all in the soup will return a list containing all matching objects
        images = soup.find_all('img')

        # Put the image links into a list
        imgList = []
        for im in images:
            src = im.get('src')
            # Only interested in image links that exist and are valid web links
            if src and src.startswith("https"):
                imgList.append(src)

        return imgList
    

    # Gets all links in the soup and adds them to the list of urls to visit
    def getLinks(self, soup):
        # Gets all the links in the soup
        links = soup.find_all('a')
        
        for link in links:
            path = link.get('href')

            # Make sure the path exists and that it's a valid path
            if path and path.startswith("https"):
                # Make sure the path hasn't already been explored or is on the list to be explored
                if path not in self.visitedUrls or path not in self.urlsToVisit:
                    self.urlsToVisit.append(path)
                
        
    # Crawling function
    def crawl(self, url):
        html = requests.get(url).text
        soup = bs(html, 'html.parser')

        # Extract all image links and put them into a dictionary
        self.imageLinks[url] = self.getImages(soup)
        
        # Extract all page links
        self.getLinks(soup)
        

    # Main program loop
    def start(self):
        while self.urlsToVisit:
            url = self.urlsToVisit.pop(0)
            self.crawl(url)
            self.visitedUrls.append(url)
            
            self.count += 1
            # Exit loop when loop depth has been reached
            if self.count >= self.searchDepth:
                break

        self.outputResult()


    # Prints the results of the crawl to a text file
    def outputResult(self):
        # Open or create the file
        output = open("imageLinks.txt", "w")

        # Iterate through the dictionary to print all values
        for pageName, linkList in self.imageLinks.items():
            output.write(pageName + ":\n")
            for link in linkList:
                if link:
                    output.write(link + "\n")
            output.write("\n")
        output.close()
        

# Take input from command line
if len(sys.argv) < 2:
    print("Usage:", sys.argv[0], "<url> [iteration_depth]", file=sys.stderr)
    sys.exit(1)

# Check that the given url is valid
if validators.url(sys.argv[1]):
    # Check for a given search depth and pass it if given
    if len(sys.argv) > 2:
        ImageLinkCrawler(sys.argv[1], sys.argv[2]).start()
    else:
        ImageLinkCrawler(sys.argv[1]).start()
else:
    print("Please provide a valid url")
    sys.exit(2)
