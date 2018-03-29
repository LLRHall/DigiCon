#!/usr/bin/env python

import json
import datetime
import os
import threading
import webbrowser
from flask import Flask, render_template, session, request, redirect, url_for
from werkzeug.utils import secure_filename

from aws import aws_fileupload, aws_read, replace

CUR_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = CUR_DIR + '/uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/uploadfile", methods=['POST'])
def uploadfile():
    # check if the post request has the file part
    files = request.files.getlist("file[]")
    # if 'file' not in request.files:
    #     raise Exception('No file part')
    #     return redirect(request.url)
    for file in files:
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            raise Exception('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return (str(len(files)), 200)


@app.route("/processfile/<filename>")
def processfile(filename):
    aws_fileupload.file_upload(filename, UPLOAD_FOLDER)
    aws_result = aws_read.file_read(filename, UPLOAD_FOLDER)

    replace.main(json.loads(aws_result), filename, UPLOAD_FOLDER)

    return aws_result


@app.route("/history")
def history():
    kwargs = {}
    scans = [
        {
            'id': '2018-03-17T17:40:42.907425',
            'original_filename': 'somefilename.png',
            'output': 'outputfilename.png',
        },
        {
            'id': '2018-03-17T16:40:42.907425',
            'original_filename': 'somefilename.png',
            'output': 'outputfilename.png',
        },
        {
            'id': '2018-03-17T12:40:42.907425',
            'original_filename': 'somefilename.png',
            'output': 'outputfilename.png',
        },
        {
            'id': '2018-03-12T17:40:42.907425',
            'original_filename': 'somefilename.png',
            'output': 'outputfilename.png',
        },
        {
            'id': '2018-02-17T17:40:42.907425',
            'original_filename': 'somefilename.png',
            'output': 'outputfilename.png',
        },
        {
            'id': '2017-03-17T17:40:42.907425',
            'original_filename': 'somefilename.png',
            'output': 'outputfilename.png',
        },
    ]

    kwargs['scans'] = scans
    return render_template('history.html', **kwargs)

@app.route("/insights")
def insights():
    return render_template('insights.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/feedback")
def feedback():
    return render_template('feedback.html')


if __name__ == '__main__':
    app.debug = True
    port = 8000
    url = "http://127.0.0.1:{0}".format(port)
    print(""" * DigiCon v1.0 is running on port 8000\n
        Please open {0} in your browser to use the software.
        """.format(url))

    if not app.debug:
        threading.Timer(1.00, lambda: webbrowser.open(url) ).start()

    app.run(port=port)

