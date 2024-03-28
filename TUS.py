import requests
from bs4 import BeautifulSoup
from lxml import html
import pandas as pd


def crawl():
    # Define the base URL
    base_url = 'https://tus.ie/courses/?results-id=768&_sfm_course_type=undergraduate-add-ons&sf_paged='

    # Iterate over the range of page numbers
    for page_number in range(1, 2):  # Assuming you have 19 pages in total
        # Construct the URL for the current page
        url = base_url + str(page_number)

        # Fetch the page content
        reqs = requests.get(url)

        # Parse the page content
        soup = BeautifulSoup(reqs.text, 'html.parser')

        # Extract the URLs
        urls = []
        filter_word = "/courses/a"
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and filter_word in href:
                urls.append(href)

        # Save matching URLs to a text file

        with open('linksTUS.txt', 'w') as file:
                    # Print the filtered URLs
            for url in urls:
                print(url)
                file.write(url + '\n')

def check_existing():
        # Read the URLs from the text file
    with open('TUS.txt', 'r') as file:
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

# Import required modules


def extract_information():
    with open('TUS.txt', 'r') as file:
        urls = file.readlines()

    # Clean up URLs by removing leading/trailing whitespace and newlines
    urls = [url.strip() for url in urls]

    # Request the page
    details = []
    for url in urls:
        # Request the page
        page = requests.get(url)
        # Parsing the page
        tree = html.fromstring(page.content)
        # Get elements using XPath
        names = tree.xpath('/html/body/main/div[1]/div/div/div[1]/h1/text()')
        names = [name.strip() for name in names]  # Remove leading/trailing whitespace
        if names:
            name = names[0]  # If there are multiple names, take the first one
        else:
            name = ""  # Handle the case where no name is found
        year = tree.xpath('/html/body/main/div[1]/div/div/div[1]/ul/li[3]/p/text()')
        year = year[0].strip() if year else ""
        course_code = tree.xpath('/html/body/main/div[1]/div/div/div[3]/ul/li[1]/p/text()')
        course_code = course_code[0].strip() if course_code else ""
        mode = tree.xpath('/html/body/main/div[1]/div/div/div[3]/ul/li[4]/p/text()')
        mode = mode[0].strip() if mode else ""
        course_summary = tree.xpath('/html/body/main/div[3]/div/div/div/div/p/text()[1]')
        course_summary = course_summary[0].strip() if course_summary else ""
        requirements = tree.xpath('/html/body/main/div[4]/div/div/div[2]/article/p[1]/text()')
        requirements = requirements[0].strip() if requirements else ""
        location = tree.xpath('/html/body/main/div[1]/div/div/div[1]/ul/li[2]/p/text()')
        location = location[0].strip() if location else ""
        # Append the extracted information to the details list
        details.append((name, year, course_code, mode, course_summary, requirements, location))

    # Return the list of extracted information for each URL
    return details

def scrape_existing():
    # Read the URLs from the text file
    
    with open('TUS.txt', 'r') as file:
        urls = file.readlines()
    urls = [url.strip() for url in urls]
# Create lists to store extracted information
    data = []
    for url in urls:
        url = url.strip()  # Remove leading/trailing whitespace
    # Extract information from the current URL
        name, year, course_code, mode, course_summary, requirements, location = extract_information(url)
    # Append extracted information as a row to the data list
        data.append([name, year, course_code, mode, course_summary, requirements, location])

# Create a DataFrame using the extracted data and specify column names
    df = pd.DataFrame(data, columns=['Name', 'Year', 'Course Code', 'Mode', 'Course Summary', 'Requirements', 'Location'])

# Export the DataFrame to an Excel file
    df.to_excel('extracted_data1.xlsx', index=False)
    return urls

def check_exisiting():
    urls = []
    with open('TUS.txt', 'r') as file:
        urls = file.readlines()
    return set(urls)

def check_new():
    urls = []
    with open('linksTUS.txt', 'r') as file:
        urls = file.readlines()
    return set(urls)

def check_missing():
    existing_urls = check_exisiting()  # Call check_existing function to get existing URLs
    new_urls = check_new()  # Call check_new function to get new URLs
    missing = existing_urls - new_urls  # Subtract existing URLs from new URLs to find missing ones
    return missing

if __name__ == '__main__':
    #missing_urls = check_missing()
    #print("Missing URLs:", missing_urls)
    details = extract_information()
    print(details)

    
