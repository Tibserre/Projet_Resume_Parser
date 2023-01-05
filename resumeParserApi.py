from flask import Flask, json, request, jsonify
#from flask_cors import CORS
import os
import urllib.request
from threading import Thread, Lock

from werkzeug.utils import secure_filename
from resumeparserFolder import scriptMain
from resumeparserFolder.resumeparse import resumeparse

app = Flask(__name__)
#CORS(app)

 
app.secret_key = "caircocoders-ednalan"
 
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['docx', 'pdf' ])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
@app.route('/')
def main():
    return 'Bonjour SOPRA STERIA'
 



def uploadCV(files):
 

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



def checkExt():
    if 'files[]' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
    else :
        resp = jsonify({'message' : 'One or more files in the request'})
        resp.status_code = 201
        return resp

def validateCV(files):
    errors = {}
    success = False
     # check if the post request has the file part
    if 'files[]' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp

    if uploadCV(files) :
                success = True
    else:
                errors ['message']  = 'File type is not allowed'
    
    if success and errors:
            errors['message'] = 'File(s) successfully uploaded'
            resp = jsonify(errors)
            resp.status_code = 500
            return resp
    if success:
            resp = jsonify({'message' : 'Files successfully uploaded'})
            resp.status_code = 201
            return resp
    else:
            resp = jsonify(errors)
            resp.status_code = 500
            return resp
    
 
 #

def read_resumes(files, fuzzy):
    
    
    allResumes = {}

    for file in files :
        fileName= str(file.filename)
        file_name = fileName.replace(" ", "_")
        path_to_file = "uploads/"+str(file.filename)
        pathCorr =path_to_file.replace(" ", "_")
        data = resumeparse.read_file(pathCorr)

        #original json struct 
        if fuzzy=="true":
            jsonExtr=scriptMain.getJsonOfResumeWithFuzzy(data)
        else : 
            jsonExtr=scriptMain.getJsonOfResume(data)

        #On transforme en dict pour travailler avec, et ajout d'une clé et d'une valeur
        jsonExtrCastedToDict = json.loads(jsonExtr)
        #jsonExtrCastedToDict["NameFile"]= file_name
  
        allResumes[file_name]=jsonExtrCastedToDict
        

    return allResumes
    
            
            #Que dict mais a la fin dict to json !
            # envoyer ici les fichiers pour les templates 

            #séparer en POST et GET 
            #
            # Post peut retourner un identifiant par ex ! lié au get 

result = None
lock = Lock()

@app.route('/resume-parser', methods=['GET'])
def getResumeParser():
    with lock:
        return result

@app.route('/resume-parser', methods=['POST'])   
def resumeParser():
    files = []
    files= request.files.getlist('files[]')
    fuzzy = request.form.get('fuzzy') #get la valeur du param fuzzy
    responseJson = {}
    
    
    if 'files[]' not in request.files:
        rep="Aucun fichier"
        responseJson["reponse"]=rep
        return responseJson
    else :
        if uploadCV(files)==True:

            t = Thread(target=parsingFiles,args=(files,fuzzy,))
           
            t.start()
            rep="Files uploaded"
            responseJson["reponse"]=rep
            return responseJson
        else :
            rep="not uploaded"
            responseJson["reponse"]=rep
            return responseJson 
            
def parsingFiles(files,fuzzy):
    global result

    with lock:
        responseJson = {}
        rep="Travail en cours..."
        responseJson["reponse"]=rep
        result = responseJson
    with lock:
        JsonExtre = read_resumes(files, fuzzy)
        responseJson["reponse"]=JsonExtre
        result = responseJson
        



if __name__ == '__main__':
    app.run(host="localhost", port=2000, debug=True)