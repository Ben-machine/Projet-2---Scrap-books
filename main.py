import csv
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from produit import Produit

url = "https://books.toscrape.com/catalogue/the-project_856/index.html"

def main():
    chemin_sortie = "Data/data.csv"

    url_category = "https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html"
    #url_category = "https://books.toscrape.com/catalogue/category/books/science-fiction_16/index.html"
    
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
                pager = soup.html.body.find('ul', 'pager')
                if pager:
                    url_next_page = False
                    #url_next_page = pager.find('li','next').a['href']
                else:
                    url_next_page = False
            else:
                break
                
main()
