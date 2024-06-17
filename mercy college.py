import requests
from bs4 import BeautifulSoup
from lxml import html
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

def crawl_masters():
	url = 'https://www.mercy.edu/academics/programs?location=All&level=14&interest=All&school=All'
	reqs = requests.get(url)
	soup = BeautifulSoup(reqs.text, 'html.parser')

	urls = []
	filter_word = "certificate"
	for link in soup.find_all('a'):
		href = link.get('href')
		if href and href.startswith(("/academics/programs/")):
			if href and filter_word not in href:
				urls.append(href)
				print("https://www.mercy.edu"+link.get('href'))

def crawl_ug():
	url = 'https://www.mercy.edu/academics/programs?location=All&level=13&interest=All&school=All'
	reqs = requests.get(url)
	soup = BeautifulSoup(reqs.text, 'html.parser')

	urls = []
	filter_word = "certificate"
	for link in soup.find_all('a'):
		href = link.get('href')
		if href and href.startswith(("/academics/programs/")):
			if href and filter_word not in href:
				urls.append(href)
				print("https://www.mercy.edu"+link.get('href'))
				#return("https://www.mercy.edu"+link.get('href'))


def check_existing():
	with open('linksmercy.txt',"r") as file:
		urls = [line.strip() for line in file.readlines()]
	session = requests.Session()
	for url in urls: 
		
		response = session.get(url)
		if response.status_code == 200:
			status = "OK"
			redirected_to = ""
		elif response.status_code >= 300 and response.status_code < 400:
			status = f"Redirected ({response.status_code})"
			redirected_to = response.headers.get('Location', 'Unknown')
		elif response.status_code == 403:
			status = "Forbidden"
			redirected_to = ""
		else:
			status = f"Returned Status Code {response.status_code}"
			redirected_to = ""
		print(f"{url}: {status} - {redirected_to}")
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
def get_details():
    with open('linksmercy.txt',"r") as file:
        urls = [line.strip() for line in file.readlines()]
    data = []
    with ThreadPoolExecutor() as executor:
        # Submit tasks for fetching URLs
        futures = [executor.submit(fetch, url) for url in urls]
        for future, url in zip(futures, urls):
            page_content = future.result()
            if page_content:
                tree = html.fromstring(page_content)
                soup = BeautifulSoup(page_content, 'html.parser')
                tag = soup.find("ul", class_='no-bullets list-inline list-inline--pipe global-spacing--xsmall')

                words_to_filter = ['Bronx', 'Manhattan', 'Online', 'Westchester']
                
                # Filtering
                filtered_text = ' '.join(word for word in tag.text.split() if word in words_to_filter) # type: ignore
                summary = tree.xpath('/html/body/div[2]/div/div[3]/main/div/article/section[2]/div/div/div[2]/div/div/p')
                summary = [text.text_content().strip() for text in summary]
                
                #print(url)
                #print(filtered_text.strip())
                #print(summary)

                data.append({'URL':url, 'Location':filtered_text.strip(),'Summary':summary})
                df = pd.DataFrame(data)

        print(df)
        df.to_excel('Mercy.xlsx')

get_details()