from bs4 import BeautifulSoup as soup
import requests
import re
import time
import sqlite3 as sql
import pandas as pd



wiki = 'https://fr.wikipedia.org/wiki/Liste_des_communes_des_Bouches-du-Rh%C3%B4ne'

page = requests.get(wiki)
html = soup(page.content,'html.parser')

content = html.find(id='mw-content-text')
content_children = list(content.children)
main = content_children[0]
main_tab =  main.find_all('table')
lst = list(main_tab[1].children)

url = []
url_wiki = 'https://fr.wikipedia.org'

r = re.compile(r'<a href="(.*)" title=')

for i in lst:
    text = str(i)
    url.append(r.findall(text))

url2 = []
for i in url:
    try:
        url2.append(i[0])
    except:
        pass

url2 = url2[1:]
ville_coor = []
labels = ['ville','lat','lon']

for u in url2:
    ville_page = requests.get(url_wiki+u)
    ville_html = soup(ville_page.content,'html.parser')
    ville = ville_html.find(id='firstHeading').text
    lat = float(ville_html.find('a',class_='mw-kartographer-maplink')['data-lat'])
    lon = float(ville_html.find('a',class_='mw-kartographer-maplink')['data-lon'])
    row = [ville,lat,lon]
    ville_coor.append(row)
    print('{}    {}    {}'.format(ville,lat,lon))
    time.sleep(0.5)


#======N'EXECUTE PLUS - Create a database - j'ai deja cree et ajoute des donnes. N'EXECUTE PLUS
df = pd.DataFrame(ville_coor,columns=labels)

conn = sql.connect('lbc.db') #make a connection with database
#c = conn.cursor() # an object to operate with database
df.to_sql('paca_distance', conn, if_exists='replace')
conn.commit() # to save the changes we made
conn.close() # to close the connection, if not, the database is blocked
#=====================