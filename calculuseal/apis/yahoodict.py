import requests
from bs4 import BeautifulSoup

def lookup(word):
    # receive target url, (an extra token after https://tw.dictionary.search.yahoo.com/)
    resp = requests.get('https://tw.dictionary.search.yahoo.com/', headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3664.3 Safari/537.36'})
    html = BeautifulSoup(resp.text, 'html.parser')
    target_url = html.find(id='sf').attrs.get('action')

    # query the dictionary
    resp = requests.get(target_url, params={'p': word})
    definitions = BeautifulSoup(resp.text, 'html.parser').find('div', class_='dictionaryExplanation')
    return definitions.text
