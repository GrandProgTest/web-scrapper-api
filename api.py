from flask import Flask, jsonify
from main import setup_driver, fetch_page, extract_table_data

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Wasfaasfasfasrldasfasfsf!'

@app.route('/scrape')
def scrape():
    chromedriver_path = './chromedriver-win64/chromedriver.exe'
    url = "https://projects.worldbank.org/en/projects-operations/procurement/debarred-firms"
    
    driver = setup_driver(chromedriver_path)
    soup = fetch_page(driver, url)
    data = extract_table_data(soup)
    driver.quit()
    
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)