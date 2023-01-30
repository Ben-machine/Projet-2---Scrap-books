from utils import *
from category import *
import config

@time_exec
def main():
    for url_category in get_urls_categories(config.HOME_URL):
        export_data_from_category(url_category, get_data_folder(), 
                                  load_img=False)

main()
