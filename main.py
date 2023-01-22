import csv
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from produit import Produit

chemin_sortie = "Data/data.csv"

def export_data_from_category(url_category):

    with open(chemin_sortie, "w", encoding="utf-8", newline="") as output_csv:
        writer = csv.DictWriter(
            output_csv,
            fieldnames=Produit.headers,
            restval="Not Found",
            extrasaction="ignore",
        )
        writer.writeheader()

        url_next_page = url_category
        while url_next_page:
            reponse = requests.get(url_next_page)
            if reponse.ok:
                soup = BeautifulSoup(reponse.text, features="html.parser")        
                titles_book = soup.body.section.find_all('h3')
                
                for title_h3 in titles_book:
                    url_produit_relative = title_h3.a['href']
                    url_produit_absolute = urljoin(url_next_page,url_produit_relative)
                    produit = Produit(url_produit_absolute)
                    writer.writerow(produit.data)

                soup = BeautifulSoup(reponse.text, features="html.parser")        
                pager_next = soup.html.body.find('li','next')
                if pager_next:
                    url_next_relative = pager_next.a['href']
                    url_next_page = urljoin(url_next_page, url_next_relative)
                else:
                    url_next_page = False
            else:
                break


def main():

    url_category = "https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html"
    #url_category = "https://books.toscrape.com/catalogue/category/books/science-fiction_16/index.html"
    #url_category = "https://books.toscrape.com/catalogue/category/books/sports-and-games_17/index.html"
    
    export_data_from_category(url_category)
                
main()
