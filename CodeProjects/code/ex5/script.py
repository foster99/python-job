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


def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
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
    percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                     (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


def render_page(url):
    """
    Renders the page with the selenium.webdriver in order to exceute the JS calls and returns the HTML source code.
    """
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
    '''
    This function visits the sofa html code and creates a new_sofa with all the information except from the variants.
    If the paramenter add_unique_variant is set to True, the function adds the sofa information as an entry of the variant list.
    '''

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
    new_sofa['website'] = sofa_data.contents[1].attrs['href']

    # Sofa Image
    sofa_img = sofa_html.find(
        'img', class_="range-revamp-aspect-ratio-image__image")
    new_sofa['imageUrl'] = sofa_img.attrs['src']

    # insert first variant
    if add_unique_variant:

        new_sofa['variants'] = [{
            'id': sofa_data.attrs['data-product-number'],
            'website': new_sofa['website'],
            'imageUrl': sofa_img.attrs['src']
        }]

    return new_sofa


def crawl_variant_urls_from_sofa(sofa) -> bool:
    '''
    This functions visits the sofa website and and crawls the variant Urls.
    For each found Url, appends a new entry to the sofa's variant list with the {"website" : url} value
    '''

    page = requests.get(sofa['website'])
    soup = BeautifulSoup(page.content, 'html.parser')

    # Try to get variants from Grid type
    sofa_variant_list = soup.find(
        'div', class_="range-revamp-product-styles__items")

    try:
        for variant in sofa_variant_list.contents:
            if (variant.name == 'a'):
                sofa['variants'].append({'website': variant.attrs['href']})
    except:
        print(
            f"[ ERROR ] The sofa \"{sofa['name']}: {sofa['type']}\" has variants on the main page, but they do not show up on the product site.")
        return False

    return True


def crawl_image_and_id_from_variants(sofa):
    '''
    This functions visits the sofa variants links located at the variants array, and crawls the "id" and "imageUrl".
    '''

    for variant in sofa['variants']:
        variant_page = requests.get(variant['website'])
        variant_soup = BeautifulSoup(variant_page.content, 'html.parser')

        variant_data = variant_soup.find(
            'div', class_="range-revamp-product__subgrid product-pip js-product-pip")
        
        variant['id'] = variant_data.attrs['data-product-id']

        variant_image_grid = variant_data.find(
            'span', class_="range-revamp-aspect-ratio-image range-revamp-aspect-ratio-image--square range-revamp-media-grid__media-image")
        
        variant['imageUrl'] = variant_image_grid.next.attrs['src']


# ============================ SCRIPT START ============================


print("\n\n\n\n\n\n\n\n\n")
print("=========================================================================")
f = Figlet(font='slant')
print(f.renderText('IKEA CRAWLER'))
print("=========================================================================")
time.sleep(2)

# ========================== COMPUTE N SOFAS  ==========================


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
    print("[ ERROR ] Different candidates were found for variable n_sofas:")
    print(f"        --> {str(list_with_n_sofas)}")
    print("Exiting program...")
    exit(1)

print(f" -> A total of {n_sofas} sofas were found.")



# ========================== REQUEST SOFAS ============================



print(f" -> Request page with all the sofas.")
url = url + f"&page={math.ceil(n_sofas/24)}"
page = render_page(url)

print(f" -> Parsing page.")
soup = BeautifulSoup(page, 'html.parser')
html_with_list_of_sofas = soup.find('div', class_='plp-product-list__products')

list_of_sofas = html_with_list_of_sofas.find_all(
    'div', class_="plp-fragment-wrapper")


# ==========================  CRAWL SOFAS  =============================


sofas = np.empty(n_sofas, dtype=dict)

print("\n\n=========================== START SOFA CRAWLING ===========================\n")

idCount = 0
sofaIds_with_variants = []
sofaIds_failed_variants = []

print("\nCrawling sofa models:")
printProgressBar(0, n_sofas-1, prefix='Progress:',
                 suffix='Complete', length=50)

for sofa_soup in list_of_sofas:

    sofa_html = sofa_soup.find('div', class_="plp-product-list__fragment")

    if sofa_html.attrs['data-has-variants'] == 'true':
        sofaIds_with_variants.append(idCount)
        sofas[idCount] = crawl_sofa_data(sofa_html, add_unique_variant=False)
    else:
        sofas[idCount] = crawl_sofa_data(sofa_html, add_unique_variant=True)

    printProgressBar(idCount, n_sofas-1, prefix='Progress:',
                     suffix='Complete', length=50)
    idCount += 1


# ==========================  CRAWL SOFA VARIANTS  =============================


print("\nCrawling sofa variants:")
printProgressBar(0, len(sofaIds_with_variants)-1,
                 prefix='Progress:', suffix='Complete', length=50)

for i, sofaId in enumerate(sofaIds_with_variants):

    sofas[sofaId]['variants'] = []
    if crawl_variant_urls_from_sofa(sofas[sofaId]):
        crawl_image_and_id_from_variants(sofas[sofaId])
    else:
        sofaIds_failed_variants.append(sofaId)

    printProgressBar(i, len(sofaIds_with_variants)-1,
                     prefix='Progress:', suffix='Complete', length=50)


# =======================  CRAWL SOFA VARIANTS ALTERNATIVE  ===========================

print("\n Retrying to crawl the failed sofa variants with an alternative strategy:")
for i, sofaId in enumerate(sofaIds_failed_variants):

    sofa_soup = list_of_sofas[sofaId]
    sofa_thumbnail_list = sofa_soup.parent.find(
        'div', class_="plp-product-thumbnails")

    try:
        for variant in sofa_thumbnail_list.contents:
            if (variant.name == 'a'):
                sofas[sofaId]['variants'].append(
                    {'website': variant.attrs['href']})

        crawl_image_and_id_from_variants(sofas[sofaId])

        print(
            f"[SUCCESS] The sofa \"{sofas[sofaId]['name']}: {sofas[sofaId]['type']}\" variants were crawled succesfully.")

    except:
        print(
            f"[ ERROR ] The alternative variant url crawling strategy failed for sofa \"{sofas[sofaId]['name']}: {sofas[sofaId]['type']}\".")

    printProgressBar(i, len(sofaIds_failed_variants)-1,
                     prefix='Progress:', suffix='Complete', length=50)

print("\n\n=================================== DONE ====================================\n")


# ===========================  WRITE DATA TO JSON FILE  =============================


path = "./data/ikea_sofas.json"
print(f" --> Writing result into the JSON file: \n  {os.path.abspath(path)}")

with open(path, 'w') as file:
    json.dump(sofas.tolist(), file, ensure_ascii=False, indent=4)
