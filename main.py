#from resume_parser.test import resumeparse
from resumeparse import resumeparse

data = resumeparse.read_file("./CV/CV_NicolasBEQUE_English.pdf")
print(data)
