
import time
from selenium import webdriver
from selenium.common import StaleElementReferenceException
from bs4 import BeautifulSoup
import pandas as pd
#from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import aiohttp
import asyncio
def crawl():
    # Set up Chrome driver service
     # Replace with the path to your chromedriver executable
    driver = webdriver.Firefox()

# Define the mother URL
    mother_url = 'https://uel.ac.uk/site-search?search_text=&search_category_type=courses&f%5B0%5D=course_level%3AUndergraduate&f%5B1%5D=facet_course_attendence%3AFull%20time&f%5B2%5D=facet_course_attendence%3AFull%20time%2C%201%20year&f%5B3%5D=facet_course_attendence%3AFull%20time%2C%202%20years&f%5B4%5D=facet_course_attendence%3AFull%20time%2C%203%20years&f%5B5%5D=facet_course_attendence%3AFull%20time%2C%203%2F4%20years&f%5B6%5D=facet_course_attendence%3AFull%20time%2C%203%2F4%2F5%20years&f%5B7%5D=facet_course_attendence%3AFull%20time%2C%204%20years&f%5B8%5D=facet_course_attendence%3AFull%20time%2C%204%2F5%20years&f%5B9%5D=facet_course_location%3ADocklands%20Campus&f%5B10%5D=facet_course_location%3AMaria%20Montessori%20Institute&f%5B11%5D=facet_course_location%3AStratford%20Campus&f%5B12%5D=facet_course_location%3AUniversity%20Square%20Stratford&f%5B13%5D=course_start_date%3AMarch%202024&f%5B14%5D=course_start_date%3ASeptember%202024&items_per_page=50&page='
    
# Define the keywords
    #keywords = ['minor', 'certficate','advanced_certificate']  # Replace with your desired keywords
    for page_number in range(0, 3):

# Open the mother URL
        driver.get(mother_url+str(page_number))

# Introduce a delay to wait for the page to load
        time.sleep(5)  # Adjust the delay time as needed

# Find all anchor elements
        course_anchors = driver.find_elements(By.CLASS_NAME, 'title')

    # Extract course URLs
        
        course_urls = set()
        for anchor in course_anchors:
            try:
                href = anchor.get_attribute('href')
                if href:
                    course_urls.add(href)
            except StaleElementReferenceException:
            # If StaleElementReferenceException occurs, reattempt finding the element
                continue

        #for url in course_urls:
            #print(url)
        with open('linksLondon.txt', 'a') as file:
            for url in course_urls:
                print(url)
                file.write(url + '\n')

    driver.close()

def crawl_masters():
        # Set up Chrome driver service
     # Replace with the path to your chromedriver executable
    driver = webdriver.Firefox()

# Define the mother URL
    mother_url = 'https://uel.ac.uk/site-search?search_text=&search_category_type=courses&f%5B0%5D=facet_course_attendence%3AFull%20time&f%5B1%5D=facet_course_attendence%3AFull%20time%2C%201%20year&f%5B2%5D=facet_course_attendence%3AFull%20time%2C%202%20years&f%5B3%5D=facet_course_attendence%3AFull%20time%2C%203%20years&f%5B4%5D=facet_course_attendence%3AFull%20time%2C%203%2F4%20years&f%5B5%5D=facet_course_attendence%3AFull%20time%2C%203%2F4%2F5%20years&f%5B6%5D=facet_course_attendence%3AFull%20time%2C%204%20years&f%5B7%5D=facet_course_attendence%3AFull%20time%2C%204%2F5%20years&f%5B8%5D=facet_course_location%3AMaria%20Montessori%20Institute&f%5B9%5D=course_start_date%3ASeptember%202024&f%5B10%5D=facet_course_location%3AUniversity%20Square%20Stratford%20and%20Docklands&f%5B11%5D=facet_course_location%3AUniversity%20Square%20Stratford&f%5B12%5D=course_level%3APostgraduate&f%5B13%5D=facet_course_location%3ADocklands%20Campus&f%5B14%5D=facet_course_location%3AStratford%20Campus&f%5B15%5D=facet_course_attendence%3AFull%20time%20(MFA)%2C%202%20years&f%5B16%5D=facet_course_attendence%3AFull%20time%2C%201%2F2%20years&f%5B17%5D=facet_course_location%3AUniversity%20Square%20Stratford%20and%20Stratford%20Campus&items_per_page=50&page='
    
