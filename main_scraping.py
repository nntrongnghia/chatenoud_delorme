import FNscraping as scrap
import time
from datetime import datetime as dt

#================ Configurer le programme pricipal
CategoryChoice = ['Consoles &amp; Jeux vidéo' , 'Informatique' , 'Motos' , 'Téléphonie']
RegionChoice = ['Bouches-du-Rhône']
url = "https://www.leboncoin.fr/annonces/offres/provence_alpes_cote_d_azur/"
#==================================================

while 1:
    connexionTest = scrap.connection_check()
    if connexionTest == True :
        li_list = scrap.get_li_list(url)
        for i in li_list:
            IsGood = True    
            Id = scrap.get_id(i)
            try:
                if Id == x :
                    x = scrap.get_id(li_list[0])
                    #POUR TESTER
                    print('Found X')
                    break
            except:
                x = scrap.get_id(li_list[34])
            #=================================================
            #Filtre + Get_Data
            HaveDesc = False
            categorie = scrap.get_cat(i)
            departement = scrap.get_department(i)
            #POUR TESTER, J'AI ENLEVE DES FILTRES
            #if  categorie in CategoryChoice and departement == 'Bouches-du-Rhône':
            if True:
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
                    link = scrap.get_link(i)
                    # il faut rajouter le code postal !!!
                    code_postal = desc_code['code']
                    # rentrer les bonnes annonces dans un tableau ici !!!
                    scrap.save_data(Id, titre, categorie, price, desc, link, departement, ville, code_postal, date)
            #=================================================
            if i == li_list[-1] and scrap.get_id(li_list[-1]) != x:
                x = scrap.get_id(li_list[0])
                # envoyer un message pour dire "on a perdu le x , chef !!"
                scrap.send_log('on a perdu le x , chef !!' + '  ' + str(date) + ' ' + str(dt.today()))
                break
        #POUR TESTER
        print('I have just finished 1 loop!' + ' ' + str(dt.today()))
        
    else:
        scrap.send_log('No connection  ' + str(dt.today()))

    #attendre quelques secondes ..
    time.sleep(5)
    
