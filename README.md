# chatenoud_delorme

## TACHES A FAIRE
- Creer des fonctions pour rendre esthetique des informations
- Remarque: une fonction pour chaque information
    - name
    - category
    - region
    - prix
    - date (necessiter d'une fonction pour traiter la date actuelle)
    - lien de l'annonce
- grouper des departements en categories en fonction de la distance
    - scrap des noms de villes - Hako #
    - scrap des coordonnees - Tony #
    - calculer la distance - Hako #
- lister des categories que l'on veut - Hako
- stocker des donnees - Tony
- modifier get_price pour gagner du temps (marcher que avec des categories interessantes) - Tony
j'ai creer 2 fonctions pour prendre le prix (get_price_li et get_price_desc)
- Tester la connection avant telecharger html
- achitecture du programme principal - ensemble
- tester la fonction principale
- Pour le titre et la desc, suprimmer les accents et les changer sous forme minuscule - Hako
    - Pour changer sous forme minuscule: s.lower() avec s est une variable 'string'
- Ameliorer l'architecture principale pour avoir moins de perte de X (integrer la page 2) - Hako
- probleme de distance avec code postal <--> leboncoin - Tony
- Regular Expression pour classifier des annonces - Hako
- ameliorer le programme pricipal pour ne perdre plus d'annonce - Tony
==================================================================


## BIBLIOTHEQUES NECESSSAIRES
import requests
import re
from bs4 import BeautifulSoup as soup
from datetime import datetime
from math import sqrt
from math import asin
from math import sin
from math import cos
import sqlite3 as sql
import time
from datetime import datetime as dt

## PROBLEMES
- leboncoin viens de changer l'interface de page. Il faut tester plus, notamment la fonc get_desc.
- Ne reussir pas de telecharger le html de certaines annonces
- Le tableau des codes postaux et des coordonnees manque certaines communes -> trouver le code postal le plus proche -> il y a une erreur de distance
