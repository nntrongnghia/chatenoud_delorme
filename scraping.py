import requests
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
