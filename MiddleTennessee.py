from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.ui import Select 
import time

def get_details():
# Use Chrome driver
    driver = webdriver.Firefox()
    url = "https://www.mtsu.edu/search-program/"
    driver.get(url)
    select = driver.find_element(by=By.XPATH,value='/html/body/div[1]/div/div/div/main/article/div/div[1]/div/div/div/div[2]/div[3]/div/div/select')

    select.send_keys("On Ground")
    time.sleep(5)
# Extract program details
    links = driver.find_elements(By.CLASS_NAME, 'jet-listing-dynamic-link__link')
    modes = driver.find_elements(By.CLASS_NAME, 'jet-listing-dynamic-field__content')
    data = []
    for link,mode in zip (links,modes):
        program_url = link.get_attribute('href')
        program_name = link.find_element(By.CLASS_NAME, 'jet-listing-dynamic-link__label').text
        program_mode = mode.text.strip()
 
        print(f"Program Name: {program_name}, URL: {program_url},Program Mode: {program_mode}")
        data.append([program_url, program_name, program_mode])
    #print(f"Program Mode: {program_mode}")

    df = pd.DataFrame(data, columns=['url','Name','mode'])
    #df.to_excel('Middletennessee.xlsx')
    driver.close()

def filtered():
    url = "https://www.mtsu.edu/search-program/"
    driver = webdriver.Firefox()
    driver.get(url)

    select = driver.find_element(by=By.XPATH,value='/html/body/div[1]/div/div/div/main/article/div/div[1]/div/div/div/div[2]/div[3]/div/div/select')

    select.send_keys("On Ground")

get_details()
#
'''  
for mode in modes:
    program_mode = mode.text.strip()
    print(f"Program Mode: {program_mode}")
   ''' 

# Close the driver
    
