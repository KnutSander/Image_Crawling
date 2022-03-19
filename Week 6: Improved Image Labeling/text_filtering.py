#!usr/bin/env python3

"""
" A program to test and explore different ways to filter and export the text
" of articles on The Independent to label the images on them
"""

#-------------------------------------------------------------------------------
# Imports and Global Variables
#-------------------------------------------------------------------------------

# Standard imports
import sys, requests, time, csv, json, validators

# BeautifulSoup, html handling
from bs4 import BeautifulSoup as bs

# Elasticsearch, content analysis
from elasticsearch import Elasticsearch

# Match all query for getting all elements as well as deleting the content
match_all = {
  "query": {
    "match_all": {}
  }
}

# Initalise Elasticsearch
elastic = Elasticsearch("http://localhost:9200")

#-------------------------------------------------------------------------------
# Classes and Methods
#-------------------------------------------------------------------------------


def extract_text(url):
    "Gets the article text"

    # Extract the html of the given url
    html = requests.get(url).text

    # Make the html into soup
    soup = bs(html, 'html.parser')

    # Extract the 'frameInner', article main content
    soup = soup.find(id='frameInner')

    # Extract the main content from the soup
    main = soup.find(id='main')
        
    # Get all the text of the article
    p_tags = main.find_all('p')

    # Remove the 'p' tags from the strings and add them to the list
    text = []
    for elem in p_tags:
        text.append(elem.get_text())

    # Get the title as it has useful text as well
    title = soup.find('h1')
    title = title.get_text()

    # Get the subtitle as well
    sub = soup.find('h2')
    sub = sub.get_text()

    # Add title and subtitle to the text list
    text.append(title)
    text.append(sub)

    return text



def format_data(text):
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



def send_data(data):
    "Sends the data to Elasticsearch"
    
    # Delete the previous article content
    elastic.delete_by_query('articles', match_all)

    # Post the data to elasticsearch, waiting for it to finish before proceeding
    elastic.bulk(data, 'articles', 'content', refresh='wait_for')

    # Query the data for the results
    output = elastic.search(match_all, 'articles')

    print(output)


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

# Remove the index if it exists, then re-create it with the settings
#elastic.indices.delete("articles")
#elastic.indices.create("articles", body)

# Retrieve the text content of the page
text = extract_text(sys.argv[1])

# Format the text for input
data = format_data(text)

# Send the data to Elasticsearch
send_data(data)

#-------------------------------------------------------------------------------
# End of text_filtering.py
#-------------------------------------------------------------------------------
