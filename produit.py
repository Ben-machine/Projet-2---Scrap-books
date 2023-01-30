import requests
from bs4 import BeautifulSoup
from collections import UserDict
from urllib.parse import urljoin
import re
import os
import config


class Produit(UserDict):
    """La classe représente un produit du site Book to scrap.

    Attributs:
        data : dict
            dictionnaire regroupant les informations sur le produit
        headers : list
            liste des champs scrapés et clés du dictionnaire "data"
        soup : BeautifulSoup 
            "soup" de la page web du produit

    Methods :
        scrap_[element]():
            stock dans data [element] (liste des éléments scrappables 
            dans headers), \n 
            scrappé depuis l'objet soup
        
        import_img():
            export dans le dossier fourni par config.py l'image importée
            depuis "img_url"
    """    
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

    def __init__(self, page_url : str, header_extend: list[str] = None) \
            -> None:
        """Construit le dictionnaire des attributs de Produit

        Args:
            page_url (str): url du produit sur le site
            header_extend (list of string, optional): liste des informations 
            additionnelles à extraire. Defaults to None.
        """        
        self.data = {"product_page_url": page_url}

        if header_extend is not None:
            self.headers.extend(header_extend)

        reponse = requests.get(page_url)
        if reponse.ok:
            reponse.encoding = config.FILE_ENCODING
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
        gallery = self.soup.body.find(id="product_gallery")
        url_relative = gallery.find("img")["src"]
        if self["product_page_url"]:
            return urljoin(self["product_page_url"], url_relative)
        else:
            return url_relative

    #Extrait directement les données issues de la seconde colonne du tableau
    # "Product information" recherché à partir de la clé en première colonne
    def __get_elements_tables_striped(self, text):
        table_details = self.soup.html.body.find("table", "table-striped")
        return table_details.find("th", text=text).parent.td.text.strip()

    def scrap_universal_product_code(self):
        return self.__get_elements_tables_striped("UPC")

    def scrap_price_excluding_tax(self):
        text = self.__get_elements_tables_striped("Price (excl. tax)")
        result = re.search(r"([\d\.]+)", text)
        return result.group(1)

    def scrap_price_including_tax(self):
        text = self.__get_elements_tables_striped("Price (incl. tax)")
        result = re.search(r"([\d\.]+)", text)
        return result.group(1)

    def scrap_number_available(self):
        text = self.__get_elements_tables_striped("Availability")
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
