# Web Crawling Work
This is a repository of web crawling work undertaken while working with Dr. Shoaib Jameel and Senior Data Scientist Mozhgan Talebpour.
The main aim of the work is to try to use web crawling to get images and label them. To achieve this, several different approaches was tested, all of which are explained below.
The work was undertaken in a 10 week period in colaboration with the Frontrunners program at the University of Essex,
All work is of my own creation, any code or concepts taken or adapted from anywhere is aknowledged.



## Image Crawling
Week 1 and 2 was a mixture of work and obligatory meetings, which is the reason there was little development done in the first two weeks. It was a also a period with a lot of exploring and understanding of several of the packages and concepts used for web crawling in Python.

The resulting products were the following:
* *beautifulSoup_test.py* - A test class to understand how Beautiful Soup works.
* *getImages.py* - A class that takes a link as an argument, and outputs a list of images links and alternative text.
* *iterativeGetImages.py* - A class that does what the class mentioned above does, as well as finding links on the given page and exploring connected pages iterativly until a given number of pages has been searched.

### Folder Contents
* beautifulSoup_test.py
* getImages.py
* iterativeGetImages.py
* imageLinks.txt
* singleOutput.txt
* output.txt
* README.md



## Topic Searching
In week 3 the goal was to crawl a specific topic, the topic chosen being sports, then trying to label which sport the picture is of. Doing this on The Independet was relativly successful as most of there pages has the type of sport in the URL, so it was a simple operation of extracting it from there.

The resulting product was *sportPictureLabeling.py* a class that starts crawling on the main sports page on The Independent, crawls through articles iterativly until a given depth, and finally output a CSV file where the alt-text and images links are grouped and labeled based on the sport.

### Folder Contents
* sportPictureLabeling.py
* result.csv
* README.md



## Image Labeling
In week 4 and 5, the topic was changed into technlogy and science as too many people were working on sport related content. The use of Elasticsearch to label the images was fairly successful, and provided a basis of which to continue to build on.

The resulting products were the following:
* *link_extraction_old,py* - A class that was abandoned as the use of Selenium was unnecessary.
* *link_extraction.py* - A class that extracts links related to the given topic from The Independet archive until a given depth/number of days, then outputting them to a CSV file.
* *image_labeler.py* - A class that extracts the links from the output of *link_extraction.py*, gets the images from the webpage and labels them given the three most common words in the article content, finally outputting it to a CSV file.
* *independent_crawler.py* - A class that combines the functionality of the two previous files with subtile changes and additions to several methods, and an improved output where the image labels, image links, article text and article link are display and ordered based on their topic.

### Folder Contents
* link_extraction_old.py
* link_extraction.py
* image_labeler.py
* independent_crawler.py
* links.csv
* result.csv
* science_and_tech_result.csv
* README.md



## Folder Name
Text explaining briefly what was done in the week;

The resulting product/s:

### Folder Contents
*
