import requests
from bs4 import BeautifulSoup
import pandas as pd

main_url = 'https://romebusinessschool.com/master-and-mba-fees/'
response = requests.get(main_url)
soup = BeautifulSoup(response.text, 'html.parser')

fee_table_div = soup.find('div', class_='fee-table-desktop')

if fee_table_div:
    # Initialize a list to store all details
    details = {
        'URL': [],
        'Text': [],
        'Language': [],
        'Fee': []
    }

    # Find all 'tr' tags within the fee_table_div
    for row in fee_table_div.find_all('tr'): # type: ignore
        # Extract individual elements from the row
        cols = row.find_all('td')
        
        if len(cols) >= 4:  # Ensure there are enough columns to extract data
            # Extracting URL and text from the first column ('td')
            link = cols[0].find('a')
            if link:
                href = link.get('href')
                if href and "https://romebusinessschool.com/" in href:
                    # Extracting additional details from other columns
                    language = cols[1].get_text().strip()
                    fee = cols[3].get_text().strip()
                    
                    # Append all details to the list
                    details['URL'].append(href) 
                    details['Text'].append(link.get_text()) 
                    details['Language'].append(language) 
                    details['Fee'].append(fee) 
                    #details.append((href, link.get_text().strip(), language, fee))
    df = pd.DataFrame(details)

    

    for index, row in df.iterrows():
        print(f"URL: {row['URL']}")
        print(f"Text: {row['Text']}")
        print(f"Language: {row['Language']}")
        print(f"Fee: {row['Fee']}")
        print()
    
    # Save DataFrame to Excel
    excel_file = 'master_and_mba_fees.xlsx'
    df.to_excel(excel_file, index=False)
    print(f"Data successfully saved to {excel_file}")
else:
    print("No div with class 'fee-table-desktop' found on the page.")