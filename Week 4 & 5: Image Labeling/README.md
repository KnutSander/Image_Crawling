# Image_Labeling
The aim of this is to search through The Independent technology and science related news, and try to label the images in each article
Here I will attempt to label images based on the most common word in the article, after formatting and processing it through Elasticsearch.

## Link_Extraction
Extracts links from the independent archive related to the given topics.

## Image_Labeler
Using the links from link_extraction.py, it explores the articles, gets the images and article text, and uses the most common words to label the picture.

## Independent_Crawler
Combines the two Python files mentioned above into one, as well as doing some improvments to the code.
It searches for links relevant to the given topics, then extracts the articles images and text. 
It then uses Elasticsearch and custom analyser to find the three most common words, and uses those to label the images.
This is all nicely formatted and output into a CSV file.
