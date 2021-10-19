import re
import os
import time
import math
import json
import requests
import numpy as np
from pprint import pprint
from pyfiglet import Figlet
from bs4 import BeautifulSoup
from requests.api import request
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()


def print_header():
    print("\n\n\n\n\n\n\n\n\n")
    print("=========================================================================")
    f = Figlet(font='slant')
    print(f.renderText('IKEA CRAWLER'))
    print("=========================================================================")
    time.sleep(2)

def render_page(url):
    print("\n -> Rendering website ...")

    print("\n\n=========================== WebDriver Manager ===========================\n")
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    time.sleep(3)
    r = driver.page_source
    # driver.quit()
    print("\n=========================================================================\n\n")
    print("\n -> Render DONE")

    return r


def crawl_sofa_data(sofa_html, add_unique_variant=False):

    new_sofa = {}

    # Basic Data
    sofa_data = sofa_html.find('div', class_="range-revamp-product-compact")
    new_sofa['name'] = sofa_data.attrs['data-product-name']
    new_sofa['price'] = float(sofa_data.attrs['data-price'])
    new_sofa['currencyCode'] = sofa_data.attrs['data-currency']

    # Rating value
    sofa_rating = sofa_html.find(
        'span', class_="range-revamp-average-rating")

    if sofa_rating is None:
        new_sofa['ratingValue'] = None
    else:
        new_sofa['ratingValue'] = min([float(num) for num in re.findall(
            r"[-+]?\d*\.\d+|\d+", sofa_rating.attrs['aria-label'])])

    # Rating count

    sofa_count_rating = sofa_html.find(
        'span', class_="range-revamp-average-rating__reviews")

    if sofa_count_rating is None:
        new_sofa['ratingCount'] = None
    else:
        new_sofa['ratingCount'] = min([int(num) for num in re.findall(
            r"[-+]?\d*\.\d+|\d+", sofa_count_rating.text)])

    # Sofa description (type)
    sofa_type = sofa_data.find(
        'span', class_="range-revamp-header-section__description-text")

    new_sofa['type'] = sofa_type.text

    # Web URL
    sofa_web = sofa_html.find(
        'a', class_="range-revamp-product-compact__wrapper-link")

    new_sofa['website'] = sofa_web.attrs['href']

    # insert first variant
    if add_unique_variant:

        # Sofa Image
        sofa_img = sofa_html.find(
            'img', class_="range-revamp-aspect-ratio-image__image")

        new_sofa['variants'] = [{
            'id': sofa_data.attrs['data-product-number'],
            'website': new_sofa['website'],
            'imageUrl': sofa_img.attrs['src']
        }]

    return new_sofa


def crawl_variant(url):
    
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    sofa_data = soup.find('div', class_="range-revamp-product__subgrid product-pip js-product-pip")

    sofa_images = sofa_data.find_all('img', class_="range-revamp-aspect-ratio-image__image")

    first_image = sofa_images[0].attrs['src']

    return {
        'id' : sofa_data.attrs['data-product-id'],
        'website' : url,
        'imageUrl' : first_image
    }


print_header()

# N Sofas
print("\n -> Looking for how many sofas does the page contain...")

url = 'https://www.ikea.com/es/es/cat/sofas-fu003/?filters=f-subcategories%3A10661%7C16238%7C10663'
page = render_page(url)
soup = BeautifulSoup(page, 'html.parser')
str_that_contains_n_sofas = str(soup.find_all(
    'span', class_='plp-filter-information__total-count'))
list_with_n_sofas = [int(word) for word in re.findall(
    r"\d+", str_that_contains_n_sofas) if word.isdigit()]

n_sofas = 0
if len(list_with_n_sofas) == 1:
    n_sofas = list_with_n_sofas[0]
else:
    print("[ERROR] Different candidates were found for variable n_sofas:")
    print(f"        --> {str(list_with_n_sofas)}")
    print("Exiting program...")
    exit(1)

print(f" -> A total of {n_sofas} sofas were found.")


# Request a page with all the products
print(f" -> Request page with all the sofas.")
url = url + f"&page={math.ceil(n_sofas/24)}"
page = render_page(url)

print(f" -> Parsing page.")
soup = BeautifulSoup(page, 'html.parser')
html_with_list_of_sofas = soup.find('div', class_='plp-product-list__products')

list_of_sofas = html_with_list_of_sofas.find_all(
    'div', class_="plp-fragment-wrapper")


sofas = np.empty(n_sofas, dtype=dict)

print("\n\n=========================== START SOFA CRAWLING ===========================\n")

idCount = 0
for sofa_soup in list_of_sofas:

    printProgressBar(idCount, n_sofas, prefix = 'Progress:', suffix = 'Complete', length = 50)


    sofa_html = sofa_soup.find('div', class_="plp-product-list__fragment")

    # Check the presence of variants

    if sofa_html.attrs['data-has-variants'] == 'true':

        sofas[idCount] = crawl_sofa_data(sofa_html, add_unique_variant=False)
        sofas[idCount]['variants'] = []

        variant_list_soup= sofa_soup.find('div', class_="plp-product-thumbnails")\
                                        .find_all('a',class_="plp-product-thumbnail plp-product-thumbnail--selected")

        variant_urls = [variant.attrs['href'] for variant in variant_list_soup]

        for variant_url in variant_urls:
            sofas[idCount]['variants'].append(crawl_variant(variant_url))

    else:
        sofas[idCount] = crawl_sofa_data(sofa_html, add_unique_variant=True)

    idCount += 1

print("\n\n=================================== DONE ====================================\n")

# pprint(sofas)

# json_obj = { str(sofas.tolist())[1:-1] }

path = "./data/ikea_sofas.json"
print(f" --> Writing result into the JSON file: \n        {os.path.abspath(path)}")

with open(path, 'w') as file:
    json.dump(sofas.tolist(), file, ensure_ascii=False, indent=4)