# Define the keywords
    #keywords = ['minor', 'certficate','advanced_certificate']  # Replace with your desired keywords
    for page_number in range(0, 3):

# Open the mother URL
        driver.get(mother_url+str(page_number))

# Introduce a delay to wait for the page to load
        time.sleep(5)  # Adjust the delay time as needed

# Find all anchor elements
        course_anchors = driver.find_elements(By.CLASS_NAME, 'title')

    # Extract course URLs
        
        course_urls = set()
        for anchor in course_anchors:
            try:
                href = anchor.get_attribute('href')
                if href:
                    course_urls.add(href)
            except StaleElementReferenceException:
            # If StaleElementReferenceException occurs, reattempt finding the element
                continue

        #for url in course_urls:
            #print(url)
        with open('linksLondonmasters.txt', 'a') as file:
            for url in course_urls:
                print(url)
                file.write(url + '\n')

    driver.close()
async def fetch(url, session):
    async with session.get(url) as response:
        return await response.text()
    
async def get_details():
    with open('linksLondonmasters.txt', 'r') as file:
        urls = file.readlines()
    data = []
    async with aiohttp.ClientSession() as session:
        # Gather responses from all tasks
        tasks = []
        for url in urls:
            tasks.append(fetch(url.strip(), session))  # Strip newline characters
        pages = await asyncio.gather(*tasks)
        
        for url, page_content in zip(urls, pages):  # Iterate over both urls and pages simultaneously
            htmlParse = BeautifulSoup(page_content, 'html.parser')
        
            name = htmlParse.find_all("h1", class_='coh-heading coh-style-header-1-small coh-ce-cpt_course_page_hero_component-6ed92d12')
            summary = htmlParse.find_all("p", class_='coh-style-body')
            
            try:
                Fees = htmlParse.find_all("span",id = 'fee-fees-2-1-3-1')
                if Fees and Fees[0].get_text() != "":
                    Fees = Fees[0].get_text()
            except IndexError:
                "n/A"
            #ucas = htmlParse.find_all("span",class_='ucas-code')
            '''
            try:
                ucas1 = htmlParse.find_all("span",class_='ucas-code')
                if ucas1[1].get_text() != "":
                    ucas1[1].get_text()
            except IndexError:
                "n/A"
        '''
            EntryUcas = htmlParse.find_all("div", class_='rich-txt-custom')
            English = htmlParse.find_all("div",class_='rich-txt-custom' )
            starts = htmlParse.find_all('span', class_='course-details application-type application-type-2')
            start_text = starts[0].get_text() if starts else "n/a"

            attendance = htmlParse.find_all('span', class_='course-details attendance-type')
            attendance_text = attendance[4].get_text() if len(attendance) > 4 else "n/a"
            try:
                duration = htmlParse.find_all("span", id = 'fee-attendance-year-2-1-3-1')
                if duration and duration[0].get_text() !="":
                    duration = duration[0].get_text()
            except IndexError:
                "n/A"
            #data.append([url.strip(), name[0].get_text() if name else "",])
            data.append([url.strip(), name[0].get_text() if name else "", summary[0].get_text() if summary else "", Fees,  EntryUcas[2].get_text(), English[3].get_text(), duration, start_text, attendance_text])
    df = pd.DataFrame(data, columns=["url","name", "Summary","Fees","entry","english","duration","starts","attendance"])
    df.to_excel('extracted_london_masters.xlsx', index=False)
    
if __name__ == '__main__':
    asyncio.run(get_details())
    #crawl_masters()
