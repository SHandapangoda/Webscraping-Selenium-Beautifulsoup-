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

    return {'URL':url,'Name': name, 'Locations': ', '.join(locations), 'Summary': summary, 'Awards': ', '.join(award), 'Outcome': outcome}


def read_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file.readlines() if line.strip()]
    return urls

def check_Exsisiting_Urls(File):
   # Get the base name of the text file
   text_file_name = File
   
   # Read URLs from file
   with open(text_file_name, "r") as file:
       urls = [line.strip() for line in file.readlines()]

   # Create a session to handle cookies
   session = requests.Session()

   # Check each URL
   for url in urls:
       try:
           headers = {
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
               'Referer': url
           }
           response = session.get(url, headers=headers, allow_redirects=False)


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
           print(f"{url}: {status}", redirected_to)

def check_sheets():
    df1 = pd.read_excel('loyalist_data.xlsx')
    df2 = pd.read_excel('latest.xlsx')

    difference = df1[df1!=df2]
    print (difference)

if __name__ == '__main__':
    start_time = time.time()

    toronto()
    main_uni()

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
