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
    - **NEW** id

- Hako: les 3 premieres
- Tony: les autres

## BIBLIOTHEQUES NECESSSAIRES
import requests
from bs4 import BeautifulSoup as soup
from datetime import datetime

## PROBLEMES
- Tester la connection avant telecharger html
- le nouvelle type de page leboncoin. ex: https://www.leboncoin.fr/decoration/1375807336.htm?ca=21_s
