import csv
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from produit import Produit
import os
import re
from datetime import datetime

DIR_DATA = "Data"
HOME_URL = "https://books.toscrape.com/"

def export_data_from_category(url_category, dir_path):
    result = re.search(r".+/([a-z\-]+)_[\d]+/(index\.html)?$", url_category)
    category_name = result.group(1)
    file_path = f"{dir_path}/data-{category_name}.csv"

    with open(file_path, "w", encoding="utf-8", newline="") as output_csv:
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

def get_urls_categories(home_url):
    reponse = requests.get(home_url)
    if reponse.ok:
        soup = BeautifulSoup(reponse.text, features="html.parser")
        list_category = soup.find(True, class_="side_categories").ul.li.ul.find_all('li')
        return [urljoin(home_url, category.a['href']) for category in list_category]

    else:
        return None



def main():

    time_code = datetime.now().strftime("%y%m%d%H%M%S")
    dir_path = f"{DIR_DATA}/{time_code}"
    os.makedirs(dir_path)
    
    for url_category in get_urls_categories(HOME_URL)[:3]:
        export_data_from_category(url_category,dir_path)

main()
