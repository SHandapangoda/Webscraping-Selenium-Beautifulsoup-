import pandas as pd
from lxml import html
import requests
import time
from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def crawl():
    # Set up Chrome driver service
    service = Service('chromedriver.exe')  # Replace with the path to your chromedriver executable
    driver = webdriver.Chrome(service=service)

# Define the mother URL
    mother_url = 'https://www.tntech.edu/majors/'

# Define the keywords
    keywords = ['majors']  # Replace with your desired keywords
    keywords_exc = ['index', '#', '.pcf','career.php']

# Open the mother URL
    driver.get(mother_url)

# Introduce a delay to wait for the page to load
    time.sleep(5)  # Adjust the delay time as needed

# Find all anchor elements
    anchors = driver.find_elements(By.TAG_NAME, 'a')

# Extract URLs containing the keywords
    matching_urls = []
    for anchor in anchors:
        try:
            href = anchor.get_attribute('href')
            if href and any(keyword in href for keyword in keywords):
                if href and not(any(keyword in href for keyword in keywords_exc)):
                    matching_urls.append(href)
        except StaleElementReferenceException:
        # If StaleElementReferenceException occurs, reattempt finding the element
            continue

    for url in matching_urls:
        print(url)

# Save matching URLs to a text file
# with open('linksSUNY.txt', 'w') as file:
#     for url in matching_urls:
#         file.write(url + '\n')

# Close the driver
    driver.quit()
    

# Define a function to process each URL
def process_url(url):
    print("Requested URL:", url)  # Print the requested URL

    # Request the page
    page = requests.get(url)

    # Parsing the page
    tree = html.fromstring(page.content)

    # Get elements using XPath
    major = tree.xpath('/html/body/main/div[1]/div/div[1]/section/div/div/div/address[1]/text()[2]')
    concentrate = tree.xpath('/html/body/main/div[1]/div/div[1]/section/div/div/div/address[1]/text()[3]')
    summary = tree.xpath('/html/body/main/div[1]/div/div[2]/div/div/div/p[1]/text()')

    # Set default values for modified_text and modified_text_con
    modified_text = "Not found"
    modified_text_con = "Not found"
    original_tex_sum = "Not Found"

    # Remove "Major:" from the string
    if major:
        original_text = major[0]
        modified_text = original_text.replace("Major:", "").strip()

    # Remove "Concentration:" from the string
    if concentrate:
        original_text_con = concentrate[0]
        modified_text_con = original_text_con.replace("Concentration:", "").strip()

    if summary:
        original_tex_sum = summary[0]

    return {'URL': url, 'modified_text': modified_text, 'modified_text_con': modified_text_con, 'Summary': original_tex_sum}
def check_sheets():
    df1 = pd.read_excel('output test.xlsx') # replace, rename with the old scraped excel sheet
    df2 = pd.read_excel('masters1.xlsx') # latest

    difference = df1[df1!=df2]
    print (difference)

def get_fees():

    # Request the page
    page = requests.get('https://www.tntech.edu/bursar/tuition/index.php')
    tree = html.fromstring(page.content)  
    data = []
# Get element using XPath
    fees_UG = tree.xpath('/html/body/main/div[2]/div/div[1]/div/div/div/table[2]/tbody/tr[5]/td[2]')
    fees_ug_text = [text.text_content().strip() for text in fees_UG]
    fees_PG = tree.xpath('/html/body/main/div[2]/div/div[1]/div/div/div/table[4]/tbody/tr[5]/td[2]')
    fees_pg_text = [text.text_content().strip() for text in fees_PG]
    print(fees_ug_text)
    print(fees_pg_text)
    today = date.today()
    data.append({'Date':today, 'UG':fees_ug_text,'PG':fees_pg_text})
    df = pd.DataFrame(data)
    excel_file = 'fees.xlsx'

    try:

        df_existing = pd.read_excel(excel_file)
        df_combined = pd.concat([df_existing, df], ignore_index=True)
    except FileNotFoundError:
        df_combined = df
    df_combined.to_excel(excel_file, index=False)
    print(df)
# Define the file containing URLs
file_path = 'tennessee test urls'

# Read URLs from the file and process each one
data = []
with open(file_path, 'r') as file:
    urls = file.readlines()
    for url in urls:
        url = url.strip()  # Remove leading/trailing whitespaces and newlines
        data.append(process_url(url))

# Create a DataFrame
df = pd.DataFrame(data)

# Save DataFrame to Excel
excel_file = 'output test.xlsx'
df.to_excel(excel_file, index=False)

print("Data saved to", excel_file)
