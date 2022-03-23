#!usr/bin/env python3

"""
" A class to test the speed of which various methods used
" in improved_independent_crawler.py takes.
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
    "number_of_shards": 1,
    "analysis": {
      "analyzer": {
        "content_anal": {
          "type": "custom",
          "tokenizer": "whitespace",
          "filter": [
            "lowercase",
            "custom_stop",
            "apostrophe"
          ]
        }
      },
      "filter": {
        "custom_stop": {
          "type": "stop",
          "stopwords": ["_english_", "you", "from", "have", "can", "been",
                        "were", "has", "your", "its", "than"]
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


# Important urls
start_url = "https://www.independent.co.uk/archive"
base_url = "https://www.independent.co.uk"

# Topics to be found
topics = ["/tech/", "/life-style/gadgets-and-tech/", "/news/science/"]

# Max depth for searching for relevant links
MAX_DEPTH = 3

#-------------------------------------------------------------------------------
# Classes and Methods
#-------------------------------------------------------------------------------


class Independent_Crawler:
    "A class created to crawl The Independent"

    
    def __init__(self):
        "Initialises the class variables"

        # List of date urls to visit and relevant articles
        self.date_urls = []
        self.rel_urls = []

        # Initalise elasticsearch
        self.elastic = Elasticsearch("http://localhost:9200")
        self.elastic.indices.delete("articles")
        self.elastic.indices.create("articles", body)

        # The dictonary of all the pictures and related info
        self.img_data = {}

        

    def get_content(self, url):
        "Gets the main content of the given page"

        # Retrieve page html, then turn it into soup and extract the frameInner
        # frameInner is the main content of any page from The Independet
        html = requests.get(url).text
        soup = bs(html, 'html.parser')
        return soup.find(id='frameInner')


    
    def get_links(self, soup):
        "Gets all links within a given soup"

        # Retrieve the links form the soup
        link_objs = soup.find_all('a')

        # All the urls on the archive page leads to different dates
        # Add them all to the list after making them into valid links
        for obj in link_objs:
            self.date_urls.append(base_url + obj.get('href'))


            
    def get_rel_links(self, soup):
        "Gets links that are relevant to the defined topics"

        # Retrieve the links from the soup
        link_objs = soup.find_all('a')
        
        for obj in link_objs:

            # Get the link
            href = obj.get('href')

            # Check if the link is relevant using the defined topics
            # Also save what topic it belongs to
            link_relevant = False
            for topic in topics:
                if topic in href:
                    link_relevant = True
                    this_topic = topic
                    break

            # If it isn't relevant the loop moves on to another link
            if not link_relevant:
                continue

            # Link is relevant, add the topic and the link to the list
            self.rel_urls.append([topic, base_url + href])

            

    def get_images(self, soup):
        "Gets all the image urls from the webpage"
        
        # Get all images on the page
        all_images = soup.find_all(['img', 'amp-img'])

        # List of image urls and alt texts
        im_urls = []
        alt_texts = []
        
        for image in all_images:

            # Images with links as parents link to other pages, so disregard them
            link_parent = image.find_parent('a')
            if link_parent == None:

                # Make sure the src link is a valid web link
                src = image.get('src')
                if "http" in src:

                    # Add the url to the list
                    im_urls.append(src)

                    # Get the alt text of the image
                    alt = image.get('alt')

                    # Only process the alt if it exists
                    if alt is not None:

                        # Remove the "<p>" tags if they exists before adding them
                        alt.replace("<p>", "")
                        alt_texts.append(alt)
                    
        # Both im_urls and alt_text currently hold several duplicate values
        # These need to be removed before the results are returned by the method

        # To remove duplicate images, find the url stems and remove duplicates
        # Temporary list to contain the stems
        stems = []

        # Run through the image urls and extract the stems
        for url in im_urls:

            # Split the url on "?" to get only the image link
            split = url.split("?")
            stems.append(split[0])

        # To remove the duplicates, turn the list into a dictonary and then
        # back to a list again
        im_urls = list(dict.fromkeys(stems))

        # Convert to string for better formating
        im_urls = ", ".join(im_urls)

        # Perform the same operation to remove duplicate alt text
        alt_texts = list(dict.fromkeys(alt_texts))

        return im_urls, alt_texts

    

    def get_text(self, soup):
        "Gets the article text and title of from the webpage"
        
        # Get all the text of the article
        p_tags = soup.find_all('p')

        # Remove the 'p' tags from the strings
        text = []
        for elem in p_tags:
            text.append(elem.get_text())

        # Get the title to be used later, also add it to the text list
        title = soup.find('h1')
        title = title.get_text()
        text.append(title)

        # Get the subtitle as well
        sub = soup.find('h2')
        text.append(sub.get_text())

        return text, title


    
    def format_text(self, text):
        "Formats the input text to be uploaded to Elasticsearch"

        # Empty string to hold the JSON data
        data = ''

        # Id number incremented for every line
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
        # Aggregations summarises data as metrics, statistics or other analytics
        output = self.elastic.search(search, "articles")
        aggs = []

        # Get the three mosy common words from the aggregation
        for i in range(0, 3):
            word = output['aggregations']['content']['buckets'][i]['key']
            aggs.append(word)

        # Make into a string for better formatting
        aggs = ", ".join(aggs)

        return aggs


    
    def output_result(self):
        "Outputs the result into a csv file"

        # Define the field names
        fieldnames = ['descriptors', 'image links', 'article name', 'article link']

        # Open a cv file that will contain the results
        with open('tech_and_science_result.csv', 'w') as f:
            
            # Initalise csv writer
            writer = csv.writer(f)

            # Iterate through every topic in the dictonary
            for topic, data in self.img_data.items():

                # Start by writing the topic
                writer.writerow([topic])

                # Add the field names
                writer.writerow(fieldnames)

                # Write out every entry in the list of lists
                writer.writerows(data)

                # Blank line to seperate the different topics
                writer.writerow([""])


#-------------------------------------------------------------------------------
# Main Program
#-------------------------------------------------------------------------------

# Initialise the class
crawler = Independent_Crawler()

# Measure the time it takes to extract links, used to get every date link
# Takes on average 0.9 seconds from testing
start = time.time()

soup = crawler.get_content(start_url)
crawler.get_links(soup)

#end = time.time()

#print("Time taken to extraxt date links was " + str(end-start) + " seconds.")

# Measure the time it takes to extract relevant links from a date page
# Takes on average 0.5 seconds from testing
#start = time.time()

url = crawler.date_urls.pop(10)
soup = crawler.get_content(url)
crawler.get_rel_links(soup)

#end = time.time()

#print("Time taken to extract relevant links was " + str(end-start) + " seconds.")

# Prepare the content for the next operations
item = crawler.rel_urls.pop(0)
topic, url = item[0], item[1]
soup = crawler.get_content(url)

# Measure the time taken to extract the image links from an article
# Takes on average 0.002 seconds from testing
#start = time.time()

images, alt = crawler.get_images(soup)

#end = time.time()

#print("Time taken to extract image links was " + str(end-start) + " seconds.")

# Measure time taken to extract the article content
# Takes on average 0.003 seconds on average
#start = time.time()

text, title = crawler.get_text(soup)

#end = time.time()

#print("Time taken to extract the text was " + str(end-start) + " seconds.")

# Measure time taken to format the text
# Takes on average 0.002 seconds on average
text = text + alt

#start = time.time()

data = crawler.format_text(text)

#end = time.time()

print("Time taken to format the text was " + str(end-start) + " seconds.")

# Measure time taken to analyse the text and get the image labels
# Takes on average 0.7 seconds on average
#start = time.time()

terms = crawler.analyse_data(data)

end = time.time()

print("Time taken to analyse the data and return the terms was "
      + str(end-start) + " seconds.")

# If operations were run in this order for every link, it would take the program
# on average 2.5 seconds to extract and label the images


#-------------------------------------------------------------------------------
# End of operation_speed.py
#-------------------------------------------------------------------------------
