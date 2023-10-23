# Exploring web scraping with scrapy

This program scrapes quotes from https://quotes.toscrape.com/page/1/ and https://quotes.toscrape.com/page/2/

# Run in a python virtual environment

  - check the python documentation on how to create a virtual environment for your operating system
    
# Requirements.txt file tracks dependency versions

  - install requirements.txt with " pip install -r requirements.txt "

# Sample output
quotes.json 

# Commands
scrapy crawl ["spider name"] -O ["output_file_name"].json  

  - Runs ["spider_name"] that scrapes the page in the spider
    
  - outputs result in a json file named ["output_file_name"].json


