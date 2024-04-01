from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from lxml import html
import requests
import urllib.request  
from bs4 import BeautifulSoup 
import pandas as pd
def scrape():
# Set up Chrome driver service
    service = Service('chromedriver.exe')  # Replace with the path to your chromedriver executable
    driver = webdriver.Chrome(service=service)

# Define the mother URL
# mother_url = 'https://admission.wsu.edu/academics/fos/Public/area.castle?id=41819'  # Replace with the actual mother URL
    mother_url = 'https://www.abertay.ac.uk/course-search?studyLevel=Undergraduate'  # Replace with the actual mother URL

# Define the keywords
    keywords = ['/undergraduate']# Replace with your desired keywords

# Open the mother URL
    driver.get(mother_url)

# Find all anchor elements
    anchors = driver.find_elements(By.TAG_NAME, 'a')

# Extract URLs containing the keywords
    matching_urls = []
    for anchor in anchors:
        href = anchor.get_attribute('href')
        if href and any(keyword in href for keyword in keywords):
            matching_urls.append(href)

    for url in matching_urls:
        print(url + '/n')
# Save matching URLs to a text file
    with open('linksAbertay.txt', 'w') as file:
        for url in matching_urls:
            file.write(url + '\n')

# Close the driver
    driver.quit()

def extract_content(url):
    try:
        html = urllib.request.urlopen(url)
# parsing the html file 
        htmlParse = BeautifulSoup(html, 'html.parser') 
        previous_text = None  # Variable to store previous text 
# getting all the paragraphs 
        for para in htmlParse.find_all("td"):
            text = para.get_text().strip()
    
            if "Points" and previous_text == "International Baccalaureate":
                points = text.split()[0]
                return points
                
            previous_text = text
    except Exception as e:
        return "Null"
            
import pandas as pd

def extract_Summary(urls):
    data = {'URL': [], 'Summary': []}
    for url in urls:
        # opening the url for reading 
        html = urllib.request.urlopen(url) 
  
        # parsing the html file 
        htmlParse = BeautifulSoup(html, 'html.parser') 
  
        # Getting all the paragraphs with class 'preamble'
        preambles = htmlParse.find_all("p", class_='preamble')

        # Check if there are at least two 'preamble' elements
        if len(preambles) >= 2:
            # Extract the second 'preamble' element
            second_preamble = preambles[1]
            print(second_preamble.get_text())
        else:
            print("There is no second preamble element on the page.")
        
        # Append URL and Summary to data dictionary
        data['URL'].append(url)
        data['Summary'].append(second_preamble.get_text() if len(preambles) >= 2 else "No second preamble element found")

    # Create a DataFrame from the data
    df = pd.DataFrame(data)
    df.to_excel('scraped_data.xlsx', index=False)




file_path = 'linksAbertay.txt'

# Open the file and read URLs
with open(file_path, 'r') as file:
    urls = [line.strip() for line in file.readlines()]

# Call extract_Summary() with the list of URLs
extract_Summary(urls)

# Process each URL
#for url in urls:
    #url = url.strip()  # Remove leading/trailing whitespace, including newline characters
    #content = extract_Summary([url])  #
    #if content is not None:
        #print(url + " " + content)
    #else:
        #print(url + " Error: Unable to extract content")

