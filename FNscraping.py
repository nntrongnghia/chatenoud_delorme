import requests
import re
from bs4 import BeautifulSoup as soup
from datetime import datetime
from math import sqrt
from math import asin
from math import sin
from math import cos
import sqlite3 as sql
import time
from datetime import datetime as dt

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

def find_latlon(df,code): #pas bon. ex:13106 13107 13105 13104
    coor = {}
    diff =  df['Code Postal'].apply(lambda x: abs(code-x))
    i = diff[diff == diff.min()].index.tolist()[0]
    coor['lat'] = df.loc[i]['Latitude']
    coor['lon'] = df.loc[i]['Longitude']
    return coor

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
    try:
        date_html = li.a.find_all(class_='item_supp')[-1]
        d = date_html['content']
        h = date_html.text.split()[-1]
        dt = datetime.strptime(d + ' ' + h,'%Y-%m-%d %H:%M')
    except:
        date_html = li.a.find_all('p',class_='item_supp')[-1]
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


#return TRUE if there is a connection
def connection_check():
    try:
        requests.get('https://www.google.fr')
        return True
    except:
        return False

#stocker des donnees dans un tableau dans le database lbc.db
def save_data(Id=None,title=None,cat=None,price=None,desc=None,link=None,department=None,city=None,code=None,date=None):
    conn = sql.connect('lbc.db')
    c = conn.cursor()
    values = (Id,title,cat,price,desc,link,department,city,code,date)
    c.execute("INSERT INTO annonce VALUES (?,?,?,?,?,?,?,?,?,?)", values)
    conn.commit() 
    conn.close()
    return None

#obtenir la description et le code postal
#renvoyer une dictionaire de 2 mots cles: 'desc' et 'code'
def get_desc_code(li):
    link = get_link(li)
    link = 'http:'+link   
    time.sleep(1)
    page_annonce = requests.get(link)
    result = {'desc':None, 'code':None}
    if page_annonce.status_code == requests.codes.ok:
        page_soup = soup(page_annonce.content,'html.parser')
        try: 
            desc_html = page_soup.find_all(class_='line properties_description')[0]
            desc_split = desc_html.text.split()
            desc = ''
            for s in desc_split:
                desc = desc + ' ' + s
            #obtenir code postal   
            code = page_soup.find_all(class_='line line_city')[0].find_all(class_='value')[0].text.split()[-1]
            #return desc

        except:
            page_html = str(page_soup)
            r = re.compile(r'<div data-qa-id=\"adview_description_container\" data-reactid=\"\d+\"><div data-reactid=\"\d+\"><span data-reactid=\"\d+\">(.*)</span></div><div class=\"_3ey2y\"')
            if len(r.findall(page_html)) == 0:
                desc = 'Not found'
                print(desc)
            else:
                desc = r.findall(page_html)[0]

            r1 = re.compile(r'(<br/>)')
            desc = r1.sub(r' ',desc)

            if len(page_soup.find_all(class_='_1aCZv')) != 0:
                code_text = page_soup.find_all(class_='_1aCZv')[0].text
                r2 = re.compile(r'\D(\d{5})\D')
                if len(r2.findall(code_text)) == 0:
                    code = 'Not found' 
                    print(code)
                else:
                    code = r2.findall(code_text)[0]
            else:
                code = 'Not found the html class'
                print(code)
    else:
        send_log('Failed to get html' + ' ' + str(dt.today()))
        print('Failed to get html')
        desc = 'Failed to get html'
        code = 'Failed to get html'

    result['desc'] = desc
    result['code'] = code
    return result

def send_log(message):
    with open('log.txt','a') as f:
        f.write('\n' + message)
    return None



def min_not_space(t):
    return t.lower().replace(" ","")



#================================================================
#Filtres pour telephones !!!!
#-----------------------------

def filter_iphone(SimpleTilte):
    
    target = re.compile(r'(iphone)').findall(SimpleTilte)
    
    if len(target) != 0:
        
        target = re.compile(r'(iphone5)').findall(SimpleTilte)

        if len(target) != 0:
            target = re.compile(r'(iphone5c)').findall(SimpleTilte)
            if len(target) != 0:
                phone="Ip5c"
            target = re.compile(r'(iphone5s)').findall(SimpleTilte)
            if len(target) != 0:
                phone="Ip5s"
            else:
                phone="Ip5"
        target = re.compile(r'(iphone6)').findall(SimpleTilte)
        if len(target) != 0:
            target = re.compile(r'(iphone6s)').findall(SimpleTilte)
            if len(target) != 0:
                target = re.compile(r'(iphone6s(\+|plus))').findall(SimpleTilte)
                if len(target) != 0:
                    phone = "Ip6s+"
                else:
                    phone = "Ip6s"   
            target = re.compile(r'(iphone6(\+|plus))').findall(SimpleTilte)
            if len(target) != 0:
                phone="Ip6+"
            else:
                phone="Ip6"
        target = re.compile(r'(iphone7)').findall(SimpleTilte)
        if len(target) != 0:
            target = re.compile(r'(iphone7(\+|plus))').findall(SimpleTilte)
            if len(target) != 0:
                phone="Ip7+"
            else:
                phone="Ip7"
        target = re.compile(r'(iphone8)').findall(SimpleTilte)
        if len(target) != 0:
            target = re.compile(r'(iphone8(\+|plus))').findall(SimpleTilte)
            if len(target) != 0:
                phone="Ip8+"
            else:
                phone="Ip8"
        target = re.compile(r'(iphonex)').findall(SimpleTilte)
        if len(target) != 0:
            phone="Ipx"
        target = re.compile(r'(iphonese)').findall(SimpleTilte)
        if len(target) != 0:
            phone="Ipse"
    else :
        phone="not defined"   
    return phone


