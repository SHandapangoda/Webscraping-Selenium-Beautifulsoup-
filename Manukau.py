from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from openpyxl import Workbook
import requests
from bs4 import BeautifulSoup
def get_details():

#from webdriver_manager.chrome import ChromeDriverManager

# Configure Chrome WebDriver
    service = Service(r'chromedriver.exe')  # Replace with the path to your chromedriver executable
    driver = webdriver.Chrome(service=service)

# Read URLs from the text file
    with open("linksManukau1", "r") as file:
        urls = [line.strip() for line in file.readlines()]

# Define a dictionary of elements and their respective selectors
    selectors = {
        "Course Name":'/html/body/div/div[2]/div/div[1]/main/div[3]/div[2]/div/div[1]/div/div/div[4]/div/div/div/div/ul/li[1]/div',
        "Course Fees": '/html/body/div[1]/div[2]/div/div[1]/main/div[3]/div[2]/div/div[1]/div/div/div[5]/div/div/div/div/ul/li[2]/div',
        "Start Dates": '/html/body/div/div[2]/div/div[1]/main/div[3]/div[2]/div/div[1]/div/div/div[3]/div/div/div/div/ul/li[2]/div[1]/p',
        #"Summary": '/html/body/div/div[2]/div/div[1]/main/div[3]/div[3]/div[2]/div/div/div[2]',
        "Entry Req": '/html/body/div[1]/div[2]/div/div[1]/main/div[3]/div[3]/div[4]/div',
        "Location": '/html/body/div[1]/div[2]/div/div[1]/main/div[3]/div[2]/div/div[1]/div/div/div[2]/div/div/div/div/ul/li[3]/div/p/a'


    # Add more elements with their respective selectors as needed
    }

# Create a new workbook
    workbook = Workbook()
# Create a new worksheet
    worksheet = workbook.active

# Write the header row
    header_row = ["Course Website URL"] + list(selectors.keys())
    worksheet.append(header_row)

# Iterate over the URLs
    for url in urls:
    # Load the webpage
        driver.get(url)
    # Create a new row for each URL
        data_row = [url]
    # Iterate over the elements and extract the desired information
        for element_name, selector in selectors.items():
        # Extract the text content under the specified selector
            try:
            # Execute JavaScript code to extract data under the specified selector
                script = f"""
                const element = document.evaluate('{selector}', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                // Extract the text content from the element under the specified selector
                const extractedData = element ? element.textContent.trim() : "";
                return extractedData;
            """
                data = driver.execute_script(script)
            except:
                data = ""
        # Append the extracted data to the data
            data_row.append(data)
    # Write the data row to the worksheet
        worksheet.append(data_row)

# Save the workbook as an Excel file
    workbook.save("test.xlsx")

# Close the browser
    driver.quit()

def check_status():
    session = requests.Session()
    with open('linksmanukau1','r') as file:
        urls = [line.strip() for line in file.readlines()]
           # Create a session to handle cookies
    session = requests.Session()
    for url in urls:
        response = session.get(url, allow_redirects=False)
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
            
def crawl():
    url = 'https://www.manukau.ac.nz/study/areas-of-study'
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    filter_word = 'https://www.manukau.ac.nz/study/areas-of-study/culinary-hospitality-and-baking/'
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and filter_word in href:
            
            
            print(href)

crawl()