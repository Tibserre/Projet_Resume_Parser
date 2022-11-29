from flask import Flask
from RCSS.rcss import rcssSkillRecognition


app = Flask(__name__)

# skills = getSkillsList() (Liste des compétences extraites du CV du candidat venant de la fonction dans le fichier resume_parser d'Anne & Nicolas)
skills = ["sql", "C++", "Postman", "c", "C#", "Gestion documents", "CDP", "Corea"]

# Test de la fonction avec une liste de compétences aléatoire
rcssSkillRecognition(skills=skills)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/resume_parse")
def resume_parser():
    return

if __name__ == '__main__':
    app.run()   