import os
from datetime import datetime
from category import *
import config


def main():
    debut = datetime.now()

    time_code = datetime.now().strftime("%y%m%d%H%M%S")
    dir_path = f"{config.DIR_DATA}/{time_code}"
    os.makedirs(dir_path)

    for url_category in get_urls_categories(config.HOME_URL):
        export_data_from_category(url_category, dir_path, load_img=True)

    fin = datetime.now()
    print(f"Données extraites en {fin - debut}")
main()
