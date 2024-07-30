from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
from lxml import html
import json
# Initialize Chrome driver



def get_url():
    driver = webdriver.Firefox()

    mother_url = ["https://www.oxfordinternational.com/search?universities%5B%5D=5569&search=&study_levels%5B%5D=1207&study_levels%5B%5D=611&study_levels%5B%5D=584&page=1","https://www.oxfordinternational.com/search?universities%5B%5D=5569&search=&study_levels%5B%5D=1207&study_levels%5B%5D=611&study_levels%5B%5D=584&page=2","https://www.oxfordinternational.com/search?universities%5B%5D=5569&search=&study_levels%5B%5D=1207&study_levels%5B%5D=611&study_levels%5B%5D=584&page=3","https://www.oxfordinternational.com/search?universities%5B%5D=5569&search=&study_levels%5B%5D=1207&study_levels%5B%5D=611&study_levels%5B%5D=584&page=4","https://www.oxfordinternational.com/search?universities%5B%5D=5569&search=&study_levels%5B%5D=1207&study_levels%5B%5D=611&study_levels%5B%5D=584&page=5"]

def get_url():
    
    mother_url = ["https://www.oxfordinternational.com/search?universities%5B%5D=5569&search=&study_levels%5B%5D=611&page=1"]

    matching_urls = []
    keywords = ["https://www.oxfordinternational.com/degrees/"]
    for url in mother_url:
   # Open the mother URL
        driver.get(url)
        time.sleep(10)
   # Find all anchor elements
        anchors = driver.find_elements(By.TAG_NAME, 'a')

   # Extract URLs containing the keywords
        
        for anchor in anchors:
            href = anchor.get_attribute('href')
            if href and any(keyword in href for keyword in keywords):
                matching_urls.append(href)

                #print(href)
        matching_urls = list(set(matching_urls))


#saving the extracted URLs
    with open('oieglinks07-30.txt', 'w') as file:
        for url in matching_urls:
            file.write(f"{url}\n")  

    driver.close()  
    return matching_urls
    
#get URLs of the main University
def get_ref_url():
    driver = webdriver.Firefox()
    urls = []
    #provide the system URLs 
    with open('oieglinks.txt', 'r') as file:
        for url in file:
            urls.append(url)
    # Directly initialize urls list, or read from a file if necessary
      # or replace with code to read URLs from a file if needed

    # The following commented-out code can be used to read URLs from a file if needed:
    '''
    # Read URLs from the file
    with open('urls.txt', 'r') as file:
  # Strip newline characters and add to the list
    '''
    

        print(matching_urls)
        return matching_urls

def get_ref_url():
    urls = get_ref_url()
    urls = []
    '''
    # Read URLs from the file
    with open('urls.txt', 'r') as file:
        for url in file:
            urls.append(url.strip())  # Strip newline characters and add to the list
'''

    matching_urls = []
    keywords = ["https://www.ravensbourne.ac.uk"]

    for url in urls:
        try:
            # Open the URL in the driver
            driver.get(url)
            time.sleep(5)  # Introducing a delay to ensure the page loads completely

            # Find all anchor elements on the page
            anchors = driver.find_elements(By.TAG_NAME, 'a')

            # Extract URLs containing the keywords
            for anchor in anchors:
                href = anchor.get_attribute('href')
                if href and any(keyword in href for keyword in keywords):
                    #print(matching_urls)
                    matching_urls.append(href)

        except Exception as e:
            print(f"Error processing URL {url}: {str(e)}")
    matching_urls = list(set(matching_urls))

    #file save with the existing the main university urls
    with open('oiegmainlinks.txt', 'w') as file:
        for url in matching_urls:
            file.write(f"{url}\n") 
      
    driver.close()
    return matching_urls


# before running this section please make sure to run the "get_ref_url()"    
# get the details of the main University and save to JSON

