import requests
from bs4 import BeautifulSoup
from selenium import webdriver

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.starbucksVillage2


# headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
# data = requests.get('https://www.starbucks.co.kr/menu/drink_list.do',headers=headers)

dr = webdriver.Chrome('./chromedriver.exe')
dr.get("https://www.starbucks.co.kr/menu/drink_list.do")

html_source = dr.page_source

soup = BeautifulSoup(html_source, 'html.parser')


#coldbrew
#lists = soup.select_one('#container > div.content > div.product_result_wrap.product_result_wrap01 > div > dl > dd:nth-child(2) > div.product_list > dl > dd:nth-child(2) > ul')

coldbrews = soup.select_one('.product_cold_brew')
for li in coldbrews:
    coffee = li.select_one('dl')
    if coffee is not None:
        image = li.select_one('a > img')['src']
        coffeeName = li.select_one('dd')
        category = '콜드 브루'

        doc = {
            'image': image,
            'coffeeName': coffeeName.text,
            'category': category
        }
        db.coffees.insert_one(doc)


broods = soup.select_one('.product_brood')
for li in broods:
    coffee = li.select_one('dl')
    if coffee is not None:
        image = li.select_one('a > img')['src']
        coffeeName = li.select_one('dd')
        category = '브루드'

        doc = {
            'image': image,
            'coffeeName': coffeeName.text,
            'category': category
        }
        db.coffees.insert_one(doc)


expressos = soup.select_one('.product_espresso')
for li in expressos:
    coffee = li.select_one('dl')
    if coffee is not None:
        image = li.select_one('a > img')['src']
        coffeeName = li.select_one('dd')
        category = '에스프레소'

        doc = {
            'image': image,
            'coffeeName': coffeeName.text,
            'category': category
        }
        db.coffees.insert_one(doc)


frappuccinos = soup.select_one('.product_frappuccino')
for li in frappuccinos:
    coffee = li.select_one('dl')
    if coffee is not None:
        image = li.select_one('a > img')['src']
        coffeeName = li.select_one('dd')
        category = '프라푸치노'

        doc = {
            'image': image,
            'coffeeName': coffeeName.text,
            'category': category
        }
        db.coffees.insert_one(doc)


blendeds = soup.select_one('.product_blended')
for li in blendeds:
    coffee = li.select_one('dl')
    if coffee is not None:
        image = li.select_one('a > img')['src']
        coffeeName = li.select_one('dd')
        category = '블랜디드'

        doc = {
            'image': image,
            'coffeeName': coffeeName.text,
            'category': category
        }
        db.coffees.insert_one(doc)


fizzos = soup.select_one('.product_fizzo')
for li in fizzos:
    coffee = li.select_one('dl')
    if coffee is not None:
        image = li.select_one('a > img')['src']
        coffeeName = li.select_one('dd')
        category = '피치오'

        doc = {
            'image': image,
            'coffeeName': coffeeName.text,
            'category': category
        }
        db.coffees.insert_one(doc)


teas = soup.select_one('.product_tea')
for li in teas:
    coffee = li.select_one('dl')
    if coffee is not None:
        image = li.select_one('a > img')['src']
        coffeeName = li.select_one('dd')
        category = '티'

        doc = {
            'image': image,
            'coffeeName': coffeeName.text,
            'category': category
        }
        db.coffees.insert_one(doc)


etcs = soup.select_one('.product_etc')
for li in etcs:
    coffee = li.select_one('dl')
    if coffee is not None:
        image = li.select_one('a > img')['src']
        coffeeName = li.select_one('dd')
        category = '기타'

        doc = {
            'image': image,
            'coffeeName': coffeeName.text,
            'category': category
        }
        db.coffees.insert_one(doc)


juices = soup.select_one('.product_juice')
for li in juices:
    coffee = li.select_one('dl')
    if coffee is not None:
        image = li.select_one('a > img')['src']
        coffeeName = li.select_one('dd')
        category = '주스(병음료)'

        doc = {
            'image': image,
            'coffeeName': coffeeName.text,
            'category': category
        }
        db.coffees.insert_one(doc)

