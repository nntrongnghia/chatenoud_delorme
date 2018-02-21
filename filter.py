def min_not_space(t):
    t = t.replace(" ","").replace("-","").replace("_","")
    return t.lower().replace("è","e").replace("é","e").replace("ê","e")

def filter_iphone(SimpleTilte):
    target = re.compile(r'(iphone)').findall(SimpleTilte)
    if len(target) != 0:
        #print("i phone")
        return True
    else :
        #print("not i phone")
        return False



#================================================================
#Filtres pour telephones !!!!
#-----------------------------

def filter_phone(SimpleTilte):
    SimpleTilte =  min_not_space(SimpleTilte)

    phone= "not defined"

    SimpleTilte = min_not_space(SimpleTilte)

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
                            phone="g S6 Edge +"

                        else :
                            #c est un Galaxy s6 edge !!!
                            phone="g S6 Edge"

                    else:
                        #c est un Galaxy s6 !!!
                        phone="g S6"

#-------------------------------------------------------------------------------
# Galaxy S 7
#-------------------------------------------------------------------------------
                if i.group(2) == "7":
                        if len(SimpleTilte) > 2 and i.group(3) == "edge" :

                            phone="g S7 Edge"

                        else:
                            #c est un Galaxy s6 !!!
                            phone="g S7"

                if i.group(2) == "8":
                        if len(SimpleTilte) > 2 and (i.group(3) == "plus" or i.group(3) == "+" ) :

                            phone="g S8 +"

                        else:
                            #c est un Galaxy s6 !!!
                            phone="g S8"


                if i.group(2) == "9":
                        if len(SimpleTilte) > 2 and (i.group(3) == "plus" or i.group(3) == "+" ) :

                            phone="g S9 +"

                        else:
                            #c est un Galaxy s6 !!!
                            phone="g S9"


    return phone


#================================================================
#Filtres pour consoles !!!!
#-----------------------------

def filter_games(SimpleTilte):
    SimpleTilte =  min_not_space(SimpleTilte)

    game= "not defined"

    SimpleTilte = min_not_space(SimpleTilte)

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

def filter_scoot(SimpleTilte):
    SimpleTilte =  min_not_space(SimpleTilte)

    scoot= "not defined"

    SimpleTilte = min_not_space(SimpleTilte)

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

