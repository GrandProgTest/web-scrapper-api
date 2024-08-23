from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

service = Service('./chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=service)

url = "https://projects.worldbank.org/en/projects-operations/procurement/debarred-firms"
driver.get(url)

time.sleep(5)

soup = BeautifulSoup(driver.page_source, 'html.parser')

table_container = soup.find('div', class_='k-grid-content k-auto-scrollable')

if table_container:
    tbody = table_container.find('tbody', role='rowgroup')

    if tbody:
        rows = tbody.find_all('tr', attrs={'role': 'row'})

        for row in rows:
            columns = row.find_all('td', attrs={'role': 'gridcell'})
            if len(columns) > 0:
                firm_name = columns[0].text.strip()
                additional_info = columns[1].text.strip()
                address = columns[2].text.strip()
                country = columns[3].text.strip()
                from_date = columns[4].text.strip()
                to_date = columns[5].text.strip()
                grounds = columns[6].text.strip()
                
                print(f"Firm Name: {firm_name}")
                print(f"Additional Info: {additional_info}")
                print(f"Address: {address}")
                print(f"Country: {country}")
                print(f"From Date: {from_date}")
                print(f"To Date: {to_date}")
                print(f"Grounds: {grounds}")
                print("-" * 50)
    else:
        print("No se encontró el tbody dentro del div 'k-grid-content k-auto-scrollable'.")
else:
    print("No se encontró el div con la clase 'k-grid-content k-auto-scrollable'.")

driver.quit()