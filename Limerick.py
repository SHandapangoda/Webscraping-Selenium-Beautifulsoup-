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
                urls.append(href)


    # Print the filtered URLs
    for url in urls:
        print(f"https://www.ul.ie{url}")

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
    df.to_excel('scraped_data.xlsx', index=False)

def extractcontent(urls):
    data = {'URL': [], 'Summary': []}
    for url in urls:
        # Request the page
        page = requests.get(url)

        # Parsing the page
        tree = html.fromstring(page.content)

        # Get element using XPath
        fees_element = tree.xpath(
            '/html/body/div[1]/main/div/div/div[2]/article/div[2]/div[2]/div[3]/div[3]/div[4]/div/div/div/p[2]/text()')

        # Extract text content from the element
        if fees_element:
            fees_text = fees_element[0].text_content().strip()
            fees_text = fees_text.replace('€', '').replace(',', '')
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

        # Print the extracted content
        for text in content_text:
            print(url,text)

    else:
        print(f"Failed to fetch the page. Status Code: {page.status_code}")


if __name__ == "__main__":
    # Specify the path to the text file containing URLs
    urls_file_path = 'linksLimerick.txt'

    # Read URLs from the text file
    urls = read_urls_from_file(urls_file_path)

    # Extract fees and content
    extractFees(urls)
    #extractcontent(urls)
