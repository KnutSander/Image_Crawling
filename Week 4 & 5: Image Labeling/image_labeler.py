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
           "stop",
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

    def __init__(self, urls):
        "Initialises the class variables"
        # Initalise elasticsearch
        self.elastic = Elasticsearch("http://localhost:9200")
        self.elastic.indices.delete("articles")
        self.elastic.indices.create("articles", body)

        # The links to explore
        self.urls = urls

        # The dictonary of all the pictures and related info
        self.img_data = {}


    def get_content(self, url):
        "Gets the main content of the given page"
        html = requests.get(url).text
        soup = bs(html, 'html.parser')
        return soup.find(id='frameInner')


    def get_images(self, soup):
        "Gets all the image urls from the webpage"
        
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
            

    def get_text(self, soup):
        "Gets the article text of from the webpage"
        
        # Get all the text of the article
        p_tags = soup.find_all('p')

        # Remove the 'p' tags from the strings
        text = []
        for elem in p_tags:
            text.append(elem.get_text())

        return text


    def format_text(self, text):
        "Formats the inout text to be uploaded to Elasticsearch"
        data = ''

        id_num = 1
        for line in text:
            index_id = {'index': {'_id': str(id_num)}}
            entry = {'content': line}
            data += json.dumps(index_id) + "\n" + json.dumps(entry) + "\n"
            id_num += 1

        return data
            
        
    def analyse_data(self, data):
        """ 
        Analyse the text to return the three most common 
        words that will be used to describe the image.
        """
        
        # Delete the previous article content
        self.elastic.delete_by_query('articles', delete)

        # Post the data to elasticsearch, waiting for it to finish before proceeding
        self.elastic.bulk(data, "articles", "content", refresh="wait_for")

        # Run the search and look at the aggregations
        output = self.elastic.search(search, "articles")
        aggs = []

        # Get the three mosy common words from the aggregation
        for i in range(0, 3):
            word = output['aggregations']['content']['buckets'][i]['key']
            aggs.append(word)

        return aggs


    def output_result(self):
        "Outputs the result into a csv file"

        # Define the field names
        fieldnames = ['descriptors', 'image links', 'article name', 'article link']

        # Open a cv file that will contain the results
        with open('result.csv', 'w') as f:
            
            # Initalise csv writer
            writer = csv.writer(f)

            # Iterate through every topic in the dictonary
            for topic, data in self.img_data.items():
                writer.writerow([topic])
                writer.writerow(fieldnames)
                writer.writerows(data)
                writer.writerow([""])
            

    def crawl(self):
        "Main crawling method"

        depth = 0
        
        while depth < 10:
            url = self.urls.pop(0)
            soup = self.get_content(url)

            images = self.get_images(soup)
            text = self.get_text(soup)
            data = self.format_text(text)
            terms = self.analyse_data(data)

            if "test" in self.img_data:
                self.img_data["test"].append([terms, images, "", url])
            else:
                self.img_data["test"] = [[terms, images, "", url]]

            depth += 1

        self.output_result()
                                
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

#-------------------------------------------------------------------------------
# End of image_labeler.py
#-------------------------------------------------------------------------------
