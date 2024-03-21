import requests
from bs4 import BeautifulSoup
from lxml import html
import pandas as pd


def crawl():
    # Define the base URL
    base_url = 'https://tus.ie/courses/?results-id=768&_sfm_course_type=undergraduate-cao&sf_paged='

    # Iterate over the range of page numbers
    for page_number in range(1, 20):  # Assuming you have 19 pages in total
        # Construct the URL for the current page
        url = base_url + str(page_number)

        # Fetch the page content
        reqs = requests.get(url)

        # Parse the page content
        soup = BeautifulSoup(reqs.text, 'html.parser')

        # Extract the URLs
        urls = []
        filter_word = "/courses/us"
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



# Import required modules


# Function to extract information from a single URL
def extract_information(url):
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
    # Return the extracted information
    return name, year, course_code, mode, course_summary, requirements, location

def read_existing():
    # Read the URLs from the text file
    with open('TUS.txt', 'r') as file:
        urls = file.readlines()

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

if __name__ == '__main__':
    # Specify the path to the text file containing URLs
    urls_file_path = 'TUS.txt'

    # Call read_existing function to read URLs and extract information
    read_existing(urls_file_path)