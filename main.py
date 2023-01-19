import csv
import requests
from bs4 import BeautifulSoup

url = 'https://books.toscrape.com/catalogue/the-project_856/index.html'

class Produit():   
    def __init__(self, page_url, soup):
        self.page_url = page_url
        self.universal_product_code = ''
        self.price_excluding_tax = ''
        self.price_including_tax = ''
        self.number_available = ''

        body = soup.html.body

        table_details = body.find('table','table-striped')
        correspondance = {'UPC': 'universal_product_code',
            'Price (excl. tax)': 'price_excluding_tax',
            'Price (incl. tax)': 'price_including_tax',
            'Availability': 'number_available',
        }
        for ligne in table_details.find_all('tr') :
            cle = ligne.th.text
            valeur = ligne.td.text

            if cle in correspondance:
                setattr(self,correspondance[cle],valeur)
        
def main():
    reponse = requests.get(url)
    if reponse.ok:
        soup = BeautifulSoup(reponse.text, features="html.parser")
        produit = Produit(url, soup)
        print(produit.universal_product_code)


main()