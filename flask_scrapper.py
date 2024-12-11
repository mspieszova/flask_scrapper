from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save_results():
    """
    Save JSON data to a file when received via POST request.
    """
    data = request.json
    with open('results.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return jsonify({"message": "Data byla uložena"})

@app.route('/search', methods=['GET'])
def search():
    """
    Perform a Google search and return results as JSON.
    """
    query = request.args.get('query')
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    }
    response = requests.get(f"https://www.google.com/search?q={query}", headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    results = []
    for g in soup.find_all('div', class_='tF2Cxc'):
        title = g.find('h3').text if g.find('h3') else None
        link = g.find('a')['href'] if g.find('a') else None
        snippet = g.find('span', class_='aCOpRe').text if g.find('span', class_='aCOpRe') else None
        if title and link:
            results.append({'title': title, 'link': link, 'snippet': snippet})
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)