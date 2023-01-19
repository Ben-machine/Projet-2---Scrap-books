import csv
import requests
from bs4 import BeautifulSoup

url = 'https://books.toscrape.com/catalogue/the-project_856/index.html'

class Produit():   
    def __init__(self, soup):
        self.title = soup.find('title').text

def main():
    reponse = requests.get(url)
    if reponse.ok:
        soup = BeautifulSoup(reponse.text, features="html.parser")
        produit = Produit(soup)
        print(produit.title)

main()