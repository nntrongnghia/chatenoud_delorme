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
==================================================================
- achitecture du programme principal - ensemble



## BIBLIOTHEQUES NECESSSAIRES
import requests
from bs4 import BeautifulSoup as soup
from datetime import datetime

## PROBLEMES
- get_date with urgent annonce
- leboncoin viens de changer l'interface de page. Il faut tester plus, notamment la fonc get_desc.
- la fonc get_desc a besoin modeliser pour chaque categorie.
- C'est mieux d'obtenir le code postal, parce que le code est unique, c'est facile a comparer, a traiter. Si on n'a que le nom de ville ou departement, le traitement sera plus difficile.
- ** get_desc ** ne marche plus avec la nouvelle l'interface de leboncoin.