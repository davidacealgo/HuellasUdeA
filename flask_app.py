"""-------------------------------------------------------------------------------------------
----------  Procesamiento de huellas digitales -----------------------------------------------
----------  Por: Cristian Dario Pulido   -----------------------------------------------------
----------       David Alejandro Acevedo -----------------------------------------------------
----------       Orion Montoya           -----------------------------------------------------
----------       Alvaro Chacon           -----------------------------------------------------
----------Curso de procesamiento digital de imagenes------------------------------------------
----------Universidad de Antioquia------------------------------------------------------------
----------Medellin 2018-----------------------------------------------------------------------
"""

"""----------1. Inicializacion del sistema e insercion de librerias---------------------------------"""

from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from app import main

app = Flask(__name__)
""" Ruta en donde se almacenan las imagenes en el backend""""
UPLOAD_FOLDER = '/home/osboxes/Documents/HuellasUdeA/python-fingerprint-recognition-master/database/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']) """Formatos de imagen permitidos"""
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER """"Se aplica la configuracion a la aplicaciòn"""

"""Metodo para verificar el formato de la imagen"""
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

"""----------2. Indexacion de la ruta de inicio---------------------------------"""

@app.route('/')
def index():
	return "Bienvenido, identificador de huellas digitales."
	
"""----------3. Funcionamiento ante un metodo post por la ruta /upload ---------------------------------"""
@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST': """Verificacion del metodo post"""
        foto=request.files['image']"""Se obtiene la imagen enviada como archivo""""
        if foto and allowed_file(foto.filename):
            filename = secure_filename(foto.filename)"""Se verifica el formato por seguridad"""
            foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))"""Se guarda la imagen en la ruta indicada"""
    	match=main(foto.filename)
        return match 

"""----------4. Iniciacion del servicio---------------------------------"""
if __name__ == "__main__":
	try:
		app.run(host='192.168.0.6',debug=False,port=9999)
	except:
		raise
