import requests 
from bs4 import BeautifulSoup 
import pandas as pd
import psutil
import urllib.request 

def get_initial_system_usage():
    # Get initial RAM and CPU usage
    initial_ram_usage = psutil.virtual_memory().used
    initial_cpu_usage = psutil.cpu_percent()
    return initial_ram_usage, initial_cpu_usage

def get_final_system_usage(initial_ram_usage, initial_cpu_usage):
    # Get final RAM and CPU usage
    final_ram_usage = psutil.virtual_memory().used
    final_cpu_usage = psutil.cpu_percent()
    return final_ram_usage - initial_ram_usage, final_cpu_usage - initial_cpu_usage

def get_initial_network_usage():
    # Get initial network usage
    initial_net_io = psutil.net_io_counters()
    initial_bytes_sent = initial_net_io.bytes_sent
    initial_bytes_received = initial_net_io.bytes_recv
    return initial_bytes_sent, initial_bytes_received

def get_final_network_usage(initial_bytes_sent, initial_bytes_received):
    # Get final network usage
    final_net_io = psutil.net_io_counters()
    final_bytes_sent = final_net_io.bytes_sent
    final_bytes_received = final_net_io.bytes_recv
    return final_bytes_sent - initial_bytes_sent, final_bytes_received - initial_bytes_received

#use a filtered method in given in the webpage
def crawl_UG():
    urls = [
        'https://www.abertay.ac.uk/course-search/?studyLevel=Undergraduate&subject=Accounting%20and%20Finance',
        'https://www.abertay.ac.uk/course-search/?studyLevel=Undergraduate&subject=Biomedical%20Science%20and%20Forensic%20Sciences',
        'https://www.abertay.ac.uk/course-search/?studyLevel=Undergraduate&subject=Business%20Management%20and%20Marketing',
        'https://www.abertay.ac.uk/course-search/?studyLevel=Undergraduate&subject=Civil%20Engineering',
        'https://www.abertay.ac.uk/course-search?studyLevel=Undergraduate&subject=Computing%20Ethical%20Hacking%20Cybersecurity',
        'https://www.abertay.ac.uk/course-search?studyLevel=Undergraduate&subject=Counselling',
        'https://www.abertay.ac.uk/course-search?studyLevel=Undergraduate&subject=Criminology',
        'https://www.abertay.ac.uk/course-search?studyLevel=Undergraduate&subject=Food%20Science%20Nutrition%20and%20Health',
        'https://www.abertay.ac.uk/course-search?studyLevel=Undergraduate&subject=Law',
        'https://www.abertay.ac.uk/course-search?studyLevel=Undergraduate&subject=Nursing',
        'https://www.abertay.ac.uk/course-search?studyLevel=Undergraduate&subject=Psychology',
        'https://www.abertay.ac.uk/course-search?studyLevel=Undergraduate&subject=Sport%20Health%20and%20Exercise%20Science',
        'https://www.abertay.ac.uk/course-search?studyLevel=Undergraduate&subject=Video%20Games'
    ]

    for url in urls:
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')

        for link in soup.find_all('a', href=True):
            href = link.get('href')
            if href and href.startswith("https://search.abertay.ac.uk/s/redirect?"):
                print(href, link.text.strip())
                print()

