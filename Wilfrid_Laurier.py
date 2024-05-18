import requests
#from bs4 import BeautifulSoup
from selenium.common import StaleElementReferenceException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import time
import pandas as pd
import requests
from lxml import html
from concurrent.futures import ThreadPoolExecutor

def check_existing():
    existing_urls = []
    with open('Wilfrid_Urls.txt', 'r') as file:
        urls = file.readlines()
        
    for url in urls:
        try:
            response = requests.get(url.strip(), allow_redirects=False)
            if response.status_code == 200:
                status = "Working Fine"
                redirected_to = ""
            elif 300 <= response.status_code < 400:
                status = f"Redirected ({response.status_code})"
                redirected_to = response.headers.get('Location', 'Unknown')
            elif response.status_code == 403:
                status = "Access Forbidden"
                redirected_to = ""
            else:
                status = f"Returned Status Code {response.status_code}"
                redirected_to = ""
            print(f"{url.strip()}: {status}")
            existing_urls.append(url.strip())  # Append the stripped URL

        except Exception as e:
            status = f"Threw an Exception: {str(e)}"
            redirected_to = ""
            print(f"{url.strip()}: {status}")
            existing_urls.append(url.strip())  # Append the stripped URL
    
    return existing_urls

def crawl_UG():
    service = Service('chromedriver.exe')  # Replace with the path to your chromedriver executable
    driver = webdriver.Chrome(service=service)
    

    url = 'https://wlu.ca/programs/?filter=undergraduate'
    driver.get(url)
    #time.sleep(5)
    elements = driver.find_elements(By.TAG_NAME, 'a') 
    urls = []
    unique_hrefs = set()
    keywords = ['/undergraduate'] 
    for title in elements:
            try:
                href = title.get_attribute('href')
                if href and href.startswith(("https://wlu.ca/programs")):
                    if href and any(keyword in href for keyword in keywords):
                        if href not in unique_hrefs:  # Check href directly
                            unique_hrefs.add(href)  # Add href, not matching_urls
                            print(href)
                            urls.append(href)
                
            except StaleElementReferenceException:
                # If StaleElementReferenceException occurs, reattempt finding the element
                continue

    with open('Wilfrid_Urls.txt', 'w') as file:
       for url in urls:
           print(url)
           file.write(url + '\n')

def fetch(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Exception as e:
        print(f"Error fetching URL {url}: {e}")
        return None
    
def extract_information_and_export_to_excel():
    # Read the URLs from the text file
    with open('Wilfrid_Urls.txt', 'r') as file:
        urls = file.readlines()

    # Clean up URLs by removing leading/trailing whitespace and newlines
    urls = [url.strip() for url in urls]

    # Create a list to store the extracted information
    data = []

    with ThreadPoolExecutor() as executor:
        # Submit tasks for fetching URLs
        futures = [executor.submit(fetch, url) for url in urls] # type: ignore
        

        # Process results
        for future, url in zip(futures, urls):
            page_content = future.result()
            if page_content:
                # Parsing the page
                tree = html.fromstring(page_content)
                # Get elements using XPath
                names = tree.xpath('/html/body/div[1]/div[2]/div/div[2]/div/div/div/div[1]/div/div[1]/h1')
                names = [name.text.strip() for name in names if name.text.strip()]  # Remove leading/trailing whitespace
                name = names[0] if names else ""  # If there are multiple names, take the first one
                course_summary_elements = tree.xpath('/html/body/div[1]/div[2]/div/div[2]/div/div/div/div[1]/div/div[3]/p[1]')
                course_summary = course_summary_elements[0].text_content().strip() if course_summary_elements else ""
                # Append the extracted information to the list
                data.append([url,name, course_summary])

    # Export the list to an Excel file
    df = pd.DataFrame(data, columns=['URL','Name', 'Course Summary'])
    print(df)
    #df.to_excel('extracted_datayoungUG.xlsx', index=False)

    return df

def english_language():
    service = Service('geckodriver.exe')
    driver = webdriver.Firefox()
    url = 'https://wlu.ca/future-students/undergraduate/admissions/requirements/english-proficiency.html'
    driver.get(url)

    selectors = {
    'CAE': '/html/body/div[2]/div[1]/div[1]/div[3]/div[2]/div/div[1]/table/tbody/tr[2]/td[2]/p',
    'Doulingo': '/html/body/div[2]/div[1]/div[1]/div[3]/div[2]/div/div[1]/table/tbody/tr[4]/td[2]/p',
    'IELTS': '/html/body/div[2]/div[1]/div[1]/div[3]/div[2]/div/div[1]/table/tbody/tr[5]/td[2]/p/text()',
    'PTE': '/html/body/div[2]/div[1]/div[1]/div[3]/div[2]/div/div[1]/table/tbody/tr[6]/td[2]/p',
    'TOEFL':'/html/body/div[2]/div[1]/div[1]/div[3]/div[2]/div/div[1]/table/tbody/tr[7]/td[2]/p[1]/text()',
    'TOEFL PB': '/html/body/div[2]/div[1]/div[1]/div[3]/div[2]/div/div[1]/table/tbody/tr[7]/td[2]/p[2]'
    }
    data_row = [url]
    for element_name, selector in selectors.items():
    # Extract the text content under the specified selector
        try:
        # Execute JavaScript code to extract data under the specified selector
            script = f"""
            const element = document.evaluate('{selector}', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            // Extract the text content from the element under the specified selector
            const extractedData = element ? element.textContent.trim() : "";
            return extractedData;
        """
            data = driver.execute_script(script)
            print(f"{element_name}: {data}")
        except Exception as e:
            print(f"Error extracting {element_name}: {e}")
        

    driver.quit()
english_language()