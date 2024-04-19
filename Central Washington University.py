import time
from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from lxml import html
import requests

def check_url_status():

            # Read the URLs from the text file
    with open('linkscentral', 'r') as file:
        urls = file.readlines()
    for url in urls:
        
        try:
            
            response = requests.get(url, allow_redirects=False)
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
            print(f"{url}: {status}")  # Print result in the terminal

        except Exception as e:
            status = f"Threw an Exception: {str(e)}"
            redirected_to = ""
            print(f"{url}: {status}")

    return urls

def scrape_details():
    with open('linkscentral', 'r') as file:
        urls = file.readlines()

    # Clean up URLs by removing leading/trailing whitespace and newlines
    urls = [url.strip() for url in urls]
    details = []
    for url in urls:
        # Request the page
        page = requests.get(url)
        # Parsing the page
        tree = html.fromstring(page.content)
        # Get elements using XPath
        names = tree.xpath('/html/body/div/main/div/div/div[1]/section[2]/div/ul[1]/li/a')
        names = [name.text_content() for name in names]  # Remove leading/trailing whitespace
        if names:
            name = names[0]  # If there are multiple names, take the first one
        else:
            name = ""  # Handle the case where no name is found
  
        # Append the extracted information to the details list
        details.append((url, name))

    # Return the list of extracted information for each URL
    return details

def crawl_UG():
    service = Service('chromedriver.exe')  # Replace with the path to your chromedriver executable
    driver = webdriver.Chrome(service=service)

    # Define the keywords
    keywords = ['https://www.cwu.edu/academics/explore-programs/']  # Replace with your desired keywords
    keywords_exc = ['.php']

    # Iterate over page indices from 0 to 9
    for page_index in range(10):
        # Define the mother URL for the current page index
        mother_url = f'https://www.cwu.edu/academics/explore-programs/index.php?search=&type=Majors&college=&deptprog=&pageindex={page_index}&pagesize=10'

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
                if href and any(href.startswith(keyword) for keyword in keywords):
                    if href and any(href.endswith(keyword) for keyword in keywords_exc):
                        matching_urls.append(href)
            except StaleElementReferenceException:
                # If StaleElementReferenceException occurs, reattempt finding the element
                continue

        # Print matching URLs for the current page index
        for url in matching_urls:
            print(url)

    # Close the driver
    driver.quit()

def crawl_PG():
    service = Service('chromedriver.exe')  # Replace with the path to your chromedriver executable
    driver = webdriver.Chrome(service=service)

    # Define the keywords
    keywords = ['https://www.cwu.edu/academics/explore-programs/']  # Replace with your desired keywords
    keywords_exc = ['.php']

    # Iterate over page indices from 0 to 5
    for page_index in range(5):
        # Define the mother URL for the current page index
        mother_url = f'https://www.cwu.edu/academics/explore-programs/index.php?search=&type=Graduate%20Degrees&college=&deptprog=&pageindex={page_index}&pagesize=10'

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
                if href and any(href.startswith(keyword) for keyword in keywords):
                    if href and any(href.endswith(keyword) for keyword in keywords_exc):
                        matching_urls.append(href)
            except StaleElementReferenceException:
                # If StaleElementReferenceException occurs, reattempt finding the element
                continue

        # Print matching URLs for the current page index
        for url in matching_urls:
            print(url)

    # Close the driver
    driver.quit()

def fees():
    # Request the page
    page = requests.get('https://www.cwu.edu/admissions-aid/financial-aid-scholarships/financial-aid/about/2023-2024-cost-attendance.php#accordion-afdc01f8-00bd-417e-b57e-9bd25a5d0389-2')

    # Parsing the page
    # (We need to use page.content rather than
    # page.text because html.fromstring implicitly
    # expects bytes as input.)
    tree = html.fromstring(page.content)

    # Get element using XPath
    UG = tree.cssselect('#main > div > div > div.content.cell.xsmall-12.large-8 > section:nth-child(6) > div.table__table > table > tbody > tr:nth-child(1) > td:nth-child(2)')
    PG = tree.cssselect('#main > div > div > div.content.cell.xsmall-12.large-8 > section:nth-child(9) > div.table__table > table > tbody > tr:nth-child(1) > td:nth-child(2)')
    UG_text = [element.text_content().strip() for element in UG]
    PG_text = [element.text_content().strip() for element in PG]

    print(UG_text)
    print(PG_text)

