from __future__ import division

import re
import os
import string

import docx2txt
from tika import parser
import pdfplumber
import logging
from nltk.corpus import stopwords
import json

import unidecode

'''
    Resumeparse class
    Computes the resume to give a dictionary regrouping the different
    sections from the resume and their content
'''
class resumeparse(object):
    '''
        List of the different headers that will be recognized by the resumeparser
        to make sections and subsections
        We have a french support of headers into each topic
    '''
    objective = (
        'career goal',
        'objective',
        'career objective',
        'employment objective',
        'professional objective',
        'career summary',
        'professional summary',
        'summary of qualifications',
        'summary',
        'objectif de carriere',
        'objectif',
        'objectif professionnel',
        'resume de carriere',
        'resume professionnel',
        'resume des qualifications',
        'resume',
        # 'digital'
    )

    work_and_employment = (
        'career profile',
        'employment history',
        'work history',
        'work experience',
        'experience',
        'professional experience',
        'professional experience/projects',
        'professional background',
        'additional experience',
        'career related experience',
        'related experience',
        'programming experience',
        'freelance',
        'freelance experience',
        'army experience',
        'military experience',
        'military background',
        'historique',
        'experience professionnelle',
        'experience',
        'carriere',
        'historique professionnel',
        'experience passee',
        'experiences',
        'experience militaire',
    )

    education_and_training = (
        'academic background',
        'academic experience',
        'programs',
        'courses',
        'related courses',
        'education',
        'qualifications',
        'educational background',
        'educational qualifications',
        'educational training',
        'education and training',
        'training',
        'academic training',
        'professional training',
        'course project experience',
        'related course projects',
        'internship experience',
        'internships',
        'apprenticeships',
        'college activities',
        'certifications',
        'special training',
        'formation',
        'education',
        'programmes',
        'cours suivis',
        'cours',
        'formation academique',
        'parcours',
        'parcours academique',
        'stage',
        'apprentissage',
        'formation en apprentissage',
        'diplomes',
    )

    skills_header = (
        'credentials',
        'areas of experience',
        'areas of expertise',
        'areas of knowledge',
        'skills',
        "other skills",
        "other abilities",
        'career related skills',
        'professional skills',
        'specialized skills',
        'technical skills',
        'computer skills',
        'personal skills',
        'computer knowledge',
        'technologies',
        'technical experience',
        'proficiencies',
        'languages',
        'language competencies and skills',
        'programming languages',
        'competencies',
        'domaine expertise',
        'domaine de compétence',
        'competences',
        'autres competences',
        'autres capacites',
        'competences professionnelles',
        'competences specialisees',
        'competences techniques',
        'competences informatique',
        'logiciels',
        'langues',
        'langage informatique',
        'langage de programmation',
        'langage',
        'connaissances informatique',
        'programming languages',
        'IT Skills',
        'Language',
        'competences fonctionnelles',
        'competences thematiques'
    )

    misc = (
        'activities and honors',
        'activities',
        'affiliations',
        'professional affiliations',
        'associations',
        'professional associations',
        'memberships',
        'professional memberships',
        'athletic involvement',
        'community involvement',
        'refere',
        'civic activities',
        'extra-Curricular activities',
        'professional activities',
        'volunteer work',
        'volunteer experience',
        'additional information',
        'interests',
        'interests & hobbies',
        'activites',
        'associations professionnelles',
        'adhesions',
        'adhesions professionnelles',
        'club sportif',
        'implication sportive',
        'centres d\'interet',
        'implication communautaire',
        'activites civiques',
        'activites extra-scolaires',
        'activites professionnelles',
        'volontariat',
        'benevolat',
        'informations additionnelles',
        'interets',
        'autres',
    )

    accomplishments = (
        'achievement',
        'licenses',
        'presentations',
        'conference presentations',
        'conventions',
        'dissertations',
        'exhibits',
        'papers',
        'publications',
        'professional publications',
        'research',
        'research grants',
        'project',
        'research projects',
        'personal projects',
        'current research interests',
        'thesis',
        'theses',
        'accomplissements',
        'licences',
        'publications professionnelles',
        'recherches',
        'projets',
        'bourses de recherche',
        'projets de recherche',
        'projets personnels',
    )

    """
        A utility function to convert a Microsoft docx files to raw text.

        This code is largely borrowed from existing solutions, and does not match the style of the rest of this repo.
        :param docx_file: docx file with gets uploaded by the user
        :type docx_file: InMemoryUploadedFile
        :return: The text contents of the docx file
        :rtype: str
    """
    def convert_docx_to_txt(docx_file, docx_parser):
        try:
            if docx_parser == "tika":
                text = parser.from_file(docx_file, service='text')['content']
            elif docx_parser == "docx2txt":
                text = docx2txt.process(docx_file)
            else:
                logging.error('Choose docx_parser from tika or docx2txt :: is not supported')
                return [], " "
        except RuntimeError as e:
            logging.error('Error in tika installation:: ' + str(e))
            logging.error('--------------------------')
            logging.error('Install java for better result ')
            text = docx2txt.process(docx_file)
        except Exception as e:
            logging.error('Error in docx file:: ' + str(e))
            return [], " "
        try:
            clean_text = re.sub(r'\n+', '\n', text)
            clean_text = clean_text.replace("\r", "\n").replace("\t", " ")  # Normalize text blob
            resume_lines = clean_text.splitlines()  # Split text blob into individual lines
            resume_lines = [re.sub('\s+', ' ', line.strip()) for line in resume_lines if
                            line.strip()]  # Remove empty strings and whitespaces
            return resume_lines, text
        except Exception as e:
            logging.error('Error in docx file:: ' + str(e))
            return [], " "

    """
        A utility function to convert a machine-readable PDF to raw text.

        This code is largely borrowed from existing solutions, and does not match the style of the rest of this repo.
        :param input_pdf_path: Path to the .pdf file which should be converted
        :type input_pdf_path: str
        :return: The text contents of the pdf
        :rtype: str
    """
    def convert_pdf_to_txt(pdf_file):
        try:
            raw_text = parser.from_file(pdf_file, service='text')['content']
        except RuntimeError as e:
            logging.error('Error in tika installation:: ' + str(e))
            logging.error('--------------------------')
            logging.error('Install java for better result ')
            pdf = pdfplumber.open(pdf_file)
            raw_text = ""
            for page in pdf.pages:
                raw_text += page.extract_text() + "\n"
            pdf.close()
        except Exception as e:
            logging.error('Error in docx file:: ' + str(e))
            return [], " "
        try:
            full_string = re.sub(r'\n+', '\n', raw_text)
            full_string = full_string.replace("\r", "\n")
            full_string = full_string.replace("\t", " ")

            # Remove awkward LaTeX bullet characters

            full_string = re.sub(r"\uf0b7", " ", full_string)
            full_string = re.sub(r"\(cid:\d{0,2}\)", " ", full_string)
            full_string = re.sub(r'• ', " ", full_string)

            # Split text blob into individual lines
            resume_lines = full_string.splitlines(True)

            # Remove empty strings and whitespaces
            resume_lines = [re.sub('\s+', ' ', line.strip()) for line in resume_lines if line.strip()]

            return resume_lines, raw_text
        except Exception as e:
            logging.error('Error in docx file:: ' + str(e))
            return [], " "

    '''
        Function that will find the indices of the lines matching our headers lists
    '''
    def find_segment_indices(string_to_search, resume_segments, resume_indices):
        for i, line in enumerate(string_to_search):  # i itérateur, line : prend comme valeur chaque ligne du CV

            # If the first letter of the line is lowercase, it belongs to the same sentence as the one before so we can
            # iterate
            if line[0].islower():
                continue

            # We lowercase the line
            header = line.lower()
            header_rm_emphases = resumeparse.remove_emphases(header)

            '''
                We'll look for the indices of the lines matching our headers lists which will allow us to delimit the 
                resume sections
            '''

            # Each element of the objective list of headers is compared to the beginning of our line contained in header
            if [o for o in resumeparse.objective if header.startswith(o)]:
                # Resume_segments is a dictionary in 2 dimensions, we first check if the cell has a value
                try:
                    resume_segments['objective'][header]
                except:
                    # Our cell is empty, we add the line index corresponding the header
                    # The dictionary contains the line index of its corresponding header
                    resume_indices.append(i)
                    header = [o for o in resumeparse.objective if header.startswith(o)][0]
                    resume_segments['objective'][header] = i
            elif [w for w in resumeparse.work_and_employment if header_rm_emphases.startswith(w)]:
                try:
                    resume_segments['work_and_employment'][header]
                except:
                    resume_indices.append(i)
                    list_header_recognized = [w for w in resumeparse.work_and_employment if header_rm_emphases.startswith(w)]
                    header = list_header_recognized[-1]
                    resume_segments['work_and_employment'][header] = i
            elif [e for e in resumeparse.education_and_training if header_rm_emphases.startswith(e)]:
                try:
                    resume_segments['education_and_training'][header]
                except:
                    resume_indices.append(i)
                    list_header_recognized = [e for e in resumeparse.education_and_training if  header_rm_emphases.startswith(e)]
                    header = list_header_recognized[-1]
                    resume_segments['education_and_training'][header] = i
            elif [s for s in resumeparse.skills_header if header_rm_emphases.startswith(s)]:
                try:
                    resume_segments['skills'][header]
                except:
                    resume_indices.append(i)
                    list_header_recognized = [s for s in resumeparse.skills_header if header_rm_emphases.startswith(s)]
                    header = list_header_recognized[-1]
                    resume_segments['skills'][header] = i
            elif [m for m in resumeparse.misc if header_rm_emphases.startswith(m)]:
                try:
                    resume_segments['misc'][header]
                except:
                    resume_indices.append(i)
                    list_header_recognized = [m for m in resumeparse.misc if header_rm_emphases.startswith(m)]
                    header = list_header_recognized[-1]
                    resume_segments['misc'][header] = i
            elif [a for a in resumeparse.accomplishments if header_rm_emphases.startswith(a)]:
                try:
                    resume_segments['accomplishments'][header]
                except:
                    resume_indices.append(i)
                    list_header_recognized = [a for a in resumeparse.accomplishments if header_rm_emphases.startswith(a)]
                    header = list_header_recognized[-1]
                    resume_segments['accomplishments'][header] = i

    def slice_segments(string_to_search, resume_segments, resume_indices):
        # We consider that everything which is before the first recognized header line index contains contact
        # information
        # Ex : If your first header is your education and that it begins on line 3 then resume_indices[0]=3 and it will
        # consider that contact info are within the line 0 to 2
        resume_segments['contact_info'] = string_to_search[:resume_indices[0]]

        # resume_segments ={
        #    "work_and_employment" : {"professional experience" : "18",
        #                              "military experience" : "20"},
        #    "a" : {"b" : "c"}
        # }
        # a = section     : defined in segment()
        # b = sub_section : header recognized in the resume
        # c = start_idx   : line index of the header
        # {b + c} = value
        for section, value in resume_segments.items():
            if section == 'contact_info':
                continue


            for sub_section, start_idx in value.items():
                # Initializing the end of section index at the end of our resume
                end_idx = len(string_to_search)
                # We can delimit our sub-sections thanks to the indexes from resume_indices
                if (resume_indices.index(start_idx) + 1) != len(resume_indices):
                    end_idx = resume_indices[resume_indices.index(start_idx) + 1]

                # Replacing our index by the strings
                resume_segments[section][sub_section] = string_to_search[start_idx:end_idx]


    def segment(string_to_search):
        resume_segments = {
            'objective': {},
            'work_and_employment': {},
            'education_and_training': {},
            'skills': {},
            'linkedin_skills': {}, #skills extracted from LINKEDIN_SKILLS_ORIGINAL.txt
            'accomplishments': {},
            'misc': {}
        }

        # List containing segment line indexes
        resume_indices = []

        # Determining header position
        resumeparse.find_segment_indices(string_to_search, resume_segments, resume_indices)

        # Determining the contact info segment
        if len(resume_indices) != 0:
            resumeparse.slice_segments(string_to_search, resume_segments, resume_indices)
        else:
            resume_segments['contact_info'] = []

        return resume_segments

    """
        Function read file which returns the full dictionary with the sorted information of the resume and the skills 
        recognized from Linkedin skills file
        file : Give path of resume file
        docx_parser : Enter docx2txt or tika, by default is tika
    """
    def read_file(file, docx_parser="tika"):
        file = os.path.join(file)
        if file.endswith('docx') or file.endswith('doc'):
            if file.endswith('doc') and docx_parser == "docx2txt":
                docx_parser = "tika"
                logging.error("doc format not supported by the docx2txt changing back to tika")
            resume_lines, raw_text = resumeparse.convert_docx_to_txt(file, docx_parser)
        elif file.endswith('pdf'):
            resume_lines, raw_text = resumeparse.convert_pdf_to_txt(file)
        elif file.endswith('txt'):
            with open(file, 'r', encoding='latin') as f:
                resume_lines = f.readlines()

        else:
            resume_lines = None

        #Pre-processing of the resume lines
        resume_lines_treated = resumeparse.resume_lines_treatment(resume_lines)

        resume_segments = resumeparse.segment(resume_lines_treated)
        resume_segments['linkedin_skills'] = resumeparse.flat_linkedin_recognition('resumeparserFolder/LINKEDIN_SKILLS_ORIGINAL.txt', resumeparse.pre_treatment(resume_lines))

        '''
        resumeparse.save_skills_lists_in_file(resume_segments, "Skills section.txt")
        resumeparse.save_skills_lists_in_file(linkedin_skills, "Skills linkedin.txt")
        '''

        return resume_segments

    '''
    Pre processing function of the resume for resume_segments
    '''
    def resume_lines_treatment(resume_lines):
        resume_lines_treated = []

        for lines in resume_lines:
            lines = lines.replace('◼', '')  # deleting bullet points
            lines = lines.replace('•', '')  # deleting bullet points
            lines = lines.replace('·', '')  # deleting bullet points
            lines = lines.strip()
            resume_lines_treated.append(lines)

        return resume_lines_treated
    '''
    Another pre processing function
    '''
    def pre_treatment(text):
        bigString = " ".join(text) #Unique string with the whole CV datas
        bigString = bigString.lower() #LowerCase everything
        bigString = resumeparse.remove_emphases(bigString) #Deleting emphasis
        bigString = resumeparse.remove_punct(bigString) #Deleting punctuation
        bigString = resumeparse.remove_stopwords(bigString) #Deleting useless words in French and English
        bigString = resumeparse.remove_duplicate(bigString) #Deleting duplicate words
        bigString = " ".join(bigString)
        return bigString


    '''
    Straightforward function to look for skills from the whole resume thanks to the linkedin skills
    '''
    def flat_linkedin_recognition(file_path, text):
        with open(file_path, 'r', encoding="utf-8") as file:
            # read all content of a file
            list_competences = file.readlines()

        result = []
        for word in list_competences:
            wLower = word.strip().lower()
            if wLower in text.split(): #if the word is within another the resume text
                result.append(word.rstrip('\n')) #adding the result and deleting \n

        return result

    '''
    Function deleting emphasis
    '''
    def remove_emphases(text):
        return unidecode.unidecode(text) #enleve accent

    '''
    Function deleting punctuation within a string
    '''
    def remove_punct(text):
        exclude = string.punctuation
        #We chose not to exclude '+' and '#' which are originally in string.punctuation for the skills like C++ and C#
        exclude = exclude.replace('+', '')
        exclude = exclude.replace('#', '')
        return text.translate(str.maketrans('', '', exclude))

    '''
    Function deleting useless French and english words
    We make this word list in 'stop_words'
    '''
    def remove_stopwords(text):
        #TODO Demander la langue du CV
        stop_words = stopwords.words('english') + stopwords.words('french')
        words_without_stop_word = []

        tokens = text.split(" ")
        for word in tokens:
            if word in stop_words:
                continue
            else:
                words_without_stop_word.append(word) #New list without stop_words
        return words_without_stop_word

    '''
    Function deleting duplicates
    '''
    def remove_duplicate(text):
        text = list(dict.fromkeys(text))
        return text

    def save_skills_lists_in_file(list, filename):
        with open(filename, 'w') as fp:
            for item in list:
                # write each item on a new line
                fp.write("%s\n" % item)
            print('Done')



    '''
    Function getting the optimized skills for Fuzzywuzzy
    '''
    def getAllSkills(data: dict):
        organized_skills = []

        lk_skills = []

        for section, value in data.items():
            if (section == "linkedin_skills"):
                lk_skills = value
            if (section == "skills"):
                for sub_section, sub_value in value.items():
                    for last_values in sub_value:
                        organized_skills.append(last_values)

        all_skills = []

        for skill in organized_skills:
            all_skills.append(skill)

        for skill in lk_skills:
            all_skills.append(skill)

        return resumeparse.remove_duplicate(all_skills)

    '''
    Function returning our dictionary in json format
    '''
    def getJson(data):
        return json.dumps(data, indent=2, ensure_ascii=False)
