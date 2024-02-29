from selectolax.parser import HTMLParser
from webscraper import WebScraper
import re
import json

def get_data_container(html):
    tree = HTMLParser(html)
    cars = tree.css('form div.d-md-none')
    return cars

def process_title(title):
    _, rest = title.split('&', 1)
    brand, model, year = rest.split('.')
    return brand, model, year

def extract_car_data(car):
    title = car.css_first('td.brandtitle-sm > a').attrs['href']
    brand, model, year = process_title(title)

    passengers_text = car.css_first('td.brandtitle-sm > span').text().strip()
    passengers_match = re.search(r'\d+', passengers_text)
    passengers = passengers_match.group() if passengers_match else None

    price_text = car.css_first('span.precio-sm').text().strip()
    price_match = re.search(r'\d+', price_text.replace(',', ''))
    price = int(price_match.group()) if price_match else None

    details = car.css_first('div.transtitle').text().replace('|', '').strip()
    details_list = [item.strip() for item in details.split('\n') if item.strip()]
    return {'brand': brand, 'model': model, 'year': year, 'passangers': passengers, 'price': price, 'details': details_list}

if __name__ == "__main__":

    URL = 'https://crautos.com/autosusados/searchresults.cfm?c=02281'
    scraper = WebScraper(URL)
    html = scraper.get_html()
    cars = get_data_container(html)
    data = [extract_car_data(car) for car in cars]
    scraper.close()
    with open('cars.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)




