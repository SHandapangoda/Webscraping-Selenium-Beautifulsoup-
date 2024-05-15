from lxml import html
import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract():
    with open("UWA.txt", "r") as file:
        urls = [line.strip() for line in file.readlines()]

    data = []
    for url in urls:
        try:
            # Request the page for the current URL
            page = requests.get(url)
            if page.status_code != 200:
                print(f"Failed to fetch URL: {url}")
                continue  # Skip to the next URL if request fails

            # Parsing the page
            tree = html.fromstring(page.content)

            # Get elements using XPath
            fees = tree.xpath('/html/body/main/div[1]/div[4]/div[3]/div/div/div/div[3]/div[2]/div/section/div[1]/div/div[2]/div/div[2]')
            fees_text = fees[0].text_content().strip().replace('$', '').replace(',', '') if fees else ""

            #time_frame_element = tree.xpath('/html/body/main/div[1]/div[4]/div[6]/div/div/div/section/div[1]/div[1]/div/div/div[8]/ul/li/text()')
            #time_frame_element = time_frame_element[0].text_content().strip()

            #summary = tree.xpath('/html/body/main/div[1]/div[4]/div[6]/div/div/div/div/p')
            #summary = summary[0].text_content().strip()

            data.append({'URL': url, 'Fees': fees_text})
        except Exception as e:
            print(f"Error processing URL: {url}, Error: {str(e)}")

    # Create DataFrame after collecting data from all URLs
    df = pd.DataFrame(data)
    
    # Write DataFrame to Excel
    df.to_excel('UWA.xlsx', index=False)


def check_existing():
    # Read URLs from a text file
    with open("missingurl.txt", "r") as file:
        urls = [line.strip() for line in file.readlines()]

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

def crawl():


    url_direct = ['https://www.uwa.edu.au/study/areas/architecture-and-design#courses','https://www.uwa.edu.au/study/areas/business-and-commerce#courses','https://www.uwa.edu.au/study/areas/data-and-computer-science#courses','https://www.uwa.edu.au/study/areas/education#courses','https://www.uwa.edu.au/study/areas/health-and-biomedical-sciences#course','https://www.uwa.edu.au/study/areas/humanities-and-social-sciences#courses','https://www.uwa.edu.au/study/areas/law#courses','https://www.uwa.edu.au/study/areas/music-and-fine-arts#courses','https://www.uwa.edu.au/study/areas/natural-and-physical-sciences#courses','https://www.uwa.edu.au/study/areas/psychology#courses']
    unique_hrefs = set()  # Create an empty set to store unique href values

    with open('UWA.txt', 'a') as file:  # Open the file in append mode
        for url in url_direct:
            reqs = requests.get(url)
            soup = BeautifulSoup(reqs.text, 'html.parser')

            keywords = ['bachelor-of','master-of']
            for link in soup.find_all('a'):
                href = link.get('href')
                if href and any(keyword in href for keyword in keywords):

                    if href.startswith("https://www.uwa.edu.au/") or href.startswith("https://"):
                        full_url = href
                    else:
                        full_url = "https://www.uwa.edu.au/" + href.lstrip('/')
                    if full_url not in unique_hrefs:  # Check if the full URL is not already in the set
                        unique_hrefs.add(full_url)  # Add the full URL to the set
                        file.write(full_url + '\n')  # Write the URL to the file
                        print(full_url)


                    if href not in unique_hrefs:  # Check if the href value is not already in the set
                        unique_hrefs.add(href)  # Add the href value to the set
                        full_url = "https://www.uwa.edu.au/" + href
                        file.write(full_url + '\n')  # Write the URL to the file
                        print(full_url)

crawl()

