import json
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader


class Sofa(Item):
    name = Field()
    type = Field()
    imageUrl = Field()
    website = Field()
    price = Field()
    currencyCode = Field()
    ratingValue = Field()
    ratingCount = Field()

class IkeaSofaCrawler(CrawlSpider):
    
    name = 'sofikea'

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'
    }

    download_delay = 1

    allowed_domains = ['ikea.com']

    start_urls = ['https://www.ikea.com/es/es/cat/sofas-fu003/']

    rules = (

        # Paginacion
        Rule(
            LinkExtractor(
                allow=r'/?page='
            ), follow=True, callback='parse_sofas'
        ),

        Rule()
    )


# N sofas

# sofa_soup = BeautifulSoup(page, 'html.parser')

# path = "./test_out.html"
# file = open(path,"w")
# file.write(str(sofa_soup.prettify()))
# file.close()

# n_sofas = sofa_soup.find_all('span', class_='plp-filter-information__total-count')

# print(f"A total of {n_sofas} sofas were found.")
