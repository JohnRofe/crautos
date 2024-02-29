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

def extract_number(text):
    match = re.search(r'\d+', text)
    return match.group() if match else None

def extract_car_data(car):
    data = {
        'title': car.css_first('td.brandtitle-sm > a').attrs['href'],
        'passengers': extract_number(car.css_first('td.brandtitle-sm > span').text().strip()),
        'price': int(extract_number(car.css_first('span.precio-sm').text().replace(',', ''))),
        'details': [item.strip() for item in car.css_first('div.transtitle').text().replace('|', '').strip().split('\n') if item.strip()]
    }
    data['brand'], data['model'], data['year'] = process_title(data['title'])
    return data

if __name__ == "__main__":

    URL = 'https://crautos.com/autosusados/searchresults.cfm?c=02281'
    scraper = WebScraper(URL)
    html = scraper.get_html()
    cars = get_data_container(html)
    data = [extract_car_data(car) for car in cars]
    with open('cars.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    scraper.close()





