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

- Hako: les 3 premieres
- Tony: les autres

## BIBLIOTHEQUES NECESSSAIRES
import requests
from bs4 import BeautifulSoup as soup
from datetime import datetime

## PROBLEMES
- Tester la connectioe avant telecharger html
- Il n'y a pas de prix
        (
            -chercher le prix dans la déscription
            -si le prix n'est pas dans détécté dans la description -->0 euros
            -si il ya plusieurs prix , --> 0 euros
        )