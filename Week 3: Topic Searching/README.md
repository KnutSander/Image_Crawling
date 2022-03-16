## Topic Searching
In week 3 the goal was to crawl a specific topic, the topic chosen being sports, then trying to label which sport the picture is of. Doing this on The Independet was relativly successful as most of there pages has the type of sport in the URL, so it was a simple operation of extracting it from there.

The resulting product was *sportPictureLabeling.py* a class that starts crawling on the main sports page on The Independent, crawls through articles iterativly until a given depth, and finally output a CSV file where the alt-text and images links are grouped and labeled based on the sport.

### Folder Contents
* sportPictureLabeling.py
* result.csv
* README.md
