from flask import Flask, json, request, jsonify

# Il peut être necessaire de décommenter import CORS et CORS(app) plus bas pour éviter les soucis de CORE policy
# from flask_cors import CORS
import os
import urllib.request
from threading import Thread, Lock

from werkzeug.utils import secure_filename
from resumeparserFolder import scriptMain
from resumeparserFolder.resumeparse import resumeparse

app = Flask(__name__)
# CORS(app)


app.secret_key = "caircocoders-ednalan"

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


# définition des extensions acceptées par le resume parser
ALLOWED_EXTENSIONS = set(['docx', 'pdf'])


def allowed_file(filename):
    """
    Cette fonction prend en paramètre un nom de fichier (filename) et vérifie que l'extension de ce fichier est bien dans la liste des extensions autorisées définies dans la variable ALLOWED_EXTENSIONS. Elle renvoie True si l'extension est autorisée, False sinon.
    """

    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def main():
    return 'Bonjour SOPRA STERIA'


def uploadCV(files):
    """
    Cette fonction prend en paramètre une liste de fichiers (files)
    et permet de les uploader dans le dossier "uploads" de l'application.
    Elle vérifie également que les fichiers uploadés sont bien des fichiers
    de type 'docx' ou 'pdf' en utilisant la fonction allowed_file(filename).
    Elle renvoie True si l'upload a été effectué avec succès, False sinon.
    """
    files = request.files.getlist('files[]')

    errors = {}
    success = False

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            success = True
        else:
            errors[file.filename] = 'File type is not allowed'
    return success


def validateCV(files):

    """
    Cette fonction prend également en paramètre une liste de fichiers (files) et vérifie que ces fichiers ont bien été uploadés en utilisant la fonction uploadCV(files). Elle renvoie une réponse HTTP en fonction du résultat de cette vérification.
    """
    errors = {}
    success = False
    # check if the post request has the file part
    if 'files[]' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp

    if uploadCV(files):  # si l'upload a retourné true
        success = True
    else:
        errors['message'] = 'File type is not allowed'

    if success and errors:
        errors['message'] = 'File(s) successfully uploaded'
        resp = jsonify(errors)
        resp.status_code = 500
        return resp
    if success:
        resp = jsonify({'message': 'Files successfully uploaded'})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify(errors)
        resp.status_code = 500
        return resp


def read_resumes(files, fuzzy):

    """
    Cette fonction prend en paramètre une liste de fichiers (files) et un booléen (fuzzy) qui indique si on souhaite utiliser la fonction de comparaison "fuzzy" ou non. Elle utilise la librairie resumeparse pour lire les fichiers uploadés et utilise la fonction scriptMain.getJsonOfResume ou scriptMain.getJsonOfResumeWithFuzzy pour extraire les informations du fichier. Cette fonction renvoie un dictionnaire contenant les informations extraites de chaque fichier.
    """

    allResumes = {}

    for file in files:
        fileName = str(file.filename)
        file_name = fileName.replace(" ", "_")
        path_to_file = "uploads/"+str(file.filename)
        pathCorr = path_to_file.replace(" ", "_")
        data = resumeparse.read_file(pathCorr)

        # original json struct
        if fuzzy == "true":
            jsonExtr = scriptMain.getJsonOfResumeWithFuzzy(data)
        else:
            jsonExtr = scriptMain.getJsonOfResume(data)

        # On transforme en dict pour travailler avec, et ajout d'une clé et d'une valeur
        jsonExtrCastedToDict = json.loads(jsonExtr)
        # jsonExtrCastedToDict["NameFile"]= file_name

        allResumes[file_name] = jsonExtrCastedToDict

    return allResumes


result = None  # initialisation d'une variable globale, cette variable contient le résultat du parsing des CV
lock = Lock()  # le lock permet d'éviter certains soucis lors de l'utilisation du multi thread



#
@app.route('/resume-parser', methods=['GET'])
def getResumeParser():
    with lock:
        return result


@app.route('/resume-parser', methods=['POST'])
def resumeParser():
    files = []
    files = request.files.getlist('files[]')
    fuzzy = request.form.get('fuzzy')  # get la valeur du param fuzzy
    responseJson = {}

    if 'files[]' not in request.files:  # check si dans request files
        rep = "Aucun fichier"
        responseJson["reponse"] = rep
        return responseJson
    else:
        if uploadCV(files) == True:

            t = Thread(target=parsingFiles, args=(files, fuzzy,))

            t.start()
            rep = "Files uploaded"
            responseJson["reponse"] = rep
            return responseJson
        else:
            rep = "not uploaded"
            responseJson["reponse"] = rep
            return responseJson


def parsingFiles(files, fuzzy):
    global result

    with lock:
        responseJson = {}
        rep = "Travail en cours..."
        responseJson["reponse"] = rep
        result = responseJson
    with lock:
        JsonExtre = read_resumes(files, fuzzy)
        responseJson["reponse"] = JsonExtre
        result = responseJson
        deleteFilesUploaded(files)


def deleteFilesUploaded(files):
    for file in files:
        file_to_delete = "uploads/"+str(file.filename)
        file_to_delete_corr = file_to_delete.replace(" ", "_")
        os.remove(file_to_delete_corr)


if __name__ == '__main__':
    app.run(host="localhost", port=2000, debug=True)
