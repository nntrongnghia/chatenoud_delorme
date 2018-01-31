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
==================================================================
- lister des categories que l'on veut - Hako
- modifier get_price pour gagner du temps (marcher que avec des categories interessantes) - Tony mais apres Hako
- grouper des departements en categories en fonction de la distance
    - scrap des noms de villes - Hako #
    - scrap des coordonnees - Tony #
    - calculer la distance - Hako
- achitecture du programme principal - ensemble
- stocker des donnees - Tony


## BIBLIOTHEQUES NECESSSAIRES
import requests
from bs4 import BeautifulSoup as soup
from datetime import datetime

## PROBLEMES
- Tester la connection avant telecharger html
- get_price takes much time
- get_date with urgent annonce
- get_price et get_desc - pour ne pas charger le html de l'annonce 2 fois.
- leboncoin viens de changer l'interface de page. Il faut tester plus, notamment la fonc get_desc.
- la fonc get_desc a besoin modeliser pour chaque categorie.
- C'est mieux d'obtenir le code postal, parce que le code est unique, c'est facile a comparer, a traiter. Si on n'a que le nom de ville ou departement, le traitement sera plus difficile.