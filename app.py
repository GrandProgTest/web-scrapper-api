from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from main import main

app = Flask(__name__)
CORS(app)

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

    data = main("worldbank")
    filtered_data = [firm for firm in data if firm_name.lower() in firm["Firm Name"].lower()]
    hits = len(filtered_data)

    return jsonify({"hits": hits, "results": filtered_data})

@app.route('/search_ofac', methods=['GET'])
@limiter.limit("20 per minute")
def search_ofac():
    firm_name = request.args.get('firm_name')

    if not firm_name:
        return jsonify({"error": "No firm name provided"}), 400

    data = main("ofac", firm_name)
    filtered_data = [firm for firm in data if firm_name.lower() in firm["Name"].lower()]
    hits = len(filtered_data)

    return jsonify({"hits": hits, "results": filtered_data})

@app.route('/search_bank_more_open', methods=['GET'])
@limiter.limit("20 per minute")
def search_bank_more_open():
    firm_name = request.args.get('firm_name')

    if not firm_name:
        return jsonify({"error": "No firm name provided"}), 400

    data = main("worldbank")
    filtered_data = [firm for firm in data if firm_name.lower() in firm["Firm Name"].lower()]
    hits = len(filtered_data)

    return jsonify({"hits": hits, "results": filtered_data})

@app.route('/search_ofac_more_open', methods=['GET'])
@limiter.limit("20 per minute")
def search_ofac_more_open():
    firm_name = request.args.get('firm_name')

    if not firm_name:
        return jsonify({"error": "No firm name provided"}), 400

    data = main("ofac", firm_name)
    filtered_data = [firm for firm in data if firm_name.lower() in firm["Name"].lower()]
    hits = len(filtered_data)

    return jsonify({"hits": hits, "results": filtered_data})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)