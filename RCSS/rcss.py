# Test de la librairie Fuzzywuzzy pour récupérer le score de similarité pour chaque élément du RSS pour chaque skill du CV candidat

# Faire les commandes suivantes pour pouvoir lancer le programme :
# pip install thefuzz
# pip install python-Levenshtein
# pip install pandas
# pip install openpyxl

import pandas as pd
from thefuzz import fuzz
from thefuzz import process
import Levenshtein as lev
import json

# skills étant la liste des compétences extraites du CV du candidat, à récupérer d'Anne & Nicolas
# skills = ["sql", "C++", "Postman", "c", "C#", "Gestion documents", "CDP", "Corea"]

def rcssSkillRecognition(skills: list[str]):

    RCSS = pd.ExcelFile("./RCSS/Referentiel_Competences.xlsx")
    df1 = pd.read_excel(RCSS, 'Compétences Métiers')
    df2 = pd.read_excel(RCSS, 'Compétences Applicatives')
    df3 = pd.read_excel(RCSS, 'Compétences Méthodo')
    df4 = pd.read_excel(RCSS, 'Compétences Outils')
    df5 = pd.read_excel(RCSS, 'Compétences Techniques')

    list_competences = [df2, df3, df4, df5] # Stocker l'ensemble des sheets dans une liste
    keepingSkillsRSSList = [] # Liste des compétences (df2 à df5) du candidat retenues en comparaison avec le RSS
    skillsList = [] # Liste de compétences finale après suppression de tous les duplicatats

    # Listes de chaque compétences triées par domaine à la fin du programme 
    list_comp_metiers = []
    list_comp_applicatif = []
    list_comp_methodo = []
    list_comp_outils = []
    list_comp_technique = []


    ########## Checking dans quelle liste se trouve le skill ##########

    # Mettre chaque élément de chaque 2ème colonne en lower case
    skills_metiers = df1.iloc[:, 1]
    skills_metiers = [item.lower() for item in skills_metiers]
    skills_applicatifs = df2.iloc[:, 1]
    skills_applicatifs = [item.lower() for item in skills_applicatifs]
    skills_methodo = df3.iloc[:, 1]
    skills_methodo = [item.lower() for item in skills_methodo]
    skills_outils = df4.iloc[:, 1]
    skills_outils = [item.lower() for item in skills_outils]
    skills_technique = df5.iloc[:, 1]
    skills_technique = [item.lower() for item in skills_technique]


    # Fonction qui permet d'enlever le premier mot avant le premier "-"
    # def substring_after(initialString, delimiter):
    #     return initialString.partition(delimiter)[2]


    ##### Récupération des compétences pour seulement pour df1 #####

    for i in range(len(skills_metiers)):
        # skills_metiers[i] = substring_after(skills_metiers[i], "- ") # Permet de supprimer le premier élément
        skills_metiers[i] = skills_metiers[i].split(" - ")

        for item in skills_metiers[i]:
            for skill in skills:
                funnel = process.extract(skill.lower(), skills_metiers[i], scorer=fuzz.partial_ratio)

                for element in funnel:
                    if (lev.ratio(element[0], skill.lower()) >= 0.85): # Seuil de précision subjectif qui peut être ajuster pour réguler les données
                        res = " - ".join([str(item) for item in skills_metiers[i]]) # traitement de la ligne, pour la remettre dans son état initial
                        keepingSkillsRSSList.append(res) # Add the skill to the final list


    ##### Récupération des compétences pour les dataframes df2 à df5 #####

    for dataframe in list_competences:
        for skill in skills:
            secondColumn = dataframe.iloc[:, 1] # Récupérer uniquement les deuxièmes colonnes [1] de chaque feuille excel
            referentiel_SS = [item.lower() for item in secondColumn] # Return items of secondColumn in lowercase
            funnel = process.extract(skill.lower(), referentiel_SS, scorer=fuzz.token_set_ratio) # S'appuie sur les calculs de distance de Levenshtein, les liens, appartenances et inversions de chaîne de caractères

            for item in funnel:
                if (lev.ratio(item[0], skill.lower()) >= 0.75): # Seuil de précision subjectif qui peut être ajuster pour réguler les données
                    keepingSkillsRSSList.append(item[0]) # Add the skill to list

    # Suppress all duplicates of "keepingSkillsRSSList"
    for item in keepingSkillsRSSList:
        if item not in skillsList:
            skillsList.append(item)

    # Checking dans quelle liste est la compétence
    for element in skills_metiers:
        res = " - ".join([str(item) for item in element])
        for skill in skillsList:
            if res == skill:
                list_comp_metiers.append(skill)

    for element in skills_applicatifs:
        for skill in skillsList:
            if element == skill:
                list_comp_applicatif.append(skill)

    for element in skills_methodo:
        for skill in skillsList:
            if element == skill:
                list_comp_methodo.append(skill)

    for element in skills_outils:
        for skill in skillsList:
            if element == skill:
                list_comp_outils.append(skill)

    for element in skills_technique:
        for skill in skillsList:
            if element == skill:
                list_comp_technique.append(skill)


    # Transform lists in JSON
    dictionary = {'Skills_metiers': list_comp_metiers, 'Skills_applicatives': list_comp_applicatif, 'Skills_methodo': list_comp_methodo, 'Skills_outils': list_comp_outils, 'Skills_techniques': list_comp_technique}
    skills_JSON = json.dumps(dictionary, indent=2)

    # Print in console a JSON
    # return skills_JSON
    return print(skills_JSON)


# Test de la fonction avec une liste de compétences aléatoire
# rcssSkillRecognition(skills=skills)