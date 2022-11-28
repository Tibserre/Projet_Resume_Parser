from RCSS.rcss import rcssSkillRecognition
# Import functions from resume_parser file of Anne & Nicolas:
# from resumeParser.resume_parser import getContacts, getSkillsList, getFormation, getExperiences
import json


# skills = getSkillsList() (Liste des compétences extraites du CV du candidat venant de la fonction dans le fichier resume_parser d'Anne & Nicolas)
skills = ["sql", "C++", "Postman", "c", "C#", "Gestion documents", "CDP", "Corea"]

# Test de la fonction avec une liste de compétences aléatoire
rcssSkillRecognition(skills=skills)


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


#
# Fonction qui permet de faire la connection à la base de données NoSql (MongoDB?):
# Récupérer le JSON du CV "getJsonOfResume()"" au moment de l'enregistrement dans la collection de CV
