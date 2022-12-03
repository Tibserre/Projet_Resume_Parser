#from resume_parser.test import resumeparse
from resumeparse import resumeparse

data = resumeparse.read_file("./CV/CV - AMO.pdf") #data prend le dictionnaire et les linkedin skills

skills = []

for section, value in data.items():
    if(section == "linkedin skills"):
        lk_skills = value

    else:
        for sub_section, sub_value in value.items():
            if(sub_section == "skills"):
                for sub_sub_section, sub_sub_value in sub_value.items():
                    skills.append(sub_sub_value)
                    print(skills)
