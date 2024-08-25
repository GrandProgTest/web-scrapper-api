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

def search_ofac_sanctions(driver, name):
    driver.get("https://sanctionssearch.ofac.treas.gov/")
    time.sleep(2)

    search_box = driver.find_element(By.ID, "ctl00_MainContent_txtLastName")
    search_box.clear()
    search_box.send_keys(name)

    search_button = driver.find_element(By.ID, "ctl00_MainContent_btnSearch")
    search_button.click()
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return soup

def extract_ofac_table_data(soup):
    table = soup.find('table', id='gvSearchResults')
    if not table:
        print("No se encontró la tabla de resultados.")
        return []

    rows = table.find_all('tr')
    data = []
    for row in rows:
        columns = row.find_all('td')
        if len(columns) > 0:
            result_data = {
                "Name": columns[0].text.strip(),
                "Address": columns[1].text.strip(),
                "Type": columns[2].text.strip(),
                "Programs": columns[3].text.strip(),
                "List": columns[4].text.strip(),
                "Score": columns[5].text.strip()
            }
            data.append(result_data)
    return data

def main(search_type, firm_name=None):
    chromedriver_path = './chromedriver-win64/chromedriver.exe'
    driver = setup_driver(chromedriver_path)
    
    if search_type == "worldbank":
        url = "https://projects.worldbank.org/en/projects-operations/procurement/debarred-firms"
        soup = fetch_page(driver, url)
        data = extract_table_data(soup)
        
    elif search_type == "ofac" and firm_name:
        soup = search_ofac_sanctions(driver, firm_name)
        data = extract_ofac_table_data(soup)
    
    else:
        driver.quit()
        return []

    driver.quit()
    return data
