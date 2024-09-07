from matplotlib.pyplot import get
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
from lxml import html
import json
# Initialize Chrome driver
def get_url():
    driver = webdriver.Firefox()
    url = 'https://warwick.ac.uk/study/undergraduate/courses/'
    matching_urls = []
    keywords = ["/study/undergraduate/"]
    
        # Open the mother URL
    driver.get(url)
    time.sleep(10)
        # Find all anchor elements
    anchors = driver.find_elements(By.TAG_NAME, 'a')
        # Extract URLs containing the keywords
    for anchor in anchors:
        href = anchor.get_attribute('href')
        if href and any(keyword in href for keyword in keywords):
            matching_urls.append(href)
                # print(href)
    matching_urls = list(set(matching_urls))
    # saving the extracted URLs from OIEG Site

    ''''
    with open('oieglinks08-05.txt', 'w') as file:
        for url in matching_urls:
            file.write(f"{url}\n")
    '''
    driver.close()
    return matching_urls

def get_pg_url():
    driver = webdriver.Firefox()
    url = 'https://warwick.ac.uk/study/postgraduate/courses/'
    matching_urls = []
    keywords = ["/study/postgraduate/"]
    
        # Open the mother URL
    driver.get(url)
    time.sleep(10)
        # Find all anchor elements
    anchors = driver.find_elements(By.TAG_NAME, 'a')
        # Extract URLs containing the keywords
    for anchor in anchors:
        href = anchor.get_attribute('href')
        if href and any(keyword in href for keyword in keywords):
            matching_urls.append(href)
                # print(href)
    matching_urls = list(set(matching_urls))
    driver.close()
    return matching_urls

def get_content():
    data = []
    with open('urls.txt', 'r') as file:
        urls = file.readlines()

    for url in urls:
       
        req = requests.get(url)
        if req.status_code == 200:
            soup = BeautifulSoup(req.text, 'html.parser')

            name = soup.find_all("h1")
            code = soup.find_all("div", class_='info-content')
            starts = soup.find_all('div',class_='info-content')
            duration = soup.find_all("div", class_='info-content')
        #nfq = soup.find_all("span", class_='course-property-value')
            data.append([url, name[1].get_text(), code[0].get_text(), starts[1].get_text(),duration[2].get_text(),starts[1].get_text()])
            print(name[1].get_text())
            print("Code:", code[0].get_text())
            print('Starts:',starts[1].get_text())
            print("Duration:", duration[2].get_text())
        #print("NFQ Level:", nfq[0].get_text())
    df = pd.DataFrame(data, columns=["url","name", "code","duration","starts"])
    print(df)
    #df.to_excel('extracted_london_masters.xlsx', index=False)
get_content()