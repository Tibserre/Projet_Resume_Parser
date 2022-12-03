from RCSS.rcss import rcssSkillRecognition
# Import functions from resume_parser file of Anne & Nicolas:
# from resumeParser.resume_parser import getContacts, getSkillsList, getFormation, getExperiences
import json

from resumeparserFolder.resumeparse import resumeparse

data = resumeparse.read_file("./CV/CV_NicolasBEQUE_English.pdf")

def getAllSkills(data):
    organized_skills = []

    for section, value in data.items():
        if (section == "linkedin skills"):
            lk_skills = value
        else:
            for sub_section, sub_value in value.items():
                if (sub_section == "skills"):
                    for sub_sub_section, sub_sub_value in sub_value.items():
                        for last_values in sub_sub_value:
                            organized_skills.append(last_values)

    all_skills = []
    for skill in organized_skills:
        all_skills.append(skill)

    for skill in lk_skills:
        all_skills.append(skill)

    return all_skills

'''
# skills = getSkillsList() (Liste des compétences extraites du CV du candidat venant de la fonction dans le fichier resume_parser d'Anne & Nicolas)
skills = ["sql", "C++", "Postman", "c", "C#", "Gestion documents", "CDP", "Corea"]'''
all_skills = getAllSkills(data)

# Test de la fonction avec une liste de compétences aléatoire
rcssSkillRecognition(skills=all_skills)


#################################### SANDBOX ####################################

# Récupération et assemblage du JSON du CV avec toutes les informations extraites:
# def getJsonOfResume():

#     resume = {
#         'contacts': contacts, # get infos/contact in json format
#         'skills': rcssSkillRecognition(skills=skills), # get skills_JSON
#         'formation': formation, # get formation in json format
#         'experiences': experiences # get experiences in json format
#     }

#     convert into JSON:
#     resume_Json = json.dumps(resume)

#     Display the JSON in the console:
#     return print(resume_Json)


# Fonction qui permet de faire la connection à la base de données NoSql (MongoDB?):
# Récupérer le JSON du CV "getJsonOfResume()"" au moment de l'enregistrement dans la collection de CV

