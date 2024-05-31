from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup
from spellchecker import SpellChecker
import re
import os
app = Flask(__name__)

# Function to get text from the soup excluding script and style tags
def get_text_from_soup(soup):
    for script in soup(["script", "style"]):
        script.extract()  # Remove these tags and their contents
    return soup.get_text()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_spelling():
    url = request.form['url']
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = get_text_from_soup(soup)

    # Clean the text
    clean_text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation

    spell = SpellChecker()

    # Add custom words to the dictionary
    custom_words = ["app", "exampleDomainWord"]  # Add more words as needed
    spell.word_frequency.load_words(custom_words)

    words = clean_text.split()
    misspelled = spell.unknown(words)

    report = []
    for word in misspelled:
        report.append(f"Misspelled word: {word}")

    return render_template('report.html', report=report)

if __name__ == '__main__':
    # Use the PORT environment variable provided by Render, default to 8080 if not available
    port = int(os.environ.get('PORT', 8080))
    # Change the host to '0.0.0.0' and port to the one specified by Render
    app.run(host='0.0.0.0', port=port, debug=True)
