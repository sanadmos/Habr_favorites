# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 17:28:06 2021

@author: admOS
"""

import requests
from lxml import html
import openpyxl

pages = []
url = "https://habr.com/ru/users/admos/favorites"
page = requests.get(url).content.decode("utf-8")
pages.append(page)
tree = html.fromstring(page)
pgs = len(tree.xpath('//li[@class="toggle-menu__item toggle-menu__item_pagination"]'))
# pgs = 1
for num in range(2, pgs+1):
    url = f"https://habr.com/ru/users/admos/favorites/page{num}"
    page = requests.get(url).content.decode("utf-8")
    pages.append(page)

xl = openpyxl.Workbook()
ws = xl.active
ws.title = "habr.com"
row = 0
for page in pages:
    tree = html.fromstring(page)
    articles = tree.xpath('//article[@class="post post_preview"]')
    for article in articles:
        row +=1
        try:
            date = article.xpath('.//span[@class="post__time"]')[0].text # время публикации поста
            title = article.xpath('.//h2')[0][0].text # название поста
            link = article.xpath('.//a/@href')[1] # ссылка на пост
            ws.cell(row=row, column=1).style = "Hyperlink"
            ws.cell(row=row, column=1).value = title
            ws.cell(row=row, column=1).hyperlink = link
            ws.cell(row=row, column=2, value=date)
        except IndexError:
            continue
ws.column_dimensions["A"].width = 130
ws.column_dimensions["B"].width = 30
xl.save("habr.com.xlsx")
xl.close()
