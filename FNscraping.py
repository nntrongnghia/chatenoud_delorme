import requests
import re
from bs4 import BeautifulSoup as soup
from datetime import datetime

def get_li(url):
    page = requests.get(url)
    page_soup = soup(page.content,'html.parser')
    section_tabs_content = page_soup.find_all(class_="tabsContent block-white dontSwitch")
    section_html = section_tabs_content[0]
    sect_ul = list(section_html.children)[1]
    li_list = sect_ul.find_all('li')
    return li_list

#des fonctions pour obtenir des informations ci-dessous prennent le 'li' tag comme entree