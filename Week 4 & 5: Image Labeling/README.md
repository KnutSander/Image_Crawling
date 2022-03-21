# Image Labeling
In week 4 and 5, the topic was changed into technlogy and science as too many people were working on sport related content. The use of Elasticsearch to label the images was fairly successful, and provided a basis of which to continue to build on.

The resulting products were the following:
* *link_extraction_old,py* - A class that was abandoned as the use of Selenium was unnecessary.
* *link_extraction.py* - A class that extracts links related to the given topic from The Independet archive until a given depth/number of days, then outputting them to a CSV file.
* *image_labeler.py* - A class that extracts the links from the output of *link_extraction.py*, gets the images from the webpage and labels them given the three most common words in the article content, finally outputting it to a CSV file.
* *independent_crawler.py* - A class that combines the functionality of the two previous files with subtile changes and additions to several methods, and an improved output where the image labels, image links, article text and article link are display and ordered based on their topic.
