from flask import Flask, request
from flask.ext.uploads import UploadSet, configure_uploads, IMAGES
import matplotlib.pyplot as plt
from app import main

app = Flask(__name__)
photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = '/home/estudiantes/davida.acevedo/Downloads/Archivospython/python-fingerprint-recognition-master/database/'
configure_uploads(app, photos)
@app.route('/')
def index():
	return "Hello World"
	

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        nombre=request.form.get('name')
        foto=request.form.get('image')
    	print("paso")
    	main(foto)
        return null

if __name__ == "__main__":
	try:
		app.run(host='192.168.194.6',debug=False,port=8000)
	except:
		raise