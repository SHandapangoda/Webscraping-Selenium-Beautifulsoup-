from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import json
import pandas as pd
from notify_run import Notify
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import datetime

start_time = time.time()
notify = Notify()
notify.register()

with open('C:/Users/User/PycharmProjects/pythonProject/central florida.txt', 'r') as file:
    urls = file.read().splitlines()

All_urls = 0

for url in urls:
    All_urls += 1

urls = list(set(urls))


# Define attribute-value pairs for extracting text content with index
attribute_value_pairs = [
    {'class': ('file-alt', 0)},  # Course name
    {'class': ('dollar-sign', 1)}, # Fees
    {'class':('prog-entry',0)}  # Entry Requirement
    
]


# Initialize the web driver (assuming you're using ChromeDriver)
#service = Service('C:/Users/User/PycharmProjects/pythonProject/chromedriver.exe')  # Replace with the path to your chromedriver executable
driver = webdriver.Firefox()

# Create a dictionary to keep track of URL content
url_content = {}

# Load the previous data from a JSON file (if it exists)
try:
    with open('Trinity00-May20.json', 'r') as current_data_file:
        url_content = json.load(current_data_file)
except FileNotFoundError:
    pass

results = []

url_count = 0
Actual_attr_count = 0
not_found_urls = []
not_found = []

for url in urls:
    attr_count = 0
    not_found_count = 0
    url_count += 1
    print(f"Checking changes for URL: {url}")
    driver.get(url)
    if url not in url_content or not isinstance(url_content[url], dict):
        url_content[url] = {}
    for attr_value_pair in attribute_value_pairs:
        attr_count += 1
        attribute = next(iter(attr_value_pair))
        value, index = attr_value_pair[attribute]
        #print(f'value = {value}')

        try:
            elements = driver.find_elements(By.XPATH, f'//*[@{attribute}="{value}"]')
            if index < len(elements):
                element = elements[index]
                # Use BeautifulSoup to parse the HTML of the element
                soup = BeautifulSoup(element.get_attribute('outerHTML'), 'html.parser') # type: ignore
                # Extract all text from the parsed HTML
                text_content = soup.get_text(separator='\n').strip()
                if url_content[url].get(value) != text_content:
                    notify.send(f"Changes detected in URL: {url}, Attribute: {attribute}, Value: {value}")
                    print(f"Changes detected in URL: {url}, Attribute: {attribute}, Value: {value}")
                    results.append({'URL': url, 'Attribute': attribute, 'Value': value, 'Index': index, 'Change': True, 'Content': text_content})
                    Actual_attr_count += 1
                else:
                    print(f"No changes detected in URL: {url}, Attribute: {attribute}, Value: {value}")
                    results.append({'URL': url, 'Attribute': attribute, 'Value': value, 'Index': index, 'Change': False, 'Content': text_content})
                    Actual_attr_count += 1
                url_content[url][value] = text_content
            else:
                print(f"No element found at index {index} for URL: {url}, Attribute: {attribute}, Value: {value}")
                not_found.append(f'{url}, Attribute: {attribute}, Value: {value}, index {index}')
        except NoSuchElementException:
            print(f"Attribute-value pair not found for URL: {url}, Attribute: {attribute}, Value: {value}")
            not_found.append(f'{url}, Attribute: {attribute}, Value: {value}, index {index}')

not_found_urls = set(not_found_urls)
with open('NotFoundAttributes01-May20.txt', 'w') as file:
    for content in not_found:
        file.write(content + '\n')

# Save the updated data to a JSON file
with open('Trinity01-May20.json', 'w') as current_data_file:
    json.dump(url_content, current_data_file)

# Convert results to DataFrame and save to Excel
df = pd.DataFrame(results)
df.to_excel('Trinity01-May20.xlsx', index=False)

# Quit the driver
driver.quit()

print("")
print(f'No of URLS : {All_urls}')
print(f'Unique URLS : {url_count}')
expected = url_count * attr_count
print(f"Expected Attributes : {expected}")
print(f'Actual Attributes : {Actual_attr_count}')
end_time = time.time()
execution_time = (end_time - start_time) / 60
rounded_execution_time = round(execution_time, 2)

print('')

print("Start Time : ", datetime.datetime.fromtimestamp(start_time))
print("End Time : ", datetime.datetime.fromtimestamp(end_time))
print(f'execution time : {rounded_execution_time} minutes')