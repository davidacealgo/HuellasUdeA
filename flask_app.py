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
""" Ruta en donde se almacenan las imagenes en el backend"""
UPLOAD_FOLDER = '/home/osboxes/home/lis/Documents/Dormi/PDI/HuellasUdeA/python-fingerprint-recognition-master/database/'

"""Formatos de imagen permitidos"""
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

"""Se aplica la configuracion a la aplicacion"""
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    """Verificacion del metodo post"""
    if request.method == 'POST':
	"""Se obtiene la imagen enviada como archivo"""
        foto=request.files['image']
        if foto and allowed_file(foto.filename):
	    """Se verifica el formato por seguridad"""
            filename = secure_filename(foto.filename)
	    """Se guarda la imagen en la ruta indicada"""
            foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    	match=main(foto.filename)
        return match 

"""----------4. Iniciacion del servicio---------------------------------"""
if __name__ == "__main__":
	try:
		app.run(host='192.168.193.201',debug=False,port=9999)
	except:
		raise
