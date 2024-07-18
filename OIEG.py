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
# Initialize Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def get_ref_url():
    urls = []
    
    # Read URLs from the file
    with open('urls.txt', 'r') as file:
        for url in file:
            urls.append(url.strip())  # Strip newline characters and add to the list

    matching_urls = []
    keywords = ["https://www.ravensbourne.ac.uk"]

    for url in urls:
        try:
            # Open the URL in the driver
            driver.get(url)
            time.sleep(5)  # Introducing a delay to ensure the page loads completely

            # Find all anchor elements on the page
            anchors = driver.find_elements(By.TAG_NAME, 'a')

            # Extract URLs containing the keywords
            for anchor in anchors:
                href = anchor.get_attribute('href')
                if href and any(keyword in href for keyword in keywords):

                    matching_urls.append(href)

        except Exception as e:
            print(f"Error processing URL {url}: {str(e)}")

    matching_urls = list(set(matching_urls))  
    #print(matching_urls)
    return matching_urls

def get_details_main():
    urls = get_ref_url()
    
    for url in urls:
        try:
            response = requests.get(url)
            # Handle response as needed
            soup = BeautifulSoup(response.text, 'html.parser')
            Entry = soup.find_all('div', class_='border border-solid border-color-black-10 mb-2')
            fees = soup.find_all('span', class_='c-course-overview-item__field')
            fees = fees[4].get_text()
            for div in Entry:
                title = div.find('h3').text.strip()
                content_paragraphs = div.find('div', class_='wysiwyg').find_all('p')
                if title == 'Entry requirements':
                    print(f'URL: {url}' )
                    print(f'fees: {fees}')
                    print(f"Title: {title}")
                    print("Content:")
                    for paragraph in content_paragraphs:
                        print(paragraph.text.strip())
                    print("\n")
            #print(f"Request to {url} successful: {response.status_code} Entry: {Entry[1].get_text()}")
            
            # Example: Parse content if needed
            # print(response.content)

        except requests.RequestException as e:
            print(f"Error fetching URL {url}: {str(e)}")

def get_details():
    urls = []
        # Read URLs from the file
    with open('urls.txt', 'r') as file:
        for url in file:
            urls.append(url.strip())

    data = []
    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise error for bad response status

            tree = html.fromstring(response.content)
            names = tree.xpath('/html/body/div[2]/div/div[1]/div[2]/div[1]/div[1]/div[2]/p[2]')

            if names:
                for name in names:
                    name.text_content().strip()
            else:
                print(f"No matching elements found for URL: {url}")
            # Example XPath query to find multiple elements
            starts = tree.xpath('/html/body/div[2]/div/div[1]/div[2]/div[1]/div[3]/div[2]/p[2]')
            
            if starts:
                for start in starts:
                    start.text_content().strip()
            else:
                print(f"No matching elements found for URL: {url}")
            
            data.append({'url': url,'name': name.text_content().strip(), 'start': start.text_content().strip()})
        except requests.RequestException as e:
            print(f"Error fetching URL {url}: {str(e)}")
        except Exception as e:
            print(f"Error processing URL {url}: {str(e)}")

    df = pd.DataFrame(data)
    print(df)


    
def get_url():
    mother_url = ["https://www.oxfordinternational.com/search?universities%5B%5D=5569&search=&study_levels%5B%5D=611&page=1"]
    matching_urls = []
    keywords = ["https://www.oxfordinternational.com/degrees/"]
    for url in mother_url:
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
                #print(href)
    matching_urls = list(set(matching_urls))
    print(matching_urls)
    return matching_urls

get_details()