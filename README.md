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
- Ameliorer l'architecture principale pour avoir moins de perte de X (integrer la page 2) - Hako
- Regular Expression pour classifier des annonces - Hako
==================================================================
- dans la nouvelle interface, la desc et le code postal ne sont pas trouves pour certains annonces - Tony

- probleme de distance avec code postal <--> leboncoin - Tony



## BIBLIOTHEQUES NECESSSAIRES
import requests
from bs4 import BeautifulSoup as soup
from datetime import datetime

## PROBLEMES
- leboncoin viens de changer l'interface de page. Il faut tester plus, notamment la fonc get_desc.





## PRIX a chercher 
 
iphone 5........:
iphone 5s.......:60
iphone 5c.......:60
iphone 6........:176
iphone 6+.......:
iphone 6s.......:
iphone 6s+......:
iphone 7........:
iphone 7+.......:
iphone 8........:
iphone 8+.......:
iphone X........:651
iphone SE.......:
Galaxy S6.......:151
Galaxy S6 Edge..:251
Galaxy S6 Edge +:251
Galaxy S7.......:251
Galaxy S7 Edge..:301
Galaxy S8.......:401
Galaxy S8+......:451
Galaxy S9.......:
Galaxy S9+......:
Nintedo Switch..:201
PlayStation4....:151
XboxOne.........:151
MBK Booster.....:551
Kymco Agility...:401
