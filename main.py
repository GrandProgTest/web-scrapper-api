from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

def setup_driver(chromedriver_path):
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--disable-gpu")  
    chrome_options.add_argument("--no-sandbox")  
    chrome_options.add_argument("--disable-dev-shm-usage")  
    
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def fetch_page(driver, url):
    driver.get(url)
    time.sleep(5)  
    return BeautifulSoup(driver.page_source, 'html.parser')

def extract_table_data(soup):
    table_container = soup.find('div', class_='k-grid-content k-auto-scrollable')
    if not table_container:
        print("No se encontró el div con la clase 'k-grid-content k-auto-scrollable'.")
        return []

    tbody = table_container.find('tbody', role='rowgroup')
    if not tbody:
        print("No se encontró el tbody dentro del div 'k-grid-content k-auto-scrollable'.")
        return []

    rows = tbody.find_all('tr', attrs={'role': 'row'})
    data = []
    for row in rows:
        columns = row.find_all('td', attrs={'role': 'gridcell'})
        if len(columns) > 0:
            firm_data = {
                "Firm Name": columns[0].text.strip(),
                "Additional Info": columns[1].text.strip(),
                "Address": columns[2].text.strip(),
                "Country": columns[3].text.strip(),
                "From Date": columns[4].text.strip(),
                "To Date": columns[5].text.strip(),
                "Grounds": columns[6].text.strip()
            }
            data.append(firm_data)
    return data

def print_data(data):
    for firm in data:
        for key, value in firm.items():
            print(f"{key}: {value}")
        print("-" * 50)

def main():
    chromedriver_path = './chromedriver-win64/chromedriver.exe'
    url = "https://projects.worldbank.org/en/projects-operations/procurement/debarred-firms"
    
    driver = setup_driver(chromedriver_path)
    soup = fetch_page(driver, url)
    data = extract_table_data(soup)
    print_data(data)
    driver.quit()

if __name__ == "__main__":
    main()