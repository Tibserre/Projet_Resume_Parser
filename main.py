#from resume_parser.test import resumeparse
#Pour first commit branche dev
from resumeparse import resumeparse

data = resumeparse.read_file("./CV/CV_NicolasBEQUE_English.pdf")
print(data)