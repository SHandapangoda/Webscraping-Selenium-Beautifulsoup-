
import time
from datetime import date
from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from lxml import html
import requests
from bs4 import BeautifulSoup
def crawl():
    # Set up Chrome driver service
    service = Service('chromedriver.exe')  # Replace with the path to your chromedriver executable
    driver = webdriver.Chrome(service=service)

# Define the mother URL
    mother_url = 'https://www.nyit.edu/degrees'

# Define the keywords
    keywords = ['minor', 'certficate','advanced_certificate']  # Replace with your desired keywords
    keywords_exc = ['index', '#', '.pcf','career.php']

# Open the mother URL
    driver.get(mother_url)

# Introduce a delay to wait for the page to load
    time.sleep(5)  # Adjust the delay time as needed

# Find all anchor elements
    anchors = driver.find_elements(By.TAG_NAME, 'a')

# Extract URLs containing the keywords
    matching_urls = []
    unique_hrefs = set()
    for anchor in anchors:
        try:
            href = anchor.get_attribute('href')
            if href and href.startswith(("https://www.nyit.edu/degrees/")):
                if href and not(any(keyword in href for keyword in keywords)):
                    if href not in unique_hrefs:  # Check href directly
                        unique_hrefs.add(href)  # Add href, not matching_urls
                        print(href)
        except StaleElementReferenceException:
        # If StaleElementReferenceException occurs, reattempt finding the element
            continue

    for url in matching_urls:
        print(url)

crawl()