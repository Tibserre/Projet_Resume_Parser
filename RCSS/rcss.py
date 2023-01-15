# Test of the Fuzzywuzzy library to retrieve the similarity score for each RSS element for each skill of the candidate CV

# Do the following commands to run the program :
# pip install thefuzz
# pip install python-Levenshtein
# pip install pandas
# pip install openpyxl

import pandas as pd
from thefuzz import fuzz
from thefuzz import process
import Levenshtein as lev


def rcssSkillRecognition(skills: list[str]):

    RCSS = pd.ExcelFile("./RCSS/Referentiel_Competences.xlsx")
    df1 = pd.read_excel(RCSS, 'Compétences Métiers')
    df2 = pd.read_excel(RCSS, 'Compétences Applicatives')
    df3 = pd.read_excel(RCSS, 'Compétences Méthodo')
    df4 = pd.read_excel(RCSS, 'Compétences Outils')
    df5 = pd.read_excel(RCSS, 'Compétences Techniques')

    list_competences = [df2, df3, df4, df5] # Store all sheets in a list
    keepingSkillsRSSList = [] # List of candidate competencies (df2 to df5) selected in comparison with the RSS
    skillsList = [] # Final skill list after deleting all duplicates

    ########## Checking which list the skill is in ##########

    # Put each element of each 2nd column in a lower case
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


    ##### Skill recovery for df1 only #####
    for i in range(len(skills_metiers)):
        skills_metiers[i] = skills_metiers[i].split(" - ")

        #for item in skills_metiers[i]:
        for skill in skills:
            funnel = process.extract(skill.lower(), skills_metiers[i], scorer=fuzz.partial_ratio)
                

            for element in funnel:
                if (lev.ratio(element[0], skill.lower()) >= 0.85): # Subjective accuracy threshold that can be adjusted to regulate the data
                    res = " - ".join([str(item) for item in skills_metiers[i]]) # treatment of the line, to restore it to its original state
                    keepingSkillsRSSList.append(res) # Add the skill to the final list


    ##### Skill recovery for dataframes df2 to df5 #####
    for dataframe in list_competences:
        for skill in skills:
            secondColumn = dataframe.iloc[:, 1] # Retrieve only the second columns [1] of each excel sheet
            referentiel_SS = [item.lower() for item in secondColumn] # Return items of secondColumn in lowercase
            funnel = process.extract(skill.lower(), referentiel_SS, scorer=fuzz.token_set_ratio) # Based on Levenshtein distance calculations, links, memberships and string inversions

            for item in funnel:
                if (lev.ratio(item[0], skill.lower()) >= 0.75): # Subjective accuracy threshold that can be adjusted to regulate the data
                    keepingSkillsRSSList.append(item[0]) # Add the skill to list

    # Suppress all duplicates of "keepingSkillsRSSList"
    for item in keepingSkillsRSSList:
        if item not in skillsList:
            skillsList.append(item)


    # Checking in which list the skill belongs
    
    list_comp_metiers = []
    
    for element in skills_metiers:
        res = " - ".join([str(item) for item in element])
        for skill in skillsList:
            if res == skill:
                list_comp_metiers.append(skill)

    def get_matching_elements(lst, reference_lst):
        matching_elements = []
        for element in lst:
            if element in reference_lst:
                matching_elements.append(element)
        return matching_elements

    list_comp_applicatif = get_matching_elements(skills_applicatifs, skillsList)
    list_comp_methodo = get_matching_elements(skills_methodo, skillsList)
    list_comp_outils = get_matching_elements(skills_outils, skillsList)
    list_comp_technique = get_matching_elements(skills_technique, skillsList)


    dictionary = {
        'Skills_metiers': list_comp_metiers, 
        'Skills_applicatives': list_comp_applicatif, 
        'Skills_methodo': list_comp_methodo, 
        'Skills_outils': list_comp_outils, 
        'Skills_techniques': list_comp_technique
        }
    

    return dictionary