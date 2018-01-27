import requests
import re
from bs4 import BeautifulSoup as soup

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

# 1 : <p class="item_supp" content="Voitures" itemprop="category">
# 2 : <p class="item_supp" content="Jeux &amp; Jouets" itemprop="category">
# 3 : <p class="item_supp" content="Equipement bébé" itemprop="category">
# 4 : <p class="item_supp" content="Equipement bébé" itemprop="category">


sentence = r': <p class="item_supp" content="Equipement bébé" itemprop="category">'
targget = re.compile(r'(<p class="item_supp" content=")(\w+ \s? \w+? )(" itemprop="category")')
matches =targget.finditer(sentence)



for match in matches:
    
    categorie =match.group(1)
    print ("categorie = " , categorie )

