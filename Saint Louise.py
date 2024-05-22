
import time
from datetime import date
from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from lxml import html
import requests
from bs4 import BeautifulSoup
def crawl_ug():
    #service = Service('geckodriver.exe')
    driver = webdriver.Firefox()
    url = 'https://catalog.slu.edu/programs/#filter=.filter_4'
    driver.get(url)
    
    anchors = driver.find_elements(By.TAG_NAME, 'a')
    urls = []
    keywords = ['-ba', '-bs']
    keywords_exc = ['certificate', 'online','accelerated','ma','ms','masters','post','dual']

    for anchor in anchors:
        href = anchor.get_attribute('href')
        try:
            if href and any(keyword in href for keyword in keywords):
                if href and href.startswith(("https://catalog.slu.edu/colleges-schools")):
                    if href and not(any(keyword in href for keyword in keywords_exc)):
                        urls.append(href)
                        print(href)
        except StaleElementReferenceException:
            continue
            
    with open('saintlouiseUG.txt', 'w') as file:
        # Print the filtered URLs
        for url in urls:
            file.write(url + '\n')
    
    driver.close()

def crawl_masters():
    #service = Service('geckodriver.exe')
    driver = webdriver.Firefox()
    url = 'https://catalog.slu.edu/programs/#filter=.filter_6'
    driver.get(url)
    
    anchors = driver.find_elements(By.TAG_NAME, 'a')
    urls = []
    keywords = ['-ma', '-ms','mph','msw','macc','llm','master']
    keywords_exc = ['certificate', 'online','minor','ba','bs','cert','madrid','phd','pbc','jd']

    for anchor in anchors:
        href = anchor.get_attribute('href')
        try:
            if href and any(keyword in href for keyword in keywords):
                if href and href.startswith(("https://catalog.slu.edu/colleges-schools")):
                    if href and not(any(keyword in href for keyword in keywords_exc)):
                        urls.append(href)
                        print(href)
        except StaleElementReferenceException:
            continue
            
    with open('saintlouisenPG.txt', 'w') as file:
        # Print the filtered URLs
        for url in urls:
            file.write(url + '\n')
    
    driver.close()
crawl_masters()