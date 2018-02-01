import requests
import re
from bs4 import BeautifulSoup as soup
from datetime import datetime
from math import sqrt
from math import asin
from math import sin
from math import cos

def get_distance_from_marseille(lon,lat):
    # les coordonés GPS de chatenoud sonts :
    # lattitude : 43.3353913
    # longitude  : 5.408912999999984
    #   x = longitude
    #   y = lattitude
    # il faut mettre la longitude en premier (axe des x)
    #coordonees de chatenoud
    latc = 43.3353913
    longc = 5.408912999999984
    #convertion des degrés en radians
    rlon = 0.017453293 * lon
    rlat = 0.017453293 * lat
    rlonc = 0.017453293 * longc 
    rlatc = 0.017453293 * latc
    #Calcule de la distance en Km
    latSin = sin((rlat - rlatc)/2)
    lonSin = sin((rlon - rlonc)/2)
    #formule de Haversine:
    dist = 2 * asin(sqrt((latSin*latSin) + cos(rlat) * cos(rlatc) * (lonSin * lonSin)))
    # pour la distance en Km il faut multiplier la valeure trouvée par le rayon de la terre
    distkm = dist * 6378.137 
    #pour Chatenoud - Hô Chi Minh-Ville (10 072 km) = 10 083.5 
    #taux d'erreurs : 11 km ( 0.112 % )
    return distkm


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

def get_price_li(li):
    item_price = li.a.find(class_='item_price').text.split()
    item_price = item_price[:3]
    #tirer le prix dans le list ci-dessus et transformer sous type float
    price_str = [s for s in item_price if s.isdigit()]
    price = ''
    for s in price_str:
        price += s
    price = int(price)
    return price
    

def get_price_desc(content):
    r = re.compile(r'(\d*\s*\d+)\s*(euros\b|E\b|e\b|euro\b|Euro\b|Euros\b|\u20AC\s*)')
    found = r.findall(content)
    if len(found) != 1:
        price = 0
    else:
        found_price = ''
        for i in found[0][0].split():
            found_price += i
        price = int(found_price)
    return price



def get_date(li):
    date_html = li.a.find_all(class_='item_supp')[-1]
    d = date_html['content']
    h = date_html.text.split()[-1]
    dt = datetime.strptime(d + ' ' + h,'%Y-%m-%d %H:%M')
    return dt

def get_cat(li):
    target_categorie = re.compile(r'(<p class="item_supp" content=")(.+?)(" itemprop="category">)')
    sentence = str(li)
    matches =target_categorie.finditer(sentence)
    #ici on extrait la catégorie qui sera implémenté dans la variable "categorie"
    for match in matches:
        categorie =match.group(2)
    return categorie

#obtenir la description
def get_desc(li):
    try:
        link = get_link(li)
        link = 'http:'+link   
        page_annonce = requests.get(link)
        page_soup = soup(page_annonce.content,'html.parser')
        desc_html = page_soup.find_all(class_='line properties_description')[0]
        desc_split = desc_html.text.split()
        desc = ''
        for s in desc_split:
            desc = desc + ' ' + s
        return desc
    except:
        return 'Nouvelle type de page sur leboncoin'

def get_title(li):
    return li.a['title']

def get_id(li):
    return li.find(class_='saveAd')['data-savead-id']

def get_department(li):
    sentence = str(li)
    targgetville = re.compile(r'<meta content="(.+)" itemprop="address"')
    matches =targgetville.findall(sentence)
    paca = ['Alpes-Maritimes','Var','Hautes-Alpes','Alpes-de-Haute-Provence','Vaucluse','Bouches-du-Rhône']
    for match in matches:
        if match in paca:
            departement=match  
    return departement

def get_city(li):
    sentence = str(li)
    targgetville = re.compile(r'<meta content="(.+)" itemprop="address"')
    matches =targgetville.findall(sentence)
    paca = ['Alpes-Maritimes','Var','Hautes-Alpes','Alpes-de-Haute-Provence','Vaucluse','Bouches-du-Rhône']
    for match in matches:
        if match not in paca:
            ville=match  
    return ville
