from flask import Flask, json, request, jsonify
import os
import urllib.request

from werkzeug.utils import secure_filename
from resumeparserFolder import scriptMain
from resumeparserFolder.resumeparse import resumeparse
app = Flask(__name__)
 
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


"""
def validateCV(files):
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
    
    """

def read_resumes(files):
    fuzzy = request.form.get('fuzzy')
   
    for file in files :
        path_to_file = "uploads/"+str(file.filename)
        if fuzzy:
            data = resumeparse.read_file(path_to_file)
            JsonExtr=scriptMain.getJsonOfResume(data)
            return JsonExtr


@app.route('/resume-parser', methods=['POST'])   
def resumeParser():
    files = []
    files= request.files.getlist('files[]')
    

    if 'files[]' not in request.files:
        return 'notOK'
    else :
        if uploadCV(files)==True:
            #JsonExtre = resumeparse.read_file("CV/CV_NicolasBEQUE_English.pdf")
            JsonExtre = read_resumes(files)
            if JsonExtre == None :
                return "vide ptn"
            else :
                return JsonExtre

            
        else :
            return "not uploaded"
            

"""
@app.route('/resume-parser', methods=['POST'])   

def resumeParser():

    data:dict =""
    files = []
    files= request.files.getlist('files')
    fuzzy = request.form.get('fuzzy')
    
   

    if validateCV(files)==200:
        return "ok"
        for file in files:
            pathToFile = "./upload/"+"str(file.filename)"
            #data = resumeparse.read_file(pathToFile)
         

            if fuzzy == True:
                return scriptMain.getJsonOfResumeWithFuzzy(data)
            else :
                return scriptMain.getJsonOfResume(data)

"""
if __name__ == '__main__':
    app.run(host="localhost", port=2000,debug=True)