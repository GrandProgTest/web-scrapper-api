from functools import wraps
from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from main import setup_driver, fetch_page, extract_table_data

app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["20 per minute"]
)

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/search', methods=['GET'])
@limiter.limit("20 per minute")
def search():
    firm_name = request.args.get('firm_name')

    if not firm_name:
        return jsonify({"error": "No firm name provided"}), 400

    chromedriver_path = './chromedriver-win64/chromedriver.exe'
    url = "https://projects.worldbank.org/en/projects-operations/procurement/debarred-firms"
    
    driver = setup_driver(chromedriver_path)
    soup = fetch_page(driver, url)
    data = extract_table_data(soup)
    driver.quit()

    filtered_data = [firm for firm in data if firm_name.lower() in firm["Firm Name"].lower()]
    hits = len(filtered_data)

    return jsonify({"hits": hits, "results": filtered_data})

if __name__ == "__main__":
    app.run(debug=True)