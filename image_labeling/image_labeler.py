#!usr/bin/env python3

"""
Opens webpages and extracts image links from them.
Then labels tham using the most common words in the article.
"""

#-------------------------------------------------------------------------------
# Imports and Global Variables
#-------------------------------------------------------------------------------

# Standard imports
import requests, time, csv, json

# BeautifulSoup, html handling
from bs4 import BeautifulSoup as bs

# Elasticsearch, content analysis
from elasticsearch import Elasticsearch

# Define the custom analyser and mapping for the text content
body = {
  "settings": {
    "analysis": {
      "analyzer": {
        "content_anal": {
          "type": "custom",
          "tokenizer": "lowercase",
          "filter": [
            "stop"
          ]
        }
      }
    }
  }, 
  "mappings": {
    "content": {
      "properties": {
        "content": {
          "type": "text",
          "analyzer": "content_anal",
          "fielddata": "true",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        }
      }   
    }
  }
}

# The search that gets the most common words
search = {
  "query": {
    "match_all": {}
  },
  "aggs": {
    "content": {
      "terms": {
        "field": "content"
      }
    }
  }
}

# The delete query sent to clear the previous article data
delete = {
  "query": {
    "match_all": {}
  }
}

#-------------------------------------------------------------------------------
# Class and Routines
#-------------------------------------------------------------------------------

# Class that labels images
class ImageLabeler:

    # Initialises the class variables
    def __init__(self, urls):
        # Initalise elasticsearch
        self.elastic = Elasticsearch("http://localhost:9200")
        self.elastic.indices.create("articles", body)

        # The links to explore
        self.urls = urls


    # Gets the main content of the given page
    def get_content(self, url):
        html = requests.get(url).text
        soup = bs(html, 'html.parser')
        return soup.find(id='frameInner')


    # Gets the image urls from the webpage
    def get_images(self, soup):
        # Get all images on the page
        all_images = soup.find_all(['img', 'amp-img'])
        
        # Remove images with links as a parent
        # Removes article link images that have nothing to do with the images
        # Place the relevant image links into a 
        # Seems to work reasonably well
        im_urls = []
        for image in all_images:
            link_parent = image.find_parent('a')
            if link_parent == None:
                im_urls.append(image.get('src'))

        return im_urls
            

    # Gets the article text content from the webpage
    def get_text(self, soup):
        # Get all the text of the article
        p_tags = soup.find_all('p')

        # Remove the 'p' tags from the strings
        text = []
        for elem in p_tags:
            text.append(elem.get_text())

        return text


    # Formats the input text to be uploaded to Elasticsearch
    def format_text(self, text):
        data = ''

        id_num = 1
        for line in text:
            index_id = {'index': {'_id': str(id_num)}}
            entry = {'content': line}
            data += json.dumps(index_id) + "\n" + json.dumps(entry) + "\n"
            id_num += 1

        return data
            
        
    
    # Analyse the text to return the three most common words
    # that will be used to describe the image
    def analyse_data(self, data):
        # Delete the previous article content
        self.elastic.delete_by_query('articles', delete)

        # Post the data to elasticsearch, waiting for it to finish before proceeding
        self.elastic.bulk(data, "articles", "content", refresh="wait_for")

        # Run the search and look at the aggregations
        output = self.elastic.search(search, "articles")
        aggs = []

        # Get the three mosy common words from the aggregation
        for i in range(0, 3):
            word =output['aggregations']['content']['buckets'][i]['key']
            aggs.append(word)

        return aggs
        


    # Main crawling method
    def crawl(self):
        # Loop body
        url = self.urls.pop(0)
        soup = self.get_content(url)

        images = self.get_images(soup)
        text = self.get_text(soup)
        data = self.format_text(text)
        terms = self.analyse_data(data)

        print(str(terms) + ' ' + str(images))

        
        
    
                                  
#-------------------------------------------------------------------------------
# Main Program
#-------------------------------------------------------------------------------

# Open link file and import it's data
# Better to save as a text file?
with open('links.csv', 'r') as f:
    reader = csv.reader(f)
    nested_urls = list(reader)
    urls = []
    for list_url in nested_urls:
        for url in list_url:
            urls.append(url)

ImageLabeler(urls).crawl()

# Send links to the class
# Go through every link, extracting image link and article content "<p>"
# Create a json that can be posted to Elasticsearch and return the common words
# Use the words to label the picture
# Save the picture link and word/words labeling it to a csv file

#-------------------------------------------------------------------------------
# End of image_labeler.py
#-------------------------------------------------------------------------------
