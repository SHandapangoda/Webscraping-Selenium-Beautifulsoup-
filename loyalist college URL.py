import multiprocessing
import requests
from bs4 import BeautifulSoup
from lxml import html
import time
import pandas as pd


def toronto():
    url = 'https://loyalistcollege.com/international/welcome-to-loyalist-college-in-toronto/programs/'
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    keywords = ["https://loyalistcollege.com/programs-and-courses/full-time-programs/"]
    end = ["-toronto"]
    urls = []
    for link in soup.find_all('a'):
        href = link.get('href')

        if href and any(href.startswith(keyword) for keyword in keywords):
            urls.append(href)
            text = link.get_text()  # Extract the text within <a> tag
            print(link.get('href'))

    with open('linksloyalisttoronto.txt', 'w') as file:
        for url in urls:
            file.write(url + '\n')


def main_uni():
    url = 'https://loyalistcollege.com/programs-and-courses/full-time-programs/'
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    keywords = ["/programs-and-courses"]
    urls = []
    for link in soup.find_all('a'):
        href = link.get('href')

        if href and any(href.startswith(keyword) for keyword in keywords):
            urls.append(href)
            print(link.get('href'))

    with open('linksloyalist.txt', 'w') as file:
        for url in urls:
            file.write("https://loyalistcollege.com" + url + '\n')


def process_url(url):
    # Request the page

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    # Parsing the page
    tree = html.fromstring(page.content)

    # Get element using XPath
    name = tree.xpath('/html/body/div[1]/section[2]/h1/text()')
    summary = tree.xpath('/html/body/div[1]/section[2]/div[2]')
    summary = [summary.text_content().strip() for summary in summary]
    award = tree.xpath('/html/body/div[1]/section[2]/div[4]/ul[1]/li[1]/ul')
    award = [award.text_content().strip() for award in award]
    location_items = soup.find_all('ul', class_='location-ul')
    locations = [item.text.strip() for sublist in location_items for item in sublist.find_all('li')]
    link = soup.find('a', title='international students', href='https://loyalistcollege.com/international/future-international-students/how-to-apply/')
    if link:

        outcome = "yes"
    else:

        outcome = "No"

    return {'Name': name, 'Locations': ', '.join(locations), 'Summary': summary, 'Awards': ', '.join(award), 'Outcome': outcome}


def read_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file.readlines() if line.strip()]
    return urls

if __name__ == '__main__':
    start_time = time.time()

    # Specify the path to the text file containing URLs
    urls_file_path = 'C:/Users/User/PycharmProjects/pythonProject/linksloyalist.txt'

    # Read URLs from the text file
    urls_to_process = read_urls_from_file(urls_file_path)

    # Scrape course information for each URL
    with multiprocessing.Pool() as pool:
        results = pool.map(process_url, urls_to_process)

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(results)

    # Save the DataFrame to an Excel file
    df.to_excel('loyalist_data.xlsx', index=False)

    print("loyalist data.xlsx'.")


    print(f"{(time.time() - start_time):.2f} seconds")
