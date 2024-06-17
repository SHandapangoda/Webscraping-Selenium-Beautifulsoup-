from lxml import html
import requests
import pandas as pd
from bs4 import BeautifulSoup

def extractUG():
    url = 'https://www.ul.ie/courses/alphabetical-list-courses'
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    urls = []
    filter_word = "bachelor"
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith(("/courses")):
            if href and filter_word in href:
                full_url = f"https://www.ul.ie{href}"
                urls.append(full_url)
                #print(full_url)

    return urls  # Return the list of URLs

def read_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def extractFees(urls):
    data = {'URL': [], 'Fees': []}
    for url in urls:
        # Request the page
        page = requests.get(url)

        # Parsing the page
        tree = html.fromstring(page.content)

        # Get element using XPath
        fees_element = tree.xpath(
            '/html/body/div[1]/main/div/div/div[2]/article/div/div/div[2]/div[5]/div[3]/div/div[1]/div[4]/div/table/tbody/tr[1]/td[3]')

        # Extract text content from the element
        if fees_element:
            fees_text = fees_element[0].text_content().strip()
            fees_text = fees_text.replace('€', '').replace(',', '')
            # Append data to the lists
            data['URL'].append(url)
            data['Fees'].append(fees_text)
        else:
            print(f"URL: {url}\nElement not found.\n")

    # Create a DataFrame from the data
    df = pd.DataFrame(data)
    df.to_excel('scraped_data_fees.xlsx', index=False)

def extractcontent(urls):
    data = {'URL': [], 'Summary': []}
    for url in urls:
        # Request the page
        page = requests.get(url)

        # Parsing the page
        tree = html.fromstring(page.content)

        # Get element using XPath
        fees_element = tree.xpath(
            '/html/body/div[1]/main/div/div/div[2]/article/div/div/div[2]/div[1]/div/div[3]/div[2]/div/p[2]/text()')

        # Extract text content from the element
        if fees_element:
            fees_text = fees_element[0]
            fees_text = fees_text
            # Append data to the lists
            data['URL'].append(url)
            data['Summary'].append(fees_text)
        else:
            print(f"URL: {url}\nElement not found.\n")

    # Create a DataFrame from the data
    df = pd.DataFrame(data)
    df.to_excel('scraped_data.xlsx', index=False)


def extractlinksPG():
    url = 'https://www.ul.ie/gps/taught-programmes/taught-programmes-list'
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')

    urls = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.endswith(("-msc", "-ma", "-mba", "-meng", "-masters", "-degree", "-march")):
            urls.append(href)

    # Print the filtered URLs
    for url in urls:
        print(f"https://www.ul.ie{url}")

def scrape_course_information_PG(url):
    # Request the page
    page = requests.get(url)
    data = {'URL': [], 'Fees': []}
    # Check if the request was successful (status code 200)
    if page.status_code == 200:
        # Parsing the page
        tree = html.fromstring(page.content)

        # Use CSS selectors to get content within the div tag with class name
        content_elements = tree.cssselect('.field--name-field-course-pg-fees > p:nth-child(2)')

        # Extract text content from the elements
        content_text = [element.text_content().strip() for element in content_elements]

        if not content_text:
            content_elements = tree.cssselect('.field--name-field-course-pg-fees > p:nth-child(3) > span:nth-child(1)')
            content_text = [element.text_content().strip() for element in content_elements]

        # Append data to the lists
        for text in content_text:
            data['URL'].append(url)
            data['Fees'].append(text)
            print(url, text)

    else:
        print(f"Failed to fetch the page. Status Code: {page.status_code}")

    return data

all_data = {'URL': [], 'Fees': []}
    # Specify the path to the text file containing URLs
urls_file_path = 'linksLimerick.txt'

    # Read URLs from the text file
urls = read_urls_from_file(urls_file_path)

def url_read_for_missing(file_path):
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file if line.strip().startswith("https://www.ul.ie")]
    return urls

def check_missing():
    new_urls = extractUG()
    urls_file_path = 'linksLimerick.txt'
    old_urls = url_read_for_missing(urls_file_path)
    
    # Convert lists to sets for comparison
    new_set = set(new_urls)
    old_set = set(old_urls)
    
    # Find missing URLs
    missing = new_set - old_set
    
    # Print missing URLs
    for url in missing:
        print(url)
    return missing
check_missing()
'''
for url in urls:
    data = scrape_course_information_PG(url)
    all_data['URL'].extend(data['URL'])
    all_data['Fees'].extend(data['Fees'])

# Create a DataFrame from the collected data
df = pd.DataFrame(all_data)

# Save the DataFrame to an Excel file
df.to_excel('scraped_data_2024_06_17.xlsx', index=False)
'''