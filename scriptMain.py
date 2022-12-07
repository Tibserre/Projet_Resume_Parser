from RCSS.rcss import rcssSkillRecognition
from resumeparserFolder.resumeparse import read_file, getAllSkills
# from resumeParser.resume_parser import getContacts, getSkillsList, getFormation, getExperiences
import json


data = read_file("./CV/CV_NicolasBEQUE_English.pdf")


'''Sans Fuzzywuzzy'''


'''Avec Fuzzywuzzy'''
all_skills = getAllSkills(data)

print(all_skills)

rcssSkillRecognition(skills=all_skills)


#################################### SANDBOX ####################################

# def getJsonOfResume():

#     resume = {
#         'contacts': contacts, # get infos/contact in json format
#         'skills': , # get skills_JSON
#         'formation': formation, # get formation in json format
#         'experiences': experiences # get experiences in json format
#     }

#     resume_Json = json.dumps(resume)

#     return resume_Json


# def getJsonOfResumeWithFuzzy():

#     resume = {
#         'contacts': contacts, # get infos/contact in json format
#         'skills': rcssSkillRecognition(skills=skills), # get skills_JSON
#         'formation': formation, # get formation in json format
#         'experiences': experiences # get experiences in json format
#     }

#     resume_Json = json.dumps(resume)

#     return resume_Json


# Fonction qui permet de faire la connection à la base de données NoSql (MongoDB?):
# Récupérer le JSON du CV "getJsonOfResume()"" au moment de l'enregistrement dans la collection de CV

