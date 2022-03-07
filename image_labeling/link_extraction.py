#!usr/bin/env python3

"""
Exports page links from The Independent archive
The link category can be specified by altering
"""

#-------------------------------------------------------------------------------
# Imports and Global Variables
#-------------------------------------------------------------------------------

# Standard imports
import requests, time, csv

# BeautifulSoup
from bs4 import BeautifulSoup as bs

# Important urls
start_url = "https://www.independent.co.uk/archive"
base_url = "https://www.independent.co.uk"

# Topics to be found
topics = ["news/science", "tech/", "life-style/gadgets-and-tech"]

#-------------------------------------------------------------------------------
# Class and Routines
#-------------------------------------------------------------------------------

# Class that extracts links from The Independent archive
class LinkExtractor:

    def __init__(self):
        # List of date urls to visit and relevant articles
        self.date_urls = []
        self.rel_urls = []


    # Gets the main content of the given page
    def get_content(self, url):
        html = requests.get(url).text
        soup = bs(html, 'html.parser')
        return soup.find(id='frameInner')


    # Gets all links in the given soup
    # Used on the main archive page to get date links
    def get_links(self, soup):
        link_objs = soup.find_all('a')
        for obj in link_objs:
            self.date_urls.append(base_url + obj.get('href'))


    # Returns links that are relevant to the topics
    # sepecefied in the topics list
    def get_rel_links(self, soup):
        link_objs = soup.find_all('a')
        for obj in link_objs:
                                
            href = obj.get('href')

            # Check if the link is on a relevant topic
            link_relevant = False
            for topic in topics:
                if topic in href:
                    link_relevant = True
                    break

            # If it isn't relevant the loop moves on to another link
            if not link_relevant:
                continue

            # Link is relevant, add it to the list
            self.rel_urls.append(base_url + href)


    # Main crawling method
    def crawl(self):
        
        # Get the links from the starting page
        main_soup = self.get_content(start_url)
        self.get_links(main_soup)

        # Depth limit and count
        max_depth = 31
        cur_depth = 0

        # Start extracting relevant links
        while self.date_urls:
            print("Search depth " + str(cur_depth))

            url = self.date_urls.pop(0)
            soup = self.get_content(url)
            self.get_rel_links(soup)

            cur_depth += 1
            if cur_depth == max_depth:
                break
            
            # Sleep to avoid aggressive crawling
            time.sleep(0.5)

        self.output()


    # Outputs the results into a csv
    def output(self):
        with open('links.csv', 'w') as f:
            for url in self.rel_urls:
                f.write(url + "\n")

                                  
#-------------------------------------------------------------------------------
# Main Program
#-------------------------------------------------------------------------------

LinkExtractor().crawl()

#-------------------------------------------------------------------------------
# End of link_extraction.py
#-------------------------------------------------------------------------------
