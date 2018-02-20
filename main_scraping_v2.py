import FNscraping as scrap
import time
from datetime import datetime as dt
import pandas as pd

# POUR TESTER, J'AI CHANGER LE FILTRE UN PEU

#================ Configurer le programme pricipal
CategoryChoice = ['Consoles &amp; Jeux vidéo' , 'Informatique' , 'Motos' , 'Téléphonie']
RegionChoice = ['Bouches-du-Rhône']
url1 = "https://www.leboncoin.fr/annonces/offres/provence_alpes_cote_d_azur/"
url2 = "https://www.leboncoin.fr/annonces/offres/provence_alpes_cote_d_azur/?o=2"
#==================================================
#traiter le tableau des coordonnees et des codes postaux
code_latlon = pd.read_excel('code_latlon.xls')

while 1:
    connexionTest = scrap.connection_check()
    if connexionTest == True :
        li_list = scrap.get_li_list(url1)
        x1 = scrap.get_id(li_list[0])
        #================ The adventure of X
        for i in li_list:
            #IsGood = True    
            Id = scrap.get_id(i)
            try:
                if Id == x2:
                    x2 = x1
                    print('Found X')
                    break
            except:
                x2 = scrap.get_id(li_list[34])
            #=================================================
            #Filtre + Get_Data
            scrap.global_filter(i)
            #=================================================
            if i == li_list[-1] and Id != x2:
                li_list_2 = scrap.get_li_list(url2)
                for y in li_list_2:
                    #IsGood = True
                    Id = scrap.get_id(y)
                    if Id == x2:
                        x2 = x1
                        print('Found X')
                        break
                    #===================
                    scrap.global_filter(y)
                    #=======================
                    if y == li_list_2[-1] and Id != x2:
                        x2 = x1
                        scrap.send_log('on a perdu le x , chef !!' + ' ' + str(dt.today()))
                        print('perdu X2')
                        break
        #POUR TESTER
        print('finished 1 loop!' + ' ' + str(dt.today()))
    else:
        scrap.send_log('No connection  ' + str(dt.today()))
        print('No connection  ' + str(dt.today()))

    #attendre quelques secondes ..
    time.sleep(8)

