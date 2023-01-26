import requests
from bs4 import BeautifulSoup
from collections import UserDict
from urllib.parse import urljoin
import re
import os
import config


class Produit(UserDict):
    headers = [
        "product_page_url",
        "universal_product_code",
        "title",
        "price_including_tax",
        "price_excluding_tax",
        "number_available",
        "product_description",
        "category",
        "review_rating",
        "image_url",
    ]

    def __init__(self, page_url, header_extend=None):
        self.data = {"product_page_url": page_url}

        if header_extend is not None:
            self.headers.extend(header_extend)

        reponse = requests.get(page_url)
        if reponse.ok:
            self.soup = BeautifulSoup(reponse.text, features="html.parser")

            for element in self.headers:
                scrap_func = f"scrap_{element}"
                if hasattr(self, scrap_func):
                    func_scrap = getattr(self, scrap_func)
                    self.data[element] = func_scrap()
        else:
            print(f"Erreur de requete sur la page {page_url}")
            # Statut d'erreur ?

    def scrap_title(self):
        return self.soup.html.body.find("h1").text.strip()

    def scrap_product_description(self):
        titre_description = self.soup.find(id="product_description")
        if titre_description is not None:
            return titre_description.next_sibling.next_sibling.text.strip()
        else:
            return ''

    def scrap_category(self):
        breadcrumb = self.soup.find("ul", "breadcrumb")
        return breadcrumb.find_all("li")[-2].text.strip()

    def scrap_review_rating(self):
        star_rating = self.soup.html.find("p", "star-rating")["class"][-1]
        trad_numbers = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
        return trad_numbers[star_rating]

    def scrap_image_url(self):
        url_relative = self.soup.body.find(id="product_gallery").find("img")["src"]
        if self["product_page_url"]:
            return urljoin(self["product_page_url"], url_relative)
        else:
            return url_relative

    def get_elements_tables_striped(self, text):
        table_details = self.soup.html.body.find("table", "table-striped")
        return table_details.find("th", text=text).parent.td.text.strip()

    def scrap_universal_product_code(self):
        return self.get_elements_tables_striped("UPC")

    def scrap_price_excluding_tax(self):
        text = self.get_elements_tables_striped("Price (excl. tax)")
        result = re.search(r"([\d\.]+)", text)
        return result.group(1)

    def scrap_price_including_tax(self):
        text = self.get_elements_tables_striped("Price (incl. tax)")
        result = re.search(r"([\d\.]+)", text)
        return result.group(1)

    def scrap_number_available(self):
        text = self.get_elements_tables_striped("Availability")
        result = re.search(r"(\d+)", text)
        return result.group(1)

    def import_img(self):
        reponse = requests.get(self["image_url"])
        if reponse.ok:
            normalized_category = self["category"].lower().replace(" ", "-")
            dir_path = f"{config.DIR_IMG}/{normalized_category}"
            os.makedirs(dir_path, exist_ok=True)
            file_path = f"{dir_path}/{self['universal_product_code']}.jpg"
            with open(file_path, "wb") as output_img:
                output_img.write(reponse.content)
            return True
        else:
            return False
