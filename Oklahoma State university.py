from lxml import html
import requests
import pandas as pd
from bs4 import BeautifulSoup
import asyncio
import aiohttp

async def fetch(url, session):
    async with session.get(url) as response:
        return await response.text()

async def extract_information_and_export_to_excel():
    # Read the URLs from the text file
    with open('existingoklahoma.txt', 'r') as file:
        urls = file.readlines()

    # Clean up URLs by removing leading/trailing whitespace and newlines
    urls = [url.strip() for url in urls]

    # Create a list to store the extracted information
    data = []

    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(fetch(url, session))
        
        # Gather responses from all tasks
        pages = await asyncio.gather(*tasks)

        # Extract information from each page
        for page_content in pages:
            # Parsing the page
            tree = html.fromstring(page_content)
            # Get elements using XPath
            names = tree.xpath('/html/body/main/div[3]/div/div/aside/div/div[2]/div/span')
            names = [name.text.strip() if name.text else "" for name in names]  # Remove leading/trailing whitespace
            if names:
                name = names[0]  # If there are multiple names, take the first one
            else:
                name = ""  # Handle the case where no name is found
            #year = tree.xpath('/html/body/main/div[1]/div/div/div[1]/ul/li[3]/p/text()')
            #year = year[0].strip() if year else ""
            #course_code = tree.xpath('/html/body/main/div[1]/div/div/div[3]/ul/li[1]/p/text()')
            #course_code = course_code[0].strip() if course_code else ""
            #mode = tree.xpath('/html/body/main/div[1]/div/div/div[3]/ul/li[4]/p/text()')
            #mode = mode[0].strip() if mode else ""
            course_summary_elements = tree.xpath('/html/body/main/div[1]/div/div/div/div/h1')
            course_summary = course_summary_elements[0].text.strip() if course_summary_elements else ""
            #requirements = tree.xpath('/html/body/main/div[4]/div/div/div[2]/article/p[1]/text()')
            #requirements = requirements[0].strip() if requirements else ""
            #location = tree.xpath('/html/body/main/div[1]/div/div/div[1]/ul/li[2]/p/text()')
            #location = location[0].strip() if location else ""

            # Append the extracted information to the DataFrame
            data.append([name, course_summary])

    # Export the DataFrame to an Excel file
    df = pd.DataFrame(data, columns=['Name', 'Course Summary'])
    df.to_excel('extracted_dataok.xlsx', index=False)

    return df

# Read URLs from a text file
def crawl_masters():
	url = 'https://go.okstate.edu/undergraduate-academics/majors/'
	reqs = requests.get(url)
	soup = BeautifulSoup(reqs.text, 'html.parser')

	urls = []
	filter_word = "option.html"
	for link in soup.find_all('a'):
		href = link.get('href')
		if href and href.startswith(("https://go.okstate.edu/undergraduate-academics/majors")):

			if href and filter_word not in href:
                            urls.append(href)
                            print(href)
                            with open('linksoklahoma.txt', 'w') as file:
                    # Print the filtered URLs
                                for url in urls:
                                    print(url)
                                    file.write(url + '\n')
def check_existing():
    existing_urls = []
    with open('existingoklahoma.txt', 'r') as file:
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


  
#new_urls = set(matching_urls) - set(existing_urls)
#missing_urls = set(existing_urls) - set(matching_urls)

def cross_validate_with_new_file(existing_urls):
    # Read the new URLs from another text file
    with open('linksoklahoma.txt', 'r') as file:
        new_urls = file.readlines()

    new_urls = [url.strip() for url in new_urls]

    # Cross-validate with existing URLs
    matching_urls = set(new_urls) - set(existing_urls)
    return matching_urls

def entry():
    # Request the page
    page = requests.get('https://go.okstate.edu/admissions/international/freshman/requirements.html')

    # Parsing the page
    # (We need to use page.content rather than
    # page.text because html.fromstring implicitly
    # expects bytes as input.)
    tree = html.fromstring(page.content)

    # Get element using XPath
    high_school = tree.xpath('/html/body/main/div/div/div/div/ul[1]/li/text()')
    TOEFL = tree.xpath('/html/body/main/div/div/div/div/ul[2]/li/ul/li[1]/text()')
    IELTS = tree.xpath('/html/body/main/div/div/div/div/ul[2]/li/ul/li[2]/text()')
    PTE = tree.xpath('/html/body/main/div/div/div/div/ul[2]/li/ul/li[3]/text()')
    iTEP = tree.xpath('/html/body/main/div/div/div/div/ul[2]/li/ul/li[4]/text()')
    Doulingo = tree.xpath('/html/body/main/div/div/div/div/ul[2]/li/ul/li[5]/text()')
    high_school_text = [element.strip() for element in high_school]
    TOEFL_text = [element.strip() for element in TOEFL]
    IELTS_text = [element.strip() for element in IELTS]
    PTE_text = [element.strip() for element in PTE]
    iTEP_text = [element.strip() for element in iTEP]
    Doulingo_text = [element.strip() for element in Doulingo]
    print(high_school_text)
    print(TOEFL_text)
    print(IELTS_text)
    print(PTE_text)
    print(iTEP_text)
    print(Doulingo_text)

def fees():
    # Request the page
    page = requests.get('https://go.okstate.edu/scholarships-financial-aid/')

    # Parsing the page
    # (We need to use page.content rather than
    # page.text because html.fromstring implicitly
    # expects bytes as input.)
    tree = html.fromstring(page.content)

    # Get element using XPath
    UG = tree.xpath('/html/body/main/div[4]/div/div/div/div[2]/div[3]/div/div/ul/li[1]/text()')
    UG_text = [element for element in UG]
    
    print(UG_text)
    
existing_urls = check_existing()
matching_urls = cross_validate_with_new_file(existing_urls)
print("Matching URLs in the new file:")
print(matching_urls)
asyncio.run(extract_information_and_export_to_excel())