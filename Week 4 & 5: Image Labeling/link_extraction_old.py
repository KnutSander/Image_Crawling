#!usr/bin/env python3

"""
Exports page links from The Independent archive
Only links related to either Tech or Science
"""

#-------------------------------------------------------------------------------
# Imports and Global Variables
#-------------------------------------------------------------------------------

# Standard imports
import sys, requests, validators, time, csv

# BeautifulSoup
from bs4 import BeautifulSoup as bs

# Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.action_chains import ActionChains

# Webdriver Manager
from webdriver_manager.firefox import GeckoDriverManager

# Main url
main_url = "https://www.independent.co.uk/archive"


#-------------------------------------------------------------------------------
# Main Program
#-------------------------------------------------------------------------------

# Initialise driver for selenium
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

# Get the archive page
driver.get("https://www.independent.co.uk/archive")

# Need to wait for the frame to load, test to make sure this enough
# Better way to do this https://stackoverflow.com/questions/26566799/wait-until-page-is-loaded-with-selenium-webdriver-for-python
time.sleep(3)

# Switch to pivacy frame
driver.switch_to.frame('sp_message_iframe_598404')

# Find the buttons and assign the ACCEPT button
buttons = driver.find_elements(By.TAG_NAME, 'button')
button = None
for b in buttons:
    if b.get_attribute('title') == 'AGREE':
        button = b
        break

# Click the accept button
actions = ActionChains(driver)
actions.click(button)
actions.perform()

# Return to the main content frame
driver.switch_to.default_content()

# Open every year, extract the links and get the links within them that are
# related to tech and science

#driver.close()
#-------------------------------------------------------------------------------
# End of "Program name"
#-------------------------------------------------------------------------------
