#!/usr/bin/env python3

import os
import glob
import time
import flask
import qrcode
import urllib.parse
from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory
from config import uploadr as config
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
encode = urllib.parse.quote
decode = urllib.parse.unquote

def check_create(dir):
    if not os.path.isdir(dir):
        os.makedirs(dir)

check_create(config.uploads)
check_create(config.qrcodes)

@app.route("/")
@app.route('/upload', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        time_uploaded = str(time.time())
        file_dir = config.uploads + '/' + filename
        check_create(file_dir)
        check_create(file_dir + '/' + time_uploaded)
        f.save(config.uploads 
                + '/' + encode(filename)
                + '/' + time_uploaded
                + '/' + filename)
        return render_template('upload_success.html',
                link = filename + '?version=' + time_uploaded,
                port = config.port,
                )
    else:
        return render_template('upload.html',
                port = config.port,
                )

@app.route('/qrcodes/<filename>')
def qrcodes(filename):
    link = 'http://{0}:{1}/download/{2}?version={3}'.format(
            config.domain
            , config.port
            , encode(filename)
            , request.args.get('version')
            )
    image = qrcode.make(link)
    with open(config.qrcodes + '/' + filename+ '.png', mode = 'bw+') as file:
        image.save(file)
    return send_from_directory(config.qrcodes, filename + '.png', as_attachment=True)

@app.route('/qr/<filename>')
def qr(filename=None):
    return render_template('qr.html'
            , imagesrc = 'http://{0}:{1}/qrcodes/{2}?version={3}'.format(
                 config.domain
                , config.port
                , filename
                , request.args.get('version')
                )
            )

@app.route('/download/<filename>')
def download(filename=None):
    provided_version = request.args.get('version')
    directory_base = config.uploads + '/' + filename + '/'
    directory = directory_base + str(provided_version)
    if not os.path.isdir(directory):
        existing_versions = glob.glob(directory_base + '*')
        existing_versions.sort()
        latest_version = existing_versions[-1]
        directory = latest_version 

    return flask.send_from_directory(directory, decode(filename), as_attachment=True)

@app.route('/css/<filename>')
def css(filename=None):
    return flask.send_from_directory('css', filename)

@app.route('/fonts/<filename>')
def fonts(filename=None):
    return flask.send_from_directory('fonts', filename)

if __name__ == '__main__':
    app.debug = True
    app.run()
