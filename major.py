import csv
from bs4 import BeautifulSoup
from selenium import webdriver

def get_url(search_term):
    """ generate a url """
    template = "https://www.amazon.com/s?k={}&ref=nb_sb_noss_2"
    search_term=search_term.replace(' ',' +')
    url=template.format(search_term)
    url+='&page{}'
    return url

def extract_record(item):
    """extract and return data"""
    #description tag and url
    atag = item.h2.a
    description = atag.text.strip()
    url = "https://www.amazon.com"+atag.get('href')
    #price
    try:
        price_parent = item.find('span', 'a-price')
        price = price_parent.find('span', 'a-offscreen').text
    except AttributeError:
        return
    #rating
    try:
        rating = item.i.text
        review_count = item.find('span', {'class', 'a-size-base', 'dir', 'auto'})
    except AttributeError:
        rating = ' '
        review_count = ' '

    result = (description,price,rating,review_count,url)
    return result

def main(search_term):
    """main function"""
    driver = webdriver.Chrome()
    records = []
    url=get_url(search_term)
    for page in range(1,21):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source,'html.parser')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})
    for item in results:
        record=extract_record(item)
        if record:
            records.append(record)

    driver.close()
    with open('results.csv', 'w',newlines='',encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow('Description', 'Price','Rating','ReviewCount','url')
        writer.writerow(records)