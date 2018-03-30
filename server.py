#!/usr/bin/env python

import json
import datetime
import os
import threading
import webbrowser
import requests
from flask import Flask, render_template, session, request, redirect, url_for
from werkzeug.utils import secure_filename
from json2html import *

from aws import aws_fileupload, aws_read, replace

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = CUR_DIR + '/static/files/uploads'

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
    return ('success', 200)

@app.route("/processfile/<filename>")
def processfile(filename):
    try:
        aws_fileupload.file_upload(filename, UPLOAD_FOLDER)
        aws_result = aws_read.file_read(filename, UPLOAD_FOLDER)

        replace.main(json.loads(aws_result), filename, UPLOAD_FOLDER)
        return (filename, 200)
    except Exception:
        return (filename, 500)


@app.route("/history")
def history():
    kwargs = {}
    scans = [
        {
            'id' : '2018-03-17T17:40:42.907425',
            'patient_name' : 'Writwick Wraj',
            'original_filename' : 'static/assets/img/uploads/123.jpg',
            'output': '/uploads/16737-FederationFormat.jpg',
        },
        {
            'id' : '2018-03-17T17:40:42.907425',
            'patient_name' : 'Writwick Wraj',
            'original_filename' : 'static/assets/img/uploads/123.jpg',
            'output': '/uploads/16737-FederationFormat.jpg',
        },
        {
            'id' : '2018-03-17T17:40:42.907425',
            'patient_name' : 'Writwick Wraj',
            'original_filename' : 'static/assets/img/uploads/123.jpg',
            'output': '/uploads/16737-FederationFormat.jpg',
        },
        {
            'id' : '2018-03-17T17:40:42.907425',
            'patient_name' : 'Writwick Wraj',
            'original_filename' : 'static/assets/img/uploads/123.jpg',
            'output': '/uploads/16737-FederationFormat.jpg',
        },
        {
            'id' : '2018-03-17T17:40:42.907425',
            'patient_name' : 'Writwick Wraj',
            'original_filename' : 'static/assets/img/uploads/123.jpg',
            'output': '/uploads/16737-FederationFormat.jpg',
        },
    ]

    kwargs['scans'] = scans
    return render_template('history.html', **kwargs)


@app.route("/insights", methods=['GET', 'POST'])
def insights():
    token = '71c4161312f0f36b120f80f4b015717bee72c4e337fc4800840786fa50102ccb'
    if request.method == 'POST':
        query = request.form['query']
        r = requests.get(
            "http://www.healthos.co/api/v1/autocomplete/medicines/brands/" + query,
            headers={
                'Authorization': 'Bearer ' + token})

        if len(
                r.content) > 2:  # checking if the response has more than just two brackets []
            parsed = json.loads(r.content)
            for element in parsed:
                del element['medicine_id']
                del element['id']
                del element['search_score']
            # print (json.dumps(parsed, indent=4, sort_keys=True))
            finaltable = json2html.convert(json=parsed).replace('>','>\n')


            f = open("templates/template.html", "r")
            contents = f.readlines()
            f.close()
            cssname = """<link href="/static/assets/css/table.css" rel="stylesheet"/>"""
            contents.insert(27, cssname)
            contents.insert(39, finaltable)
            contents.insert(40,
                            """
                                <br><br>
                                <a href="/insights" class="button">Search again</a>
                            """)
            # contents.insert(58,"""<script src="/static/assets/js/table.js"></script>""")
            # ans=""
            # for x in contents:
            #     ans+=x;
            #     ans+='\n'
            f = open("templates/new.html", "w")
            contents = "".join(contents)
            f.write(contents)
            f.close()


            with open("templates/new.html", "r") as f:
                for num, line in enumerate(f, 1):
                    if num==39:
                        newline="""<table class="table" border="1">"""
                        line=newline
        else:
            f = open("templates/template.html", "r")
            contents = f.readlines()
            f.close()
            contents.insert(39, "<b>Your query returned no results.</b>")
            contents.insert(40,
                            """
                                <br><br>
                                <a href="/insights" class="button">Search again</a>
                            """)
            f = open("templates/new.html", "w")
            contents = "".join(contents)
            f.write(contents)
            f.close()
        return render_template('new.html')
    else:
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
        threading.Timer(1.00, lambda: webbrowser.open(url)).start()

    app.run(port=port)
