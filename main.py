import csv
import requests
from bs4 import BeautifulSoup

url = 'https://books.toscrape.com/catalogue/the-project_856/index.html'

class Produit():   
    def __init__(self, page_url, soup):
        self.page_url = page_url
        self.title = ''
        self.universal_product_code = ''
        self.price_excluding_tax = 0
        self.price_including_tax = 0
        self.number_available = 0
        self.product_description = ''
        self.category = ''

        self.review_rating = 0
        self.image_url = ''

        body = soup.html.body

        self.title = body.find('h1')
        self.product_description = body.find(id='product_description').next_sibling.next_sibling.text

        breadcrumb = body.find('ul','breadcrumb')
        self.category = breadcrumb.find_all('li')[-2].text

        star_rating = body.find('p','star-rating')['class'][-1]
        trad_numbers = {'One':1, 'Two':2, 'Three':3, 'Four':4, 'Five':5}
        self.review_rating = trad_numbers[star_rating]

        self.image_url = body.find(id='product_gallery').find('img')['src']

        table_details = body.find('table','table-striped')
        correspondance_table = {'UPC': 'universal_product_code',
            'Price (excl. tax)': 'price_excluding_tax',
            'Price (incl. tax)': 'price_including_tax',
            'Availability': 'number_available',
        }
        for ligne in table_details.find_all('tr') :
            cle = ligne.th.text
            valeur = ligne.td.text

            if cle in correspondance_table:
                setattr(self,correspondance_table[cle],valeur)
        
def main():
    reponse = requests.get(url)
    if reponse.ok:
        soup = BeautifulSoup(reponse.text, features="html.parser")
        produit = Produit(url, soup)
        #print(produit.image_url)


main()