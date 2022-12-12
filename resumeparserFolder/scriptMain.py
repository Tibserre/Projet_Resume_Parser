
from resumeparserFolder.resumeparse import resumeparse
from RCSS.rcss import rcssSkillRecognition

import json

#data2 = resumeparse.read_file("./CV/CV - AMO.pdf")


'''Sans Fuzzywuzzy'''



def getJsonOfResume(data: dict):
        resume = {
            'formation' :                  data['education_and_training'], # get formation in json format
            'professionnal_experiences':   data['work_and_employment'],    # get experiences in json format
            'skills':                      data['skills'],                 # get skills_JSON
            'linkedin_skills':             data['linkedin_skills']         # get linkedin_skills
        }

        resume_Json = json.dumps(resume, indent=2, ensure_ascii=False)


    #print(getJsonOfResume(data))


'''Avec Fuzzywuzzy'''

def getJsonOfResumeWithFuzzy(data: dict):
        resume = {
            'formation':                    data['education_and_training'],  # get formation in json format
            'professionnal_experiences':    data['work_and_employment'],  # get experiences in json format
            'skills':                       rcssSkillRecognition(skills=resumeparse.getAllSkills(data)),  # get skills_JSON
        }

        resume_Json = json.dumps(resume, indent=2, ensure_ascii=False)


    #################################### SANDBOX ####################################

    # def getJsonOfResume():

    #     resume = {
    #         'contacts': resumeparse.getContact, # get infos/contact in json format
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


    #
    # Fonction qui permet de faire la connection à la base de données NoSql (MongoDB?):
    # Récupérer le JSON du CV "getJsonOfResume()"" au moment de l'enregistrement dans la collection de CV

