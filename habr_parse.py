# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 17:28:06 2021

@author: admOS
"""

import requests
from lxml import html

pages = []
url = "https://habr.com/ru/users/admos/favorites"
page = requests.get(url).content.decode("utf-8")
pages.append(page)
tree = html.fromstring(page)
pgs = len(tree.xpath('//li[@class="toggle-menu__item toggle-menu__item_pagination"]'))
pgs = 1
for num in range(2, pgs+1):
    url = f"https://habr.com/ru/users/admos/favorites/page{num}"
    page = requests.get(url).content.decode("utf-8")
    pages.append(page)
    
for page in pages:
    tree = html.fromstring(page)
    articles = tree.xpath('//article[@class="post post_preview"]')
    for article in articles:
        try:
            print(article.xpath('.//h2')[0][0].text)
            
            print(article.xpath('.//span[@class="post__time"]')[0].text)
        except IndexError:
            continue
