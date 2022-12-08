# %%writefile /content/resume_parser/resume_parser/resumeparse.py
# !apt-get install python-dev libxml2-dev libxslt1-dev antiword unrtf poppler-resumeparse pstotext tesseract-ocr
# !sudo apt-get install libenchant1c2a


# !pip install tika
# !pip install docx2txt
# !pip install phonenumbers
# !pip install pyenchant
# !pip install stemming

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

class resumeparse(object):
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

    def convert_docx_to_txt(docx_file, docx_parser):
        """
            A utility function to convert a Microsoft docx files to raw text.

            This code is largely borrowed from existing solutions, and does not match the style of the rest of this repo.
            :param docx_file: docx file with gets uploaded by the user
            :type docx_file: InMemoryUploadedFile
            :return: The text contents of the docx file
            :rtype: str
        """
        # try:
        #     text = docx2txt.process(docx_file)  # Extract text from docx file
        #     clean_text = text.replace("\r", "\n").replace("\t", " ")  # Normalize text blob
        #     resume_lines = clean_text.splitlines()  # Split text blob into individual lines
        #     resume_lines = [re.sub('\s+', ' ', line.strip()) for line in resume_lines if line.strip()]  # Remove empty strings and whitespaces

        #     return resume_lines
        # except KeyError:
        #     text = textract.process(docx_file)
        #     text = text.decode("utf-8")
        #     clean_text = text.replace("\r", "\n").replace("\t", " ")  # Normalize text blob
        #     resume_lines = clean_text.splitlines()  # Split text blob into individual lines
        #     resume_lines = [re.sub('\s+', ' ', line.strip()) for line in resume_lines if line.strip()]  # Remove empty strings and whitespaces
        #     return resume_lines
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

    def convert_pdf_to_txt(pdf_file):
        """
        A utility function to convert a machine-readable PDF to raw text.

        This code is largely borrowed from existing solutions, and does not match the style of the rest of this repo.
        :param input_pdf_path: Path to the .pdf file which should be converted
        :type input_pdf_path: str
        :return: The text contents of the pdf
        :rtype: str
        """
        # try:
        # PDFMiner boilerplate
        # pdf = pdfplumber.open(pdf_file)
        # full_string= ""
        # for page in pdf.pages:
        #   full_string += page.extract_text() + "\n"
        # pdf.close()

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

    def find_segment_indices(string_to_search, resume_segments, resume_indices):
        for i, line in enumerate(string_to_search):  # i itérateur, line : prend comme valeur chaque ligne du CV

            # Si la premiere lettre de la ligne est une minuscule, on sait que cette ligne est la
            # suite de la ligne précédente, donc on itère
            if line[0].islower():
                continue

            # On met la ligne en minuscule
            header = line.lower()
            header_rm_emphases = resumeparse.remove_emphases(header)

            # L'objectif de cette méthode est de récupérer l'indice de la ligne de chaque en-tête, ce qui permet de
            # délimiter les zones du CV

            # On prend chaque élément de la liste des objectifs de resumeparse et on le compare au début de notre ligne
            # contenue dans header
            if [o for o in resumeparse.objective if header.startswith(o)]:
                # Resume_segments est un dictionnaire en 2 dimensions, on verifie que la case du dictionnaire soit pleine
                try:
                    resume_segments['objective'][header]
                except:
                    # Notre case de dictionnaire est vide, on ajoute l'indice correspondant à notre ligne d'en-tête
                    # Le dictionnaire va contenir la position de son header correspondant
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
        # Il considere que tout ce qui est avant le premier indice de header contient les informations relatives à la
        # personne
        # Ex : Si votre premier header est votre formation et qu'elle commence à la ligne 3, resume_indices[0]=3 et il
        # considere que les informations de contact sont stockées dans les lignes 0 à 2
        resume_segments['contact_info'] = string_to_search[:resume_indices[0]]

        # resume_segments ={
        #    "work_and_employment" : {"professional experience" : "18",
        #                              "military experience" : "20"},
        #    "a" : {"b" : "c"}
        # }
        # a = section     : définit dans segment()
        # b = sub_section : header reconnu dans le CV lu
        # c = start_idx   : indice de la ligne du header
        # {b + c} = value
        for section, value in resume_segments.items():
            if section == 'contact_info':
                continue


            for sub_section, start_idx in value.items():
                # On initialise l'indice de fin de section à la fin de notre CV
                end_idx = len(string_to_search)
                # On regarde nos indices des headers pour faire la délimitation de nos sous-sections
                if (resume_indices.index(start_idx) + 1) != len(resume_indices):
                    end_idx = resume_indices[resume_indices.index(start_idx) + 1]

                # On remplace nos indices délimitant nos sous-sections par les string contenus dans celles-ci
                resume_segments[section][sub_section] = string_to_search[start_idx:end_idx]


    def segment(string_to_search):
        resume_segments = {
            'objective': {},
            'work_and_employment': {},
            'education_and_training': {},
            'skills': {},
            'linkedin_skills': {}, #skills extraits du fichier LINKEDIN_SKILLS_ORIGINAL.txt
            'accomplishments': {},
            'misc': {}
        }

        # Liste qui contient les indices de position des segments
        resume_indices = []

        # On determine la position de chaque header
        resumeparse.find_segment_indices(string_to_search, resume_segments, resume_indices)

        # On détermine la place de contact info et on remplace les indices de toutes les sous-sections par leurs valeurs
        # en string
        if len(resume_indices) != 0:
            resumeparse.slice_segments(string_to_search, resume_segments, resume_indices)
        else:
            resume_segments['contact_info'] = []

        return resume_segments

    def read_file(file, docx_parser="tika"):
        """
        file : Give path of resume file
        docx_parser : Enter docx2txt or tika, by default is tika
        """
        # file = "/content/Asst Manager Trust Administration.docx"
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

        resume_lines_treated = resumeparse.resume_lines_treatment(resume_lines)

        resume_segments = resumeparse.segment(resume_lines_treated)
        resume_segments['linkedin_skills'] = resumeparse.flat_linkedin_recognition('resumeparserFolder/LINKEDIN_SKILLS_ORIGINAL.txt', resumeparse.pre_treatment(resume_lines))

        '''
        resumeparse.save_skills_lists_in_file(resume_segments, "Skills section.txt")
        resumeparse.save_skills_lists_in_file(linkedin_skills, "Skills linkedin.txt")
        '''

        return resume_segments

    '''
    Fonction pre traitement du CV pour les donnees categorisees
    '''
    def resume_lines_treatment(resume_lines):
        resume_lines_treated = []  # pré-traitement sur les lignes du CV

        for lines in resume_lines:
            lines = lines.replace('◼', '')  # enleve bullet points
            lines = lines.replace('•', '')  # enleve bullet points
            lines = lines.replace('·', '')  # enleve bullet points
            lines = lines.strip()
            resume_lines_treated.append(lines)

        return resume_lines_treated
    '''
    Fonction de pre-traitement de nos donnees issues du CV
    '''
    def pre_treatment(text):
        bigString = " ".join(text) #On cree un unique string avec l'entierete des donnees du CV
        bigString = bigString.lower() #On met tout en minuscule
        bigString = resumeparse.remove_emphases(bigString) #Enleve les accents
        bigString = resumeparse.remove_punct(bigString) #Enleve la ponctuation
        bigString = resumeparse.remove_stopwords(bigString) #Enleve les mots inutiles francais et anglais
        bigString = resumeparse.remove_duplicate(bigString) #Enleve les doublons
        bigString = " ".join(bigString)
        return bigString


    '''
    Fonction de recherche exacte des skills sur l'ensemble du CV dans le fichier des Linkedin skills
    '''
    def flat_linkedin_recognition(file_path, text):
        with open(file_path, 'r', encoding="utf-8") as file:
            # read all content of a file
            list_competences = file.readlines()

        result = []
        for word in list_competences:
            wLower = word.strip().lower()
            if wLower in text.split(): #si une chaine de caractere est présente dans une autre chaine de caractere
                result.append(word.rstrip('\n')) #ajoute le resultat a la liste et enleve le \n

        return result

    '''
    Fonction qui enleve les accents d'un string
    '''
    def remove_emphases(text):
        return unidecode.unidecode(text) #enleve accent

    '''
    Fonction pour enlever la ponctuation d'un string
    On exclut les caracteres choisis dans exclude et on l'applique avec la fonction translate
    '''
    def remove_punct(text):
        exclude = string.punctuation
        #On a choisi de ne pas exclure le '+' qui est dans string.punctuation de base notamment pour skill C++
        #donc on remplace le + de notre string exclude par ''
        exclude = exclude.replace('+', '')
        exclude = exclude.replace('#', '')
        return text.translate(str.maketrans('', '', exclude))

    '''
    Fonction pour enlever les mots inutiles anglais et francais
    On constitue la liste de ces mots dans 'stop_words' grace aux fonctions de stopword
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
                words_without_stop_word.append(word) #Constitue la nouvelle liste de mots sans les stop_words
        return words_without_stop_word

    '''
    Fonction pour enlever les doublons
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
    Fonction pour récupérer les compétences optimisées pour Fuzzywuzzy
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
    Fonction qui return notre dictionnaire au format json
    '''
    def getJson(data):
        return json.dumps(data, indent=2, ensure_ascii=False)