def get_details_main():

    urls = []
    #save with the main University URLs
    with open('oiegmainlinks.txt', 'r') as file:
        for url in file:
            urls.append(url.strip())
    urls = get_ref_url()

    data = []

    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise error for bad response status

            tree = html.fromstring(response.content)
            soup = BeautifulSoup(response.text, 'html.parser')
            name = tree.cssselect('#block-entityviewcontent > div > div > div > h1')
            entry = soup.find_all('div', class_='border border-solid border-color-black-10 mb-2')
            fees = soup.find_all('span', class_='c-course-overview-item__field')
            int_fee_text = None
            for fee in fees:
                text = fee.get_text(strip=True)
                if text.startswith("INT:"):
                    # Extract the part after "INT:"
                    int_fee_text = text.split("INT:")[1].strip().replace('FT','').strip().replace('£', '').strip().replace(',','').strip()
                    break 
            if int_fee_text:
                print(url, int_fee_text)
            else:
                fees = soup.find_all('div', class_='wysiwyg | pt-2 pr-8 pb-8 pl-12')
                for fee in fees:
                    text = fee.get_text(strip=True)
                    if text.startswith("5 semesters:") or text.startswith("4 semesters:"):
                        int_fee_text = text.split("5 semesters:")[1].strip().replace('FT','').strip().replace('£', '').strip().replace(',','').strip()
                        print(url,int_fee_text)
  


            soup = BeautifulSoup(response.text, 'html.parser')
            entry = soup.find_all('div', class_='border border-solid border-color-black-10 mb-2')
            fees = soup.find_all('span', class_='c-course-overview-item__field')
            
            if fees and len(fees) >= 5:
                fees_value = fees[4].get_text().strip()
            else:
                fees_value = 'Not found'


            for div in entry:
                title = div.find('h3').text.strip()
                content_paragraphs = div.find('div', class_='wysiwyg').find_all('p')
                
                if title == 'Entry requirements':
                    content = "\n".join([paragraph.text.strip() for paragraph in content_paragraphs])

            data.append({'Main_URL': url, 'Name': name[0].text_content().strip(), 'Fees': int_fee_text, 'Entry': content})
          

                    data.append({'URL': url, 'Fees': fees_value, 'Title': title, 'Entry': content})


        except requests.RequestException as e:
            print(f"Error fetching URL {url}: {str(e)}")
    #print(urls)
    df = pd.DataFrame(data)

    #rename the file when running 
    df.to_json('main2024-07-30.json')
    return df


#get details of the OIEG and save to JSON file 
def get_details():
    urls = []

    #provide the all existing courses
    with open('oieglinks.txt', 'r') as file:
        for url in file:
            urls.append(url.strip())

    return data

def get_details():
    urls = get_ref_url()

    data = []

    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise error for bad response status

            tree = html.fromstring(response.content)
            names = tree.xpath('/html/body/div[2]/div/div[1]/div[2]/div[1]/div[1]/div[2]/p[2]')
            starts = tree.xpath('/html/body/div[2]/div/div[1]/div[2]/div[1]/div[3]/div[2]/p[2]')

            if names:
                name = names[0].text_content().strip()
            else:
                name = 'Not found'

            if starts:
                start = starts[0].text_content().strip()
            else:
                start = 'Not found'

            data.append({'URL': url, 'Name': name, 'Start': start})

        except requests.RequestException as e:
            print(f"Error fetching URL {url}: {str(e)}")
        except Exception as e:
            print(f"Error processing URL {url}: {str(e)}")
    df = pd.DataFrame(data)
    df.to_json('OIEG2024-07-30.json')
  
    print(df)
    return df

#check missing courses
def url_read_for_missing(file_path):
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file if line.strip()]
    return urls
def check_missing():
    new_urls = get_url()
    urls_file_path = 'oieglinks.txt' # give the existing system files with URLs
    old_urls = url_read_for_missing(urls_file_path)
    
    # Convert lists to sets for comparison
    new_set = set(new_urls)
    old_set = set(old_urls)
    
    # Find missing URLs
    missing = new_set - old_set
    
    # Print missing URLs
    for url in missing:
        print(url)
    return missing

get_details_main()
#How to run 

def load_json_to_df(filename):
    """Load a JSON file into a DataFrame."""
    with open(filename, 'r') as file:
        data = json.load(file)
    return pd.DataFrame(data)

def compare_json_files(file1, file2, output_excel):
    # Load the JSON files
    df1 = load_json_to_df(file1)
    df2 = load_json_to_df(file2)
    
    # Merge DataFrames on 'Main_URL'
    merged_df = pd.merge(df1, df2, on='Main_URL', suffixes=('_old', '_new'), how='outer', indicator=True)


    # Find differences
    changes = merged_df[merged_df['_merge'] != 'both']
    differences = merged_df[merged_df['_merge'] == 'both']
    
    # Columns to compare
    diff_columns = ['Name_old', 'Name_new', 'Fees_old', 'Fees_new', 'Entry_old', 'Entry_new']
    differences = differences[diff_columns]
    
    # Create a column that highlights differences
    for col in ['Name', 'Fees', 'Entry']:
        differences[f'{col}_changed'] = differences[f'{col}_old'] != differences[f'{col}_new']
    
    # Save the result to an Excel file
    with pd.ExcelWriter(output_excel) as writer:
        changes.to_excel(writer, sheet_name='Changes', index=False)
        differences.to_excel(writer, sheet_name='Differences', index=False)


compare_json_files('main2024-07-30.json', 'main2024-08-30.json', 'comparison_output.xlsx')


    return data

def export_to_excel():
    # Get data from both functions
    details_main = get_details_main()
    details = get_details()

    # Convert data to DataFrames
    df_main = pd.DataFrame(details_main)
    df = pd.DataFrame(details)

    # Export DataFrames to Excel
    with pd.ExcelWriter('details.xlsx') as writer:
        df_main.to_excel(writer, sheet_name='Main Details', index=False)
        df.to_excel(writer, sheet_name='Other Details', index=False)

# Call function to export details to Excel
export_to_excel()

