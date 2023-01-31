# Script de scrapping de Books to Scrape

Ce script effectue une récupération automatique des données de vente des livres sur le site Books to Scraps : prix, titres, quantité disponible, etc. L'extraction se fait au lancement du script et non de manière récurrente. Les données sont chargées dans des fichiers au format csv par catégorie. Le chargement des images est optionnel (voir ci-dessous).

## Mettre en place l'environnement virtuel

Ce script est développé en Python. Il est optimisé pour être executé dans un environnement virtuel adéquat. Ceci est détaillé ci-après. 

### Création de l'environnement

Depuis le dossier où a été cloné le repository ou celui où les fichiers du scrypt ont été copiés,
entrez dans un terminal la commande suivante pour créer un environnement virtuel nommé *"venv"* :  
```
python -m venv env
```

### Activation de l'environnement

Ensuite, activez l'environnement ainsi créé à l'aide de la commande correspondant
selon votre plateforme.  
Les commandes appropriées sont récapitulées dans la documentation à cette adresse : <https://docs.python.org/fr/3/library/venv.html#how-venvs-work>  
Vous devez remplacer `<venv>` par `env` si vous avez respecter la création de l'environnement
sous ce nom, comme indiqué dans la commande initiale.  
Par exemple, sous PowerShell sur Linux, cela donne :
```
env/bin/Activate.ps1
```

### Installation des paquets requis

Enfin, vous pouvez installer l'ensemble des paquets requis à l'installation de ce script à l'aide de `pip` et du fichier *requirements.txt*. 
Pour cela, utilisez la commande suivante :
```
pip install -r requirements.txt
```

Vous pouvez vérifier que votre environnement est fonctionnel et dispose des paquets nécessaires en executant `pip freeze` dans votre terminal.

## Exécuter le script

Une fois dans un environnement Python ayant les pré-requis nécessaires, le script peut facilement être utilisé en executant le fichier *main.py*.
En se placant à la base du dossier, cela correspond donc à faire :
```
python main.py
```

## Export (optionnel) des images

L'export des images pouvant être source d'une forte utilisation de la bande passante et du stockage du système, cette fonctionnalité a été rendue optionnelle. De plus, les images sont susceptibles de peu évoluer ; il peut être pertinent de ne pas les charger à chaque extraction des données.  

Pour ne pas charger les données, il faut indiquer `False` au paramètre `load_img` de la fonction `export_data_from_category()`.  
Ce qui donne, au sein du fichier *main.py* (ligne 8 et 9) :  
```
export_data_from_category(url_category, get_data_folder(), load_img=False)
```