import time
import flask
import config
from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory
from werkzeug.utils import secure_filename
app = Flask(__name__)

@app.route("/")
@app.route("/hello/<name>")
def hello(name=None):
    return render_template('hello.html',name=name)

@app.route('/upload', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        f =request.files['file']
        print(secure_filename(f.filename))
        filename = str(time.time()) + '.' + secure_filename(f.filename).split('.')[-1]
        f.save('./uploads/' + filename)
        return render_template('upload_success.html', 
                filename = filename, 
                port = config.port, 
                )
    else:
        return render_template('upload.html', 
                port = config.port, 
                )

@app.route('/download/<filename>')
def download(filename=None):
    if filename != None:
        return flask.send_from_directory('uploads', filename, as_attachment=True)
    else:
        return hello()


@app.route('/css/<filename>')
def css(filename=None):
    return flask.send_from_directory('css', filename)

@app.route('/fonts/<filename>')
def fonts(filename=None):
    return flask.send_from_directory('fonts', filename)
