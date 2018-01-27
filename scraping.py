import requests
import re
from bs4 import BeautifulSoup as soup
from datetime import datetime #bibliotheque pour traiter la date

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
#==================================================================

# on va chercher dans le string li_list[X] précisément l'emplacement du nom de la catégorie
targgetcategorie = re.compile(r'(<p class="item_supp" content=")(.+?)(" itemprop="category">)')

matches =targgetcategorie.finditer(sentence)


#ici on extrait la catégorie qui sera implémenté dans la variable "categorie"
for match in matches:
    categorie =match.group(2)




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
sample = li_list[0]
#tirer le lien, prix et id et creer la date 
#inutile sample.a = list(sample.children)[1] #get the a tag - child
#TIRER LE LIEN
#inutile lien = sample.a['href']
lien = sample.a['href']

#TIRER LE PRIX

#chain de caractere dans le tag 'item_price'
#c'est un list y compris le prix (sous type char) et le symbol euro
item_price = sample.a.find(class_='item_price').text.split() 
#tirer le prix dans le list ci-dessus et transformer sous type float
price = [float(s) for s in item_price if s.isdigit()][0]

#TRAITER LA DATE

#Car le html pour la date c'est le dernier tag avec class='item_supp'
date_html = sample.a.find_all(class_='item_supp')[-1]
#tirer la date et heure sous type char
d = date_html['content']
h = date_html.text.split()[-1]
#creer l'objet datetime.datetime
dt = datetime.strptime(d + ' ' + h,'%Y-%m-%d %H:%M')
#on va utiliser l'objet datetime.datetime
#car c'est facile a traiter et trier
#FIN SAMPLE CODE =================
