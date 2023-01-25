import os
from datetime import datetime
from category import *

DIR_DATA = "Data"
HOME_URL = "https://books.toscrape.com/"

def main():

    time_code = datetime.now().strftime("%y%m%d%H%M%S")
    dir_path = f"{DIR_DATA}/{time_code}"
    os.makedirs(dir_path)

    for url_category in get_urls_categories(HOME_URL)[:3]:
        export_data_from_category(url_category,dir_path)

main()