def UG_entry_english():
    page = requests.get('https://www.cwu.edu/admissions-aid/apply/additional-resources/proof-english-proficiency.php')

    # Parsing the page
    # (We need to use page.content rather than
    # page.text because html.fromstring implicitly
    # expects bytes as input.)
    tree = html.fromstring(page.content)

    # Get element using XPath
    TOEFL_elements = tree.xpath('/html/body/div/main/div/div/div[1]/section[1]/div/p[3]/text()[2]')
    Doulingo_elements = tree.xpath('/html/body/div/main/div/div/div[1]/section[1]/div/p[4]/text()[2]')
    IELTS_elements = tree.xpath('/html/body/div/main/div/div/div[1]/section[1]/div/p[5]/text()[2]')
    English_components = tree.xpath('/html/body/div/main/div/div/div[1]/section[1]/div/p[6]/text()')
    Cambridge_IG = tree.xpath('/html/body/div/main/div/div/div[1]/section[1]/div/p[7]')
    IB = tree.xpath('/html/body/div/main/div/div/div[1]/section[1]/div/p[8]')
    PTE = tree.xpath('/html/body/div/main/div/div/div[1]/section[1]/div/p[10]')
    C1 = tree.xpath('/html/body/div/main/div/div/div[1]/section[1]/div/p[12]')
    C2 = tree.xpath('/html/body/div/main/div/div/div[1]/section[1]/div/p[14]')
    SAT = tree.xpath('/html/body/div/main/div/div/div[1]/section[1]/div/p[15]')
    ACT = tree.xpath('/html/body/div/main/div/div/div[1]/section[1]/div/p[16]')
    TOEFL_text = [elements for elements in TOEFL_elements]
    Doulingo_text = [elements for elements in Doulingo_elements]
    IELTS_text = [elements for elements in IELTS_elements]
    English_components_text = [elements for elements in English_components]
    Cambridge_IG_text = [elements for elements in Cambridge_IG]
    IB_text = [elements.text_content().strip() for elements in IB]
    PTE_text = [elements.text_content().strip() for elements in PTE]
    C1_text = [elements.text_content().strip() for elements in C1]
    C2_text = [elements.text_content().strip() for elements in C2]
    SAT_text = [elements.text_content().strip() for elements in SAT]
    ACT_text = [elements.text_content().strip() for elements in ACT]

    print(TOEFL_text)
    print(Doulingo_text)
    print(IELTS_text)
    print(Cambridge_IG_text)
    print(English_components_text)
    print(IB_text)
    print(PTE_text)
    print(C1_text)
    print(C2_text)
    print(SAT_text)
    print(ACT_text)

def PG_entry():
    page = requests.get('https://www.cwu.edu/academics/colleges/graduate-studies-research/student-resources-and-general-faqs/international-student-admissions.php#accordion-876cdfb4-127d-43a9-bf68-dc6e806f6370-0')

    # Parsing the page
    # (We need to use page.content rather than
    # page.text because html.fromstring implicitly
    # expects bytes as input.)
    tree = html.fromstring(page.content)

    # Get element using XPath
    Application_elements = tree.cssselect('#main > div > div > div.content.cell.xsmall-12.large-8 > section:nth-child(2) > div > ul:nth-child(4) > li:nth-child(1)')
    GPA_elements = tree.xpath('/html/body/div/main/div/div/div[1]/section[2]/div/ul[1]/li[3]/text()')
    English_elements = tree.xpath('/html/body/div/main/div/div/div[1]/section[2]/div/ul[1]/li[4]/text()')

    Application_text = [elements.text_content().strip() for elements in Application_elements]
    GPA_text = [elements for elements in GPA_elements]
    English_text = [elements for elements in English_elements]

    print(Application_text)
    print(GPA_text)
    print(English_text)

for url, name in scrape_details():
    print(f"{url}, {name}")