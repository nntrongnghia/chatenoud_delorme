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
    targgetville = re.compile(r'<meta content=\"(.+)\" itemprop=\"address\"')
    matches =targgetville.findall(sentence)
    departement = ''
    paca = ['Alpes-Maritimes','Var','Hautes-Alpes','Alpes-de-Haute-Provence','Vaucluse','Bouches-du-Rhône']
    if len(matches) != 0:
        for match in matches:
            if match in paca:
                departement=match
    else:
        departement='No found match'
    return departement

def get_city(li):
    sentence = str(li)
    targgetville = re.compile(r'<meta content=\"(.+)\" itemprop=\"address\"')
    matches =targgetville.findall(sentence)
    ville = ''
    paca = ['Alpes-Maritimes','Var','Hautes-Alpes','Alpes-de-Haute-Provence','Vaucluse','Bouches-du-Rhône']
    if len(matches) != 0:
        for match in matches:
            if match not in paca:
                ville=match
    else:
        ville='No found match'
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
    time.sleep(0.5)
    link = get_link(li)
    link = 'http:'+link   
    result = {'desc':None, 'code':None}
    if connection_check():
        page_annonce = requests.get(link)
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
    else:
        result['desc'] = 'No connection'
        result['code'] = 'No connection'
    return result

def send_log(message):
    with open('log.txt','a') as f:
        f.write('\n' + message)
    return None



def min_not_space(t):
    t = t.replace(" ","").replace("-","").replace("_","")
    return t.lower().replace("è","e").replace("é","e").replace("ê","e")

def filter_iphone(SimpleTilte):
    target = re.compile(r'(iphone)').findall(SimpleTilte)
    if len(target) != 0:
        #print("i phone")
        return True
    else :
        #print("not i phone")
        return False



#================================================================
#Filtres pour telephones !!!!
#-----------------------------

def filter_phone(SimpleTilte):
    SimpleTilte =  min_not_space(SimpleTilte)

    phone= "not defined"

    SimpleTilte = min_not_space(SimpleTilte)

    target = re.compile(r'(galaxys|iphone)([5-9]|x|se)(s|c|edge|\+|plus)?(\+|plus)?')
    
    matches = target.finditer(SimpleTilte)

    for i in matches:

        if len(SimpleTilte) > 1 :

#===============================================================================
#partie I phone 
#===============================================================================
            if i.group(1) == "iphone":
#-------------------------------------------------------------------------------
# I phone X
#-------------------------------------------------------------------------------

                if i.group(2) == "x":
                        #c est un iphone x !!!
                    phone="iphone x"
#-------------------------------------------------------------------------------
# I phone SE
#-------------------------------------------------------------------------------

                if i.group(2) == "se":
                        #c est un iphone se !!!
                    phone="iphone se"

#-------------------------------------------------------------------------------
# I phone 5
#-------------------------------------------------------------------------------

                if i.group(2) == "5":
                    phone="iphone 5"
                    if len(SimpleTilte) > 2  and (i.group(3) != "+"or i.group(3) != "+") :

                        if i.group(3) == "s":
                                #c est un iphone 5s !!
                            phone="iphone 5s"

                        if i.group(3) == "c":
                                #c est un iphone 5c !!
                            phone="iphone 5c"
                            

#-------------------------------------------------------------------------------
# I phone 6
#-------------------------------------------------------------------------------
                if i.group(2) == "6":
                    phone="iphone 6"
                    if len(SimpleTilte) > 2  and ( i.group(3) == "+" or i.group(3) == "plus" or i.group(3) == "s" ):

                                #c est un i phone 6+ !!!
                        phone="iphone 6+"

                        if i.group(3) == "s":
                            if len(SimpleTilte) > 3 and ( i.group(4) == "+" or i.group(4) == "plus"):
                                    #c est un i phone 6s+
                                phone="iphone 6s+"

                            else:
                                #c est un i phone 6s !!!
                                phone="iphone 6s"


                    
#-------------------------------------------------------------------------------
# I phone 7
#-------------------------------------------------------------------------------
                if i.group(2) == "7":
                        if len(SimpleTilte) > 2 and (i.group(3) == "plus" or i.group(3) == "+") :

                            phone="iphone 7+"

                        else:
                            #c est un Galaxy s6 !!!
                            phone="iphone 7"

#-------------------------------------------------------------------------------
# I phone 8
#-------------------------------------------------------------------------------
                if i.group(2) == "8":
                        if len(SimpleTilte) > 2 and (i.group(3) == "plus" or i.group(3) == "+") :

                            phone="iphone 8+"

                        else:
                            #c est un Galaxy s6 !!!
                            phone="iphone 8"

