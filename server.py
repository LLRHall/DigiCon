#!/usr/bin/env python

import threading
import webbrowser
from flask import Flask, render_template, session, request, redirect

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

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

