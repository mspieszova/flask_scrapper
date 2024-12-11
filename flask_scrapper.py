from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup
import json
import os
import logging

# Nastavení logování
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# Cesta ke složce "vysledky" v kořenovém adresáři
RESULTS_DIR = os.path.join(os.getcwd(), "vysledky")
RESULTS_FILE = os.path.join(RESULTS_DIR, "vysledky.json")

# Logování cesty k souboru
logging.info(f"Cesta k výsledkům: {RESULTS_FILE}")

# Funkce pro vytvoření složky, pokud neexistuje
if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)
    logging.info(f"Složka vytvořena: {RESULTS_DIR}")
else:
    logging.info(f"Složka již existuje: {RESULTS_DIR}")

@app.route('/')
def home():
    logging.info("Načítám hlavní stránku.")
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save():
    try:
        data = request.json
        logging.info(f"Ukládám data: {data}")

        # Uložení dat do souboru
        with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        logging.info(f"Data úspěšně uložena do souboru: {RESULTS_FILE}")
        return jsonify({"message": "Data byla uložena.", "file_path": RESULTS_FILE})

    except Exception as e:
        logging.error(f"Chyba při ukládání dat: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/search', methods=['GET'])
def search():
    try:
        query = request.args.get('query')
        logging.info(f"Vyhledávám dotaz: {query}")

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
        
        logging.info(f"Nalezeno {len(results)} výsledků.")
        return jsonify(results)

    except Exception as e:
        logging.error(f"Chyba při vyhledávání: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    logging.info("Spouštím aplikaci...")
    app.run(host='0.0.0.0', port=5000, debug=True)