#===============================================================================
#partie Samsung 
#===============================================================================
#  fonction regex = (galaxys)([6-9])(edge|\+|plus)?(\+|plus)?
            if i.group(1) == "galaxys":

                if i.group(2) == "5":
                    phone="not defined"
#-------------------------------------------------------------------------------
# Galaxy S 6 
#-------------------------------------------------------------------------------

                if i.group(2) == "6":
                    if len(SimpleTilte) > 2 and i.group(3) == "edge" :

                        if len(SimpleTilte) > 3 and( i.group(4) == "+" or i.group(4) == "plus"  ) :
                            #c est un Galaxy s6 edge + !!!
                            phone="g S6 Edge +"

                        else :
                            #c est un Galaxy s6 edge !!!
                            phone="g S6 Edge"

                    else:
                        #c est un Galaxy s6 !!!
                        phone="g S6"

#-------------------------------------------------------------------------------
# Galaxy S 7
#-------------------------------------------------------------------------------
                if i.group(2) == "7":
                        if len(SimpleTilte) > 2 and i.group(3) == "edge" :

                            phone="g S7 Edge"

                        else:
                            #c est un Galaxy s6 !!!
                            phone="g S7"

                if i.group(2) == "8":
                        if len(SimpleTilte) > 2 and (i.group(3) == "plus" or i.group(3) == "+" ) :

                            phone="g S8 +"

                        else:
                            #c est un Galaxy s6 !!!
                            phone="g S8"


                if i.group(2) == "9":
                        if len(SimpleTilte) > 2 and (i.group(3) == "plus" or i.group(3) == "+" ) :

                            phone="g S9 +"

                        else:
                            #c est un Galaxy s6 !!!
                            phone="g S9"


    return phone


#================================================================
#Filtres pour consoles !!!!
#-----------------------------

def filter_games(SimpleTilte):
    SimpleTilte =  min_not_space(SimpleTilte)

    game= "not defined"

    SimpleTilte = min_not_space(SimpleTilte)

    target = re.compile(r'(switch|playstation4|ps4|xboxone)((.*)?(jeu))?')
    
    matches = target.finditer(SimpleTilte)

    for i in matches:

        if len(SimpleTilte) > 1 :
            if i.group(1) == "switch":
                
                if len(SimpleTilte) > 3 and  i.group(4) == "jeu":
                    # c est une swich avec jeu!!
                    game = "switch+jeu"
                else:
                    #c est une switch
                    game = "switch"

            if i.group(1) == "xboxone":
                
                if len(SimpleTilte) > 3 and  i.group(4) == "jeu":
                    # c est une xbox1 avec jeu!!
                    game = "xbox1+jeu"
                
                else:
                    #c est une xbox1
                    game = "xbox1"



            if i.group(1) == "ps4" or i.group(1) == "playstation4" :
                
                if len(SimpleTilte) > 3 and  i.group(4) == "jeu":
                    # c est une ps4 avec jeu!!
                    game = "ps4+jeu"
                
                else:
                    #c est une ps4
                    game = "ps4"
    return game





#================================================================
#Filtres pour Scooter !!!!
#-----------------------------

def filter_scoot(SimpleTilte):
    SimpleTilte =  min_not_space(SimpleTilte)

    scoot= "not defined"

    SimpleTilte = min_not_space(SimpleTilte)

    target = re.compile(r'(agility|booster|spirit)')
    
    matches = target.finditer(SimpleTilte)

    for i in matches:

        if len(SimpleTilte) > 1 :
            if i.group(1) == "booster" or i.group(1) == "spirit" :
                # c est un booster
                scoot = "booster"
            if i.group(1) == "agility" :
                #c est un agility
                scoot = "agility"          
    return scoot

def global_filter(i): #i est une annonce dans li_list
    HaveDesc = False
    Id = get_id(i)
    categorie = get_cat(i)
    departement = get_department(i)
    #POUR TESTER, J'AI ENLEVE DES FILTRES
    #if  categorie in CategoryChoice and departement == 'Bouches-du-Rhône':
    if True:
        try:
            price = get_price_li(i)           
        except :
            desc_code = get_desc_code(i)
            desc = desc_code['desc']
            price = get_price_desc(desc)
            HaveDesc = True
        if (price > 49) and (price < 1400) :
            if HaveDesc == False :
                desc_code = get_desc_code(i)
                desc = desc_code['desc']          
            date = get_date(i)
            titre = get_title(i)
            ville = get_city(i)
            link = get_link(i)
            # il faut rajouter le code postal !!!
            code_postal = desc_code['code']
            # rentrer les bonnes annonces dans un tableau ici !!!
            save_data(Id, titre, categorie, price, desc, link, departement, ville, code_postal, date)
    return None

