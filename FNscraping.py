import requests
import re
from bs4 import BeautifulSoup as soup
from datetime import datetime

def get_li_list(url):
    page = requests.get(url)
    page_soup = soup(page.content,'html.parser')
    section_tabs_content = page_soup.find_all(class_="tabsContent block-white dontSwitch")
    section_html = section_tabs_content[0]
    sect_ul = list(section_html.children)[1]
    li_list = sect_ul.find_all('li')
    return li_list

#des fonctions pour obtenir des informations ci-dessous prennent le 'li' tag comme entree

def get_link(li):
    link = li.a['href']
    return link

def get_price(li):
    item_price = li.a.find(class_='item_price').text.split() 
    price = [float(s) for s in item_price if s.isdigit()][0]
    return price

def get_date(li):
    date_html = li.a.find_all(class_='item_supp')[-1]
    d = date_html['content']
    h = date_html.text.split()[-1]
    dt = datetime.strptime(d + ' ' + h,'%Y-%m-%d %H:%M')
    return dt