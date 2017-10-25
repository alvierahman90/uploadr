import time
import flask
import os
import qrcode
from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory
from config import uploadr as config
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

if not os.path.isdir(config.uploads):
    os.makedirs(config.uploads)

if not os.path.isdir(config.qrcodes):
    os.makedirs(config.qrcodes)

@app.route("/")
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

@app.route('/qrcodes/<filename>')
def qrcodes(filename):
    link = 'http://{0}:{1}/download/{2}'.format(
            config.domain
            , config.port
            , filename
            )
    image = qrcode.make(link)
    with open('qrcodes/' + filename+ '.png', mode = 'bw+') as file:
        image.save(file)
    return send_from_directory(config.qrcodes, filename + '.png', as_attachment=True)

@app.route('/qr/<filename>')
def qr(filename=None):
    return render_template('qr.html', imagesrc = 'http://{0}:{1}/qrcodes/{2}'.format(
             config.domain
            , config.port
            , filename
            )
        )

@app.route('/download/<filename>')
def download(filename=None):
    if filename != None:
        return flask.send_from_directory(config.uploads, filename, as_attachment=True)
    else:
        return hello()

@app.route('/css/<filename>')
def css(filename=None):
    return flask.send_from_directory('css', filename)

@app.route('/fonts/<filename>')
def fonts(filename=None):
    return flask.send_from_directory('fonts', filename)

if __name__ == '__main__':
    app.debug = True
    app.run()
