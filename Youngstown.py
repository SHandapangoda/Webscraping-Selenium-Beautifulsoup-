import pandas as pd
from bs4 import BeautifulSoup
import requests
from lxml import html
from concurrent.futures import ThreadPoolExecutor
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
    with open('youngstownExUG.txt', 'r') as file:
        urls = file.readlines()

    # Clean up URLs by removing leading/trailing whitespace and newlines
    urls = [url.strip() for url in urls]

    # Create a list to store the extracted information
    data = []

    with ThreadPoolExecutor() as executor:
        # Submit tasks for fetching URLs
        futures = [executor.submit(fetch, url) for url in urls]
        

        # Process results
        for future, url in zip(futures, urls):
            page_content = future.result()
            if page_content:
                # Parsing the page
                tree = html.fromstring(page_content)
                # Get elements using XPath
                names = tree.cssselect('#main-content > div > div.shards-top.shards-bottom > div.article-wrapper.row > article > div > div.field.field-name-title > h1')
                names = [name.text.strip() for name in names if name.text.strip()]  # Remove leading/trailing whitespace
                name = names[0] if names else ""  # If there are multiple names, take the first one
                course_summary_elements = tree.cssselect('#main-content > div > div.shards-top.shards-bottom > div.article-wrapper.row > article > div > div.article-intro > div > p')
                course_summary = course_summary_elements[0].text_content().strip() if course_summary_elements else ""
                # Append the extracted information to the list
                data.append([url,name, course_summary])

    # Export the list to an Excel file
    df = pd.DataFrame(data, columns=['URL','Name', 'Course Summary'])
    print(df)
    df.to_excel('extracted_datayoungUG.xlsx', index=False)

    return df

def extract_information_and_export_to_excel_PG():
    # Read the URLs from the text file
    with open('youngstownExPG.txt', 'r') as file:
        urls = file.readlines()

   
    # Clean up URLs by removing leading/trailing whitespace and newlines
    urls = [url.strip() for url in urls]

    # Create a list to store the extracted information
    data = []

    with ThreadPoolExecutor() as executor:
        # Submit tasks for fetching URLs
        futures = [executor.submit(fetch, url) for url in urls]
        

        # Process results
        for future, url in zip(futures, urls):
            page_content = future.result()
            if page_content:
                # Parsing the page
                tree = html.fromstring(page_content)
                # Get elements using XPath
                names = tree.cssselect('#main-content > div > div.shards-top.shards-bottom > div.article-wrapper.row > article > div > div.field.field-name-title > h1')
                names = [name.text.strip() for name in names if name.text.strip()]  # Remove leading/trailing whitespace
                name = names[0] if names else ""  # If there are multiple names, take the first one
                course_summary_elements = tree.cssselect('#main-content > div > div.shards-top.shards-bottom > div.article-wrapper.row > article > div > div.article-intro > div')
                course_summary = course_summary_elements[0].text_content().strip() if course_summary_elements else ""
                # Append the extracted information to the list
                data.append([url,name, course_summary])

    # Export the list to an Excel file
    df = pd.DataFrame(data, columns=['URL','Name', 'Course Summary'])
    print(df)
    df.to_excel('extracted_datayoungPG.xlsx', index=False)

    return df

def crawl_UG():
    url = 'https://ysu.edu/international-programs-office/undergraduate-programs-international-students'
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')

    urls = []
    filter_word = "minor"
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith(("https://ysu.edu/academics")):
            if href and filter_word not in href:
                urls.append(href)
                print(href)

    with open('youngstownUG.txt', 'w') as file:
        # Print the filtered URLs
        for url in urls:
            print(url)
            file.write(url + '\n')

def crawl_PG():
    url = 'https://ysu.edu/international-programs-office/graduate-programs'
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')

    urls = []
    filter_word = "minor"
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith(("https://ysu.edu/academics")):
            if href and filter_word not in href:
                urls.append(href)
                print(href)

    with open('youngstownPG.txt', 'w') as file:
        # Print the filtered URLs
        for url in urls:
            print(url)
            file.write(url + '\n')

def check_existing():
    existing_urls = []
    with open('youngstownExUG.txt', 'r') as file:
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

def cross_validate_with_new_file(existing_urls):
    # Read the new URLs from another text file
    with open('youngstownUG.txt', 'r') as file:
        new_urls = file.readlines()

    new_urls = [url.strip() for url in new_urls]

    # Cross-validate with existing URLs
    matching_urls = set(new_urls) - set(existing_urls)
    return matching_urls
existing_urls = check_existing()
matching_urls = cross_validate_with_new_file(existing_urls)
print("Matching URLs in the new file:")
print(matching_urls)
crawl_PG()