def crawl_masters():
        urls = [
        'https://www.abertay.ac.uk/course-search?studyLevel=Postgraduate%20Taught&subject=Accounting%20and%20Finance',
        'https://www.abertay.ac.uk/course-search?studyLevel=Postgraduate%20Taught&subject=Business%20Management%20and%20Marketing',
        'https://www.abertay.ac.uk/course-search?studyLevel=Postgraduate%20Taught&subject=Civil%20Engineering',
        'https://www.abertay.ac.uk/course-search?studyLevel=Postgraduate%20Taught&subject=Computing%20Ethical%20Hacking%20Cybersecurity',
        'https://www.abertay.ac.uk/course-search?studyLevel=Postgraduate%20Taught&subject=Counselling',
        'https://www.abertay.ac.uk/course-search?studyLevel=Postgraduate%20Taught&subject=Food%20Science%20Nutrition%20and%20Health',
        'https://www.abertay.ac.uk/course-search?studyLevel=Postgraduate%20Taught&subject=Law',
        'https://www.abertay.ac.uk/course-search?studyLevel=Postgraduate%20Taught&subject=Psychology',
        'https://www.abertay.ac.uk/course-search?studyLevel=Postgraduate%20Taught&subject=Video%20Games'
    ]

        all_data = {'url': [], 'text': []}
    
        for url in urls:
            reqs = requests.get(url)
            soup = BeautifulSoup(reqs.text, 'html.parser')

            data = {'url': [], 'text': []}
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                if href and href.startswith("https://search.abertay.ac.uk/s/redirect?"):
                
                    print(href, link.text.strip())
                    data['url'].append(href)
                    data['text'].append(link.text.strip())
        
            all_data['url'].extend(data['url'])
            all_data['text'].extend(data['text'])

        df = pd.DataFrame(all_data)
        df.to_excel('mastersurl.xlsx', index=False)

def extract_content(url):
    try:
        html = urllib.request.urlopen(url)
# parsing the html file 
        htmlParse = BeautifulSoup(html, 'html.parser') 
        previous_text = None  # Variable to store previous text 
        
# getting all the paragraphs 
        for para in htmlParse.find_all("td"):
            text = para.get_text().strip()
    
            if previous_text == "Higher (standard entry)":
                points = text.split()[0]
                return points
                
            previous_text = text
    except Exception as e:
        return "Null"
            


def extract_Summary(urls):
    data = {'URL': [], 'Summary': []}
    for url in urls:
        # opening the url for reading 
        html = urllib.request.urlopen(url) 
  
        # parsing the html file 
        htmlParse = BeautifulSoup(html, 'html.parser') 
  
        # Getting all the paragraphs with class 'preamble'
        preambles = htmlParse.find_all("p", class_='preamble')

        # Check if there are at least two 'preamble' elements
        if len(preambles) >= 2:
            # Extract the second 'preamble' element
            second_preamble = preambles[1]
            print(second_preamble.get_text())
        else:
            print("There is no second preamble element on the page.")
        
        # Append URL and Summary to data dictionary
        data['URL'].append(url)
        data['Summary'].append(second_preamble.get_text() if len(preambles) >= 2 else "No second preamble element found")

    # Create a DataFrame from the data
    df = pd.DataFrame(data)
    df.to_excel('scraped_data.xlsx', index=False)

def check_existing():
    with open('PHD northtexas.txt') as file:
          urls = [line.strip() for line in file.readlines()]
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
    df1 = pd.read_excel('masters.xlsx')
    df2 = pd.read_excel('masters1.xlsx')

    difference = df1[df1!=df2]
    print (difference)

file_path = 'linksAbertay.txt'

# Open the file and read URLs
with open(file_path, 'r') as file:
    urls = file.readlines()

# Get initial system usage
initial_ram, initial_cpu = get_initial_system_usage()

# Get initial network usage
initial_sent, initial_received = get_initial_network_usage()
# Process each URL
for url in urls:
    url = url.strip()  # Remove leading/trailing whitespace
    content = extract_content(url)
    if content is not None:
        print(url + " " + content)
    else:
        print(url + " Error: Unable to extract content")

# Get final system usage
final_ram, final_cpu = get_final_system_usage(initial_ram, initial_cpu)

# Print system usage during code execution
print("RAM Usage during execution: {:.2f} MB".format(final_ram / (1024 * 1024)))
print("CPU Usage during execution: {:.2f}%".format(final_cpu))
# Get final network usage
final_sent, final_received = get_final_network_usage(initial_sent, initial_received)

# Print network usage during code execution
print("Data Uploaded during execution: {:.2f} MB".format(final_sent / (1024 * 1024)))
print("Data Downloaded during execution: {:.2f} MB".format(final_received / (1024 * 1024)))
