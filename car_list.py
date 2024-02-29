from selectolax.parser import HTMLParser
from webscraper import WebScraper
import json

class BrandParser:
    def __init__(self, html):
        self.html = html

    def get_brands(self):
        tree = HTMLParser(self.html)
        brand_container = tree.css_first('select[name="brand"]')
        brands = [ brand.text() for brand in brand_container.css('option') ]
        brands.pop(0)  # pop the first element, which is the "All" option
        return brands

if __name__ == "__main__":

    URL = "https://crautos.com/autosusados/"
    scraper = WebScraper(URL)
    html = scraper.get_html('select[name="brand"]')
    parser = BrandParser(html)
    brands = parser.get_brands()
    with open('brands.json', 'w') as f:
        json.dump(brands, f, ensure_ascii=False, indent=4)
    scraper.close()
    





