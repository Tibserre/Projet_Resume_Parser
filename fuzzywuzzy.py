# Test de la librairie Fuzzywuzzy pour récupérer le score de similarité pour chaque élément du RSS pour chaque skill du CV candidat
# Faire les commandes suivantes :
# pip install thefuzz
# pip install python-Levenshtein
# pip install pandas
# pip install openpyxl

import fuzzywuzzy
from thefuzz import fuzz
from thefuzz import process
import pandas as pd
import Levenshtein as lev

RSS = pd.ExcelFile("./Referentiel_Competences.xlsx")
df1 = pd.read_excel(RSS, 'Compétences Métiers')
df2 = pd.read_excel(RSS, 'Compétences Applicatives')
df3 = pd.read_excel(RSS, 'Compétences Méthodo')
df4 = pd.read_excel(RSS, 'Compétences Outils')
df5 = pd.read_excel(RSS, 'Compétences Techniques')

# TO DO : Traitement de la deuxième colonne de df1

list_competences = [df1, df2, df3, df4, df5] # Stocker l'ensemble des sheets dans une liste
keepingSkillsRSSList = [] # Liste des compétences du candidat retenues en comparaison avec le RSS

# skills étant la liste des compétences extraites du CV du candidat, à récupérer d'Anne & Nicolas
skills = ["scrum master", "sql", "C++", "Postman", ".net", "VBA", "jquery", "Angular", "CSS", "Javascript", "Java"]

for skill in skills:
    for dataframe in list_competences:
        secondColumn = dataframe.iloc[:, 1] # Récupérer uniquement les deuxièmes colonnes [1] de chaque feuille excel
        referentiel_SS = [item.lower() for item in secondColumn] # Return items of secondColumn in lowercase
        funnel = process.extract(skill.lower(), referentiel_SS, scorer=fuzz.token_set_ratio) # S'appuie sur les calculs de distance de Levenshtein, les liens, appartenances et inversions de chaÃ®ne de caractères
        # print('Similarity score: {}'.format(funnel))

        for item in funnel:
            if (lev.ratio(item[0], skill.lower()) >= 0.8): # Seuil de précision subjectif qui peut Ãªtre ajuster pour réguler les données
                keepingSkillsRSSList.append(item) # Add the skill to the final list

print(keepingSkillsRSSList)