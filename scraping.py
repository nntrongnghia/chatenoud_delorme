import requests
import re
from bs4 import BeautifulSoup as soup
from datetime import datetime #bibliotheque pour traiter la date
import FNscraping as scrap

# just listing the operations - need to develop more fuctions to minimize the program

url = "https://www.leboncoin.fr/annonces/offres/provence_alpes_cote_d_azur/"
page = requests.get(url)
page_soup = soup(page.content, 'html.parser')

#get the html of the section class="tabsContent block-white dontSwitch"
section_tabs_content = page_soup.find_all(class_="tabsContent block-white dontSwitch")#LIST type
section_html = section_tabs_content[0]

#section ul
sect_ul = list(section_html.children)[1]

#section ul [li*35]
li_list = sect_ul.find_all('li')



#=================================================================
#===================    Partie de Hako ci-dessous      ======================
#=================================================================

#-----------------------------------------------------
#   FONCTION TROUVER CAEGORIE

sentence = str(li_list[0])
# on va chercher dans le string li_list[X] précisément l'emplacement du nom de la catégorie
targgetcategorie = re.compile(r'(<p class="item_supp" content=")(.+?)(" itemprop="category">)')
matches =targgetcategorie.finditer(sentence)
#ici on extrait la catégorie qui sera implémenté dans la variable "categorie"
for match in matches:
    categorie =match.group(2)
    #imprimer la categorie (optionel !!!)
    print(categorie)


#-----------------------------------------------------
#   FONCTION TROUVER TITRE


sentence = str(li_list[0])
# on va chercher dans le string li_list[X] précisément l'emplacement du titre de l'annonce
targgettitle = re.compile(r'(<span class="lazyload" data-imgalt=")(.+?)(" data-imgsrc=)')
matches =targgettitle.finditer(sentence)
#ici on extrait le titre qui sera implémenté dans la variable "titre"
for match in matches:
    titre =match.group(2)
    #imprimer le titre (optionel !!!)
    print(titre)
    
#-----------------------------------------------------
#   FONCTION TROUVER LIEU (VILLE ET DEPARTEMENT)



sentence = str(li_list[0])
# on va chercher dans le string li_list[X] précisément les coordonéés géographiques de l'annonceur

targgetville = re.compile(r'(<meta content=")(.+)(" itemprop="address")')
matches =targgetville.finditer(sentence)
#ici on extrait le lieux (ville et departement dans le groupe 2(au millieu))
for match in matches:
    #si le lieu a le nom d'un des departements de la region paca , c est un département 
    lieu =match.group(2)
    if lieu == 'Alpes-Maritimes':
        #on l'implémentera donc dans la variable "departement"
        departement = lieu
    # sinon , c est le nom d'une ville !!!    
    else:
        #on l'implémentera alors dans la variable "ville"
        ville = lieu  
    #imprimer la ville (sous la variable ville) et le departement (dans departement) (optionel !!!)  
    print("ville = ", ville)
    print("departement = ", departement)

    


#===================================================================
#==================     Partie de Tony ci-dessous     ========================
#===================================================================

#une foncion qui prend le lien d'une page des annonces leboncoin et 
#renvoie un tableaux (LIST type) de 'li' html
def get_li(url):
    page = requests.get(url)
    page_soup = soup(page.content,'html.parser')
    section_tabs_content = page_soup.find_all(class_="tabsContent block-white dontSwitch")
    section_html = section_tabs_content[0]
    sect_ul = list(section_html.children)[1]
    li_list = sect_ul.find_all('li')
    return li_list

#SAMPLE CODE==========
li = li_list[0]
#tirer le lien, prix et id et creer la date 
#inutile li.a = list(li.children)[1] #get the a tag - child
#TIRER LE LIEN
#inutile lien = li.a['href']
lien = li.a['href']

#TIRER LE PRIX

#chain de caractere dans le tag 'item_price'
#c'est un list y compris le prix (sous type char) et le symbol euro
try:
    item_price = li.a.find(class_='item_price').text.split()
    item_price = item_price[:3]
    #tirer le prix dans le list ci-dessus et transformer sous type float
    price_str = [s for s in item_price if s.isdigit()]
    price = ''
    for s in price_str:
        price += s
    price = int(price)
except:
    #OBTENIR LA DESCRIPTION
    link = scrap.get_link(li)
    link = 'http:'+link   
    page_annonce = requests.get(link)
    page_soup = soup(page_annonce.content,'html.parser')
    desc_html = page_soup.find_all(class_='line properties_description')[0]
    desc_split = desc_html.text.split()
    desc = ''
    for s in desc_split:
        desc = desc + ' ' + s
    #FIN DESCRIPTION
    #OBTERNIR LE PRIX DANS LA DESCRIPTION
    r = re.compile(r'(\d+)\s*(euros\b|E\b|e\b|euro\b|Euro\b|Euros\b|\u20AC\s*)')
    found = r.findall(content)
    if len(found) != 1:
        price = 0
    else:
        price = int(found[0][0])

#TRAITER LA DATE

#Car le html pour la date c'est le dernier tag avec class='item_supp'
date_html = li.a.find_all(class_='item_supp')[-1]
#tirer la date et heure sous type char
d = date_html['content']
h = date_html.text.split()[-1]
#creer l'objet datetime.datetime
dt = datetime.strptime(d + ' ' + h,'%Y-%m-%d %H:%M')
#on va utiliser l'objet datetime.datetime
#car c'est facile a traiter et trier
#FIN SAMPLE CODE =================

#trouver ID de l'annonce
iden = li.find(class_='saveAd')['data-savead-id']
