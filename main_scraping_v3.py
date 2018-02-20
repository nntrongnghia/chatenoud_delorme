import FNscraping as scrap
import time
from datetime import datetime as dt
import pandas as pd

# POUR TESTER, J'AI CHANGER LE FILTRE UN PEU

#================ Configurer le programme pricipal
CategoryChoice = ['Consoles &amp; Jeux vidéo' , 'Informatique' , 'Motos' , 'Téléphonie']
RegionChoice = ['Bouches-du-Rhône']
#url1 = "https://www.leboncoin.fr/annonces/offres/provence_alpes_cote_d_azur/?o=1"
url_fond = "https://www.leboncoin.fr/annonces/offres/provence_alpes_cote_d_azur/?o="
#==================================================
#traiter le tableau des coordonnees et des codes postaux
#code_latlon = pd.read_excel('code_latlon.xls')

while 1:
    connexionTest = scrap.connection_check()
    if connexionTest == True :
        foundX2 = False
        npage = 0
        #================ The adventure of X
        #li_list1 = scrap.get_li_list(url1)
        #x1 = scrap.get_id(li_list1[0])
        while foundX2 == False and npage<75: #change la page chaque fois
            npage += 1
            li_listn = scrap.get_li_list(url_fond + str(npage))
            if npage == 1:
                x1 = scrap.get_id(li_listn[0])
            for i in li_listn:
                #IsGood = True    
                Id = scrap.get_id(i)
                try:
                    if Id == x2:
                        x2 = x1
                        print('Found X' + ' ' + str(npage))
                        foundX2 = True
                        break
                except: 
                    x2 = scrap.get_id(li_listn[34])
                #=================================================
                #Filtre + Get_Data
                scrap.global_filter(i)
                #=================================================
            #attendre quelques secondes
            time.sleep(0.5)
        if foundX2 == False:
            x2 = x1
            print('Perdu X2' + ' ' + str(npage) + ' ' + str(dt.today()))
            scrap.send_log('Perdu X2' + ' ' + str(npage) + ' ' + str(dt.today()))    
        print('finished 1 loop!' + ' ' + str(dt.today()))
    else:
        scrap.send_log('No connection  ' + str(dt.today()))
        print('No connection  ' + str(dt.today()))

    #attendre quelques secondes ..
    time.sleep(10)

