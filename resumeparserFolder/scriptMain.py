# This script allows to retrieve the json of the candidate's resume according to the choice 
# to use or not the word recognition system via Fuzzywuzzy before being called by the API

from resumeparserFolder.resumeparse import resumeparse
from RCSS.rcss import rcssSkillRecognition

import json


'''Without Fuzzywuzzy'''

def getJsonOfResume(data: dict):
        resume = {
            'formation' :                  data['education_and_training'], # get formation in json format
            'professionnal_experiences':   data['work_and_employment'],    # get experiences in json format
            'skills':                      data['skills'],                 # get skills_JSON
            'linkedin_skills':             data['linkedin_skills']         # get linkedin_skills
        }

        resume_Json = json.dumps(resume, indent=2, ensure_ascii=False)
        return resume_Json


'''With Fuzzywuzzy'''

def getJsonOfResumeWithFuzzy(data: dict):
        resume = {
            'formation':                    data['education_and_training'],  # get formation in json format
            'professionnal_experiences':    data['work_and_employment'],  # get experiences in json format
            'skills':                       rcssSkillRecognition(skills=resumeparse.getAllSkills(data)),  # get skills_JSON
        }

        resume_Json = json.dumps(resume, indent=2, ensure_ascii=False)
        return resume_Json
