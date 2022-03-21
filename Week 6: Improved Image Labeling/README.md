# Improved Image Labeling
In week 6 the goal was to further refine what was developed in week 4 and 5. This was accomplished by looking further into what text and images were extracted from the page, and then filtering out any that were not relevant.  
The extracted text contained a lot of pieces that were unrelated to the actual article, advertising for The Independnt news letter, the users bookmarks and more. To deal with this, only content from the "main" div was extracted, as well as including the title and subtitle of the article and image alt text.  
The extracted images contained duplicate images with different sizes and quality. To deal with this, all image links are stripped down to their stem and then duplicate links are removed, leaving only unique image links.  
The output was also improved for better readability, and the speed of various operations were tested and recorded.

The resulting products were the following:
* *text_filtering.py* - A class to test and improve the text ectracted from articles on The Independent.
* *image_filtering.py* - A class to test and improve the image links extracted from articles on The Independet.
* *operation_speed.py* - A class to test the operation speed of the methods implemented in *improved_independent_crawler.py*
* *improved_independent_crawler.py* - An improved version of *independent_crawler.py* that implements the text and image extraction from the two classes above, as well as improving the output and performance of it's predecessor.
