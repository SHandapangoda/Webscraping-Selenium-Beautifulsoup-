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

def get_ref_url():
    urls = get_ref_url()
    urls = []
    '''
    # Read URLs from the file
    with open('urls.txt', 'r') as file:
        for url in file:
            urls.append(url.strip())  # Strip newline characters and add to the list
'''
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
    data = []

    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise error for bad response status

            soup = BeautifulSoup(response.text, 'html.parser')
            entry = soup.find_all('div', class_='border border-solid border-color-black-10 mb-2')
            fees = soup.find_all('span', class_='c-course-overview-item__field')
            
            if fees and len(fees) >= 5:
                fees_value = fees[4].get_text().strip()
            else:
                fees_value = 'Not found'

            for div in entry:
                title = div.find('h3').text.strip()
                content_paragraphs = div.find('div', class_='wysiwyg').find_all('p')
                
                if title == 'Entry requirements':
                    content = "\n".join([paragraph.text.strip() for paragraph in content_paragraphs])
                    data.append({'URL': url, 'Fees': fees_value, 'Title': title, 'Entry': content})

        except requests.RequestException as e:
            print(f"Error fetching URL {url}: {str(e)}")

    return data

def get_details():
    urls = get_ref_url()
    data = []

    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise error for bad response status

            tree = html.fromstring(response.content)
            names = tree.xpath('/html/body/div[2]/div/div[1]/div[2]/div[1]/div[1]/div[2]/p[2]')
            starts = tree.xpath('/html/body/div[2]/div/div[1]/div[2]/div[1]/div[3]/div[2]/p[2]')

            if names:
                name = names[0].text_content().strip()
            else:
                name = 'Not found'

            if starts:
                start = starts[0].text_content().strip()
            else:
                start = 'Not found'

            data.append({'URL': url, 'Name': name, 'Start': start})

        except requests.RequestException as e:
            print(f"Error fetching URL {url}: {str(e)}")
        except Exception as e:
            print(f"Error processing URL {url}: {str(e)}")

    return data

def export_to_excel():
    # Get data from both functions
    details_main = get_details_main()
    details = get_details()

    # Convert data to DataFrames
    df_main = pd.DataFrame(details_main)
    df = pd.DataFrame(details)

    # Export DataFrames to Excel
    with pd.ExcelWriter('details.xlsx') as writer:
        df_main.to_excel(writer, sheet_name='Main Details', index=False)
        df.to_excel(writer, sheet_name='Other Details', index=False)

# Call function to export details to Excel
export_to_excel()