import requests
from bs4 import BeautifulSoup
from collections import UserDict

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
    
    def __init__(self, page_url, header_extend = None ):
        self.data = {'product_page_url': page_url}

        if header_extend is not None:
            self.headers.extend(header_extend)

        reponse = requests.get(page_url)
        if reponse.ok:
            self.soup = BeautifulSoup(reponse.text, features="html.parser")

            self.data["title"] = self.scrap_title()
            self.data["product_description"] = self.scrap_product_description()
            self.data["category"] = self.scrap_category()
            self.data["review_rating"] = self.scrap_review_rating()
            self.data["image_url"] = self.scrap_image_url()
            self.data["universal_product_code"] = self.scrap_universal_product_code()
            self.data["price_excluding_tax"] = self.scrap_price_excluding_tax()
            self.data["price_including_tax"] = self.scrap_price_including_tax()
            self.data["number_available"] = self.scrap_number_available()
        else:
            print('Erreur de requete')
            #Statut d'erreur ?

    def scrap_title(self):
        return self.soup.html.body.find("h1").text.strip()
    
    def scrap_product_description(self):
        titre_description = self.soup.find(id="product_description")
        return titre_description.next_sibling.next_sibling.text.strip()
    
    def scrap_category(self):
        breadcrumb = self.soup.find("ul", "breadcrumb")
        return breadcrumb.find_all("li")[-2].text.strip()
    
    def scrap_review_rating(self):
        star_rating = self.soup.html.find("p", "star-rating")["class"][-1]
        trad_numbers = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
        return trad_numbers[star_rating]
    
    def scrap_image_url(self):
        return self.soup.body.find(id="product_gallery").find("img")["src"]

    def get_elements_tables_striped(self, text):
        table_details = self.soup.html.body.find("table", "table-striped")
        return table_details.find("th", text=text).parent.td.text.strip()
    
    def scrap_universal_product_code(self):
        return self.get_elements_tables_striped("UPC")
    
    def scrap_price_excluding_tax(self):
        return self.get_elements_tables_striped("Price (excl. tax)")

    def scrap_price_including_tax(self):
        return self.get_elements_tables_striped("Price (incl. tax)")

    def scrap_number_available(self):
        return self.get_elements_tables_striped("Availability")
