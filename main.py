import csv
from produit import Produit

url = "https://books.toscrape.com/catalogue/the-project_856/index.html"

def main():
    chemin_sortie = "Data/data.csv"

    produit = Produit(url)

    with open(chemin_sortie, "w", encoding="utf-8", newline="") as output_csv:
        writer = csv.DictWriter(
            output_csv,
            fieldnames=Produit.headers,
            restval="Not Found",
            extrasaction="ignore",
        )
        writer.writeheader()
        writer.writerow(produit.data)

main()
