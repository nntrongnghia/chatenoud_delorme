import requests
import re
from bs4 import BeautifulSoup as soup
from datetime import datetime #bibliotheque pour traiter la date
import FNscraping as scrap

# just listing the operations - need to develop more fuctions to minimize the program
cat = []

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

CategoryChoice = ['Consoles &amp; Jeux vidéo' , 'Informatique' , 'Motos' , 'Téléphonie']


#=================================================================
#===================    Partie de Hako ci-dessous      ======================
#=================================================================

#sous catégories :
Iphone :'iphone','Iphone','i phone','I phone','iPhone','IPhone','i Phone','I Phone','IPHONE','I PHONE'
#------------------------------------------------------------
#PREMIER FILTRE !! (on apellera global_filter)
#Cette fonction filtre la liste li_list par un prix < a 50 et une 
# categorie comprise dans la variable : CategoryChoice .
sentence = str(li_list[0])

for i in li_list:
    IsGood = True
    IsPriceGood = True
    IsCatGood = True
    price = scrap.get_price(i)
    if (price < 49) or (price > 1400) :
        IsPriceGood = False
    categorie = scrap.get_cat(i)
    if categorie not in CategoryChoice: 
        IsCatGood = False
    if (IsPriceGood == False) or (IsCatGood == False) :
        IsGood = False
    print(IsGood)

# il faudrait essayer de supprimer au max de variables inutiles ...


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


sentence = str(li_list[4])

targgetville = re.compile(r'<meta content="(.+)" itemprop="address"')
matches =targgetville.findall(sentence)
paca = ['Alpes-Maritimes','Var','Hautes-Alpes','Alpes-de-Haute-Provence','Vaucluse','Bouches-du-Rhône']
for match in matches:
    if match in  paca:
        departement=match  
    else:
        ville = match 


#-----------------------------------------------------
#   FONCTION TROUVER TITRE


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
    # le prix passe d'une chaine de caractere a une valeur numérique(moin lourde)
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


#-----------------------------------------------------------------
#-----------------------------------------------------------------
#-----------------------------------------------------------------
#-----------------------------------------------------------------


#Fonction Principale :

CategoryChoice = ['Consoles &amp; Jeux vidéo' , 'Informatique' , 'Motos' , 'Téléphonie']

connexionTest = scrap.connection_check()
if connexionTest == True :

    for i in li_list:
        IsGood = True    
        Id = scrap.get_id(i)
        try:
            if Id == x :
                x = scrap.get_id(li_list[0])
                break
        except:
            x = scrap.get_id(li_list[34])
        #=================================================
        #Filtre + Get_Data
        HaveDesc = False
        categorie = scrap.get_cat(i)
        departement = scrap.get_department(i)
        if  categorie in CategoryChoice and departement == 'Bouches-du-Rhône':
            try:

                price = scrap.get_price_li(i)           

            except :
                desc_code = scrap.get_desc_code(i)
                desc = desc_code['desc']
                price = scrap.get_price_desc(desc)
                HaveDesc = True

            if (price > 49) and (price < 1400) :
                if HaveDesc == False :
                    desc_code = scrap.get_desc_code(i)
                    desc = desc_code['desc']
                
                date = scrap.get_date(i)
                titre = scrap.get_title(i)
                ville = scrap.get_city(i)
                # il faut rajouter le code postal !!!
                code_postal = desc_code['code']
                # rentrer les bonnes annonces dans un tableau ici !!!
        #=================================================
        if i == li_list[-1] and scrap.get_id(li_list[-1]) != x:

            x = scrap.get_id(li_list[0])
            # envoyer un message pour dire "on a perdu le x , chef !!"
            break


scrap.get_li_list("https://www.leboncoin.fr/annonces/offres/provence_alpes_cote_d_azur/?o=2")

#attendre quelques secondes ....











TEEEEEEEESTE !!!!!!!

#-----------------------------------------------------------------
#-----------------------------------------------------------------
#-----------------------------------------------------------------
#-----------------------------------------------------------------


#Fonction Principale :

CategoryChoice = ['Consoles &amp; Jeux vidéo' , 'Informatique' , 'Motos' , 'Téléphonie']

connexionTest = scrap.connection_check()
if connexionTest == True :

    for i in li_list:
        IsGood = True    
        Id = scrap.get_id(i)
        if i == 0 :
            x1 = Id
        try:
            if Id == x2 :
                x2=x1
                break
        except:
            x2 = scrap.get_id(li_list[34])
        #=================================================
        #Filtre + Get_Data
        #=================================================
        if i == li_list[-1] and scrap.get_id(li_list[-1]) != x2 :
            li_list_two = scrap.get_li_list("https://www.leboncoin.fr/annonces/offres/provence_alpes_cote_d_azur/?o=2")
            for y in li_list_two:
                IsGood = True    
                Id = scrap.get_id(y)
                
                if Id == x2 :
                    x2=x1

                #=================================================
                #Filtre + Get_Data
                #aviable to get datta 
                #=================================================
                if y == li_list_two[-1] and scrap.get_id(li_list_two[-1]) != x2 :
                    x2 = x1
                    # envoyer un message pour dire "on a perdu le x , chef !!"
                    break



#attendre quelques secondes ....

