import re


def min_not_space(t):
    t = t.replace(" ","").replace("-","").replace("_","")
    t = t.replace("â","a").replace("á","a").replace("à","a")
    return t.lower().replace("è","e").replace("é","e").replace("ê","e")

def filter_iphone(SimpleTilte):
    target = re.compile(r'(iphone)').findall(SimpleTilte)
    if len(target) != 0:
        #print("i phone")
        return True
    else :
        #print("not i phone")
        return False


def hs_finder(SimpleTilte,Description):

    SimpleTilte =  min_not_space(SimpleTilte)
    SimpleDesc = min_not_space(Description)
    out=False 

    target = re.compile(r'(hs|horsservic|pourpiece|areparer|pourreparateur|casse|allumeplus|demareplus)')
    
    matches1 = target.finditer(SimpleTilte)
    matches2 = target.finditer(SimpleDesc)

    for i in matches1:

        if len(SimpleTilte) != 0 :
            out =True
        else:
            out =False

    if out == False:
        for i in matches2:

            if len(SimpleDesc) != 0 :
                out =True
            else:
                out =False



    return out


#================================================================
#Filtres pour telephones !!!!
#-----------------------------

def filter_phone(SimpleTilte,Desc):
    SimpleTilte =  min_not_space(SimpleTilte)
    Desc =  min_not_space(Desc)
    out = hs_finder(SimpleTilte,Desc)
    if out == True :
        phone = "broken"
        return phone

    phone= "not defined"

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
                            phone="gS6Edge+"

                        else :
                            #c est un Galaxy s6 edge !!!
                            phone="gS6Edge"

                    else:
                        #c est un Galaxy s6 !!!
                        phone="gS6"

#-------------------------------------------------------------------------------
# Galaxy S 7
#-------------------------------------------------------------------------------
                if i.group(2) == "7":
                        if len(SimpleTilte) > 2 and i.group(3) == "edge" :

                            phone="gS7Edge"

                        else:
                            #c est un Galaxy s6 !!!
                            phone="gS7"

                if i.group(2) == "8":
                        if len(SimpleTilte) > 2 and (i.group(3) == "plus" or i.group(3) == "+" ) :

                            phone="gS8+"

                        else:
                            #c est un Galaxy s6 !!!
                            phone="gS8"


                if i.group(2) == "9":
                        if len(SimpleTilte) > 2 and (i.group(3) == "plus" or i.group(3) == "+" ) :

                            phone="gS9+"

                        else:
                            #c est un Galaxy s6 !!!
                            phone="gS9"


    return phone


#================================================================
#Filtres pour consoles !!!!
#-----------------------------

def filter_games(SimpleTilte,Desc):
    
    SimpleTilte =  min_not_space(SimpleTilte)

    SimpleTilte =  min_not_space(SimpleTilte)

    Desc =  min_not_space(Desc)

    out = hs_finder(SimpleTilte,Desc)

    if out == True :

        phone = "broken"

        return phone

    game= "not defined"

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

def filter_scoot(SimpleTilte,Desc):

    SimpleTilte =  min_not_space(SimpleTilte)

    SimpleTilte =  min_not_space(SimpleTilte)

    Desc =  min_not_space(Desc)

    #out = hs_finder(SimpleTilte,Desc)

    #if out == True :

        #phone = "broken"

        #return phone

    scoot= "not defined"

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

def decision(product,priceproduct):
    permission=False

    if product == "agility" and priceproduct < 551 and priceproduct > 99 :
        permission=True
    if product == "booster" and priceproduct < 651 and priceproduct > 99 :
        permission=True
    if product == "xbox1" and priceproduct < 161 and priceproduct > 89 :
        permission=True
    if product == "ps4" and priceproduct < 161 and priceproduct > 89 :
        permission=True
    if product == "switch" and priceproduct < 211 and priceproduct > 89 :
        permission=True
    if product == "switch+jeu" and priceproduct < 241 and priceproduct > 89 :
        permission=True
    if product == "ps4+jeu" and priceproduct < 171 and priceproduct > 89 :
        permission=True
    if product == "xbox1+jeu" and priceproduct < 171 and priceproduct > 89 :
        permission=True
    if product == "gS9" and priceproduct < 651 and priceproduct > 99: 
        permission=True
    if product == "gS8+" and priceproduct < 451  and priceproduct > 99:
        permission=True
    if product == "gS8" and priceproduct < 401  and priceproduct > 99:
        permission=True
    if product == "gS7Edge" and priceproduct <251 and priceproduct > 99 :
        permission=True
    if product == "gS7" and priceproduct <181 and priceproduct > 99 :
        permission=True
    if product == "gS6Edge+" and priceproduct <251 and priceproduct > 99 :
        permission=True
    if product == "gS6Edge" and priceproduct < 231 and priceproduct > 99:
        permission=True
    if product == "gS6" and priceproduct < 171 and priceproduct > 99:
        permission=True
    if product == "iphone x" and priceproduct < 801 and priceproduct > 601 :
        permission=True
    if product == "iphone 5c" and priceproduct < 71:
        permission=True
    if product == "iphone 5s" and priceproduct < 71:
        permission=True
    if product == "iphone 6" and priceproduct < 161 and priceproduct > 99:
        permission=True
    if product == "iphone 6+" and priceproduct < 211 and priceproduct > 99:
        permission=True
    if product == "iphone 6s" and priceproduct < 221 and priceproduct > 99:
        permission=True
    if product == "iphone 6s+" and priceproduct < 251 and priceproduct > 99:
        permission=True
    if product == "iphone 7" and priceproduct < 391 and priceproduct > 99:
        permission=True
    if product == "iphone 7+" and priceproduct < 401 and priceproduct > 99:
        permission=True
    if product == "iphone 8" and priceproduct < 601 and priceproduct > 99:
        permission=True
    if product == "iphone 8+" and priceproduct < 601 and priceproduct > 99:
        permission=True    

    return permission



def is_good(titre,desc,cat,price):
    
    obj = "not defined"

    if cat =="Motos":
        obj = filter_scoot(titre,desc)
   
    if cat =="Téléphonie":
        obj = filter_phone(titre,desc)

    if cat == "Consoles &amp; Jeux vidéo":
        obj = filter_games(titre,desc)

    IsGood = decision(obj,price)

    return IsGood