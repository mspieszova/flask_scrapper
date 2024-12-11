from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup



app = Flask(__name__)

@app.route('/')
def home():
    
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    try:
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
            if title and link:
                results.append({'title': title, 'link': link})               
        return jsonify(results)
    except Exception as e:       
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':    
    app.run(host='0.0.0.0', port=5000, debug=True)
