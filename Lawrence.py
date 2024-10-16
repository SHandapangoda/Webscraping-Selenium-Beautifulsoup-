from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

def get_url_ug():
    driver = webdriver.Firefox()
    urls = ['https://www.stlawrencecollege.ca/programs?intl=true', 'https://www.stlawrencecollege.ca/programs?p=2&intl=true','https://www.stlawrencecollege.ca/programs?p=3&intl=true','https://www.stlawrencecollege.ca/programs?p=4&intl=true','https://www.stlawrencecollege.ca/programs?p=5&intl=true']

    for url in urls:
        keywords = "https://www.stlawrencecollege.ca/programs/"
        not_key="https://www.stlawrencecollege.ca/programs/areas-of-study/"
        driver.get(url)
        time.sleep(5)
        anchors = driver.find_elements(By.TAG_NAME, 'a')
        for anchor in anchors:
            href = anchor.get_attribute('href')
            if href and href.startswith(keywords) and not href.startswith(not_key):
                    print(href)
    driver.close()

def get_details():
    with open("url.txt", "r") as file:
        urls = [line.strip() for line in file.readlines()]
    data = []
    for url in urls:
        try:
            req = requests.get(url)
            req.raise_for_status()  # Raises an error for bad responses (4xx or 5xx)
            soup = BeautifulSoup(req.text, 'html.parser')

            name = soup.find_all('h1')
            details = soup.find_all("span", class_='value')

            # Check if the expected elements exist
            if name and len(details) > 5:
                data.append({
                    'URL': url,
                    'Name': name[0].get_text(),
                    'award': details[2].get_text(),
                    'code': details[0].get_text(),
                    'start': details[1].get_text(),
                    'location': details[3].get_text(),
                    'duration': details[4].get_text(),
                    'mode': details[5].get_text()
                })
            else:
                print(f"Missing data for URL: {url}")

        except Exception as e:
            print(f"Error processing {url}: {e}")
    df = pd.DataFrame(data)
    df.to_excel('lawrence.xlsx')
    print(df)
get_details()    