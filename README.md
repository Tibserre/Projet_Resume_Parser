# Resume Parser EPF

Ce projet permet de lire des CV, essentiellement des CV écrits en lignes (voir image ci dessous)<br/><br/>

<img src="https://binaries.templates.cdn.office.net/support/templates/en-us/lt02918880_quantized.png" width="300" >
<br/><br/><br/><br/>

# Setup
## Étape 1

Mettez en place un virtual environnement.
```bash 
# Création du virtualenv
venv venv

# Ouverture du virtual env
source venv/bin/activate
```
<br/><br/>
## Étape 2
### Dépendances

```bash 
# Ci dessous toutes les dépendances du projet, 
# certaines sont installées de base avec python
- certifi==2022.12.7
- cffi==1.15.1
- charset-normalizer==2.1.1
- click==8.1.3
- cryptography==39.0.0
- docx2txt==0.8
- et-xmlfile==1.1.0
- Flask==2.2.2
- idna==3.4
- importlib-metadata==6.0.0
- itsdangerous==2.1.2
- Jinja2==3.1.2
- joblib==1.2.0
- Levenshtein==0.20.9
- MarkupSafe==2.1.1
- nltk==3.8.1
- numpy==1.24.1
- openpyxl==3.0.10
- pandas==1.5.2
- pdfminer.six==20221105
- pdfplumber==0.7.6
- Pillow==9.4.0
- pycparser==2.21
- python-dateutil==2.8.2
- pytz==2022.7
- rapidfuzz==2.13.7
- regex==2022.10.31
- requests==2.28.1
- six==1.16.0
- SQLAlchemy==1.4.46
- thefuzz==0.19.0
- tika==2.6.0
- tqdm==4.64.1
- Unidecode==1.3.6
- urllib3==1.26.13
- Wand==0.6.10
- Werkzeug==2.2.2
- zipp==3.11.0

# Ces dépendances peuvent être necessaires pour faire fonctionner Flask-Cors.
# à installer au cas où l'étape 4 ne fonctionne pas

- cmake==3.25.0 
- Flask-Cors==3.0.10
- psycopg2-binary==2.9.5
```

`Tikka` utilise `JAVA`, il peut être donc nécessaire d'installer JAVA sur votre machine. 
<br/><br/>
## Étape 3 
Lancez le projet en vous mettant sur le fichier `resumeParserApi.py` et cliquez sur le bouton comme ci dessous

<img src="https://i.stack.imgur.com/Y5OKl.png" width="200" >

<br/><br/>
## Étape 4
Lancez le front. Pour cela, le plus simple et d'utiliser LiveServer sur Visual Studio Code. 
Mais attention, subtilité qui fonctionne sur MacOS facilement (surement aussi sur Windows)

Les requêtes risquent d'être bloquées par Chrome, à cause de CORS Policy. Pour éviter cela, dans votre terminal mettez la commande suivante 

```bash 
# À lancer dans votre terminal
open -n -a /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --args --user-data-dir="/tmp/chrome_dev_test" --disable-web-security
```

Vous aurez une fenêtre Chrome sans Core Policy 