from flask import Flask, render_template,session,request,redirect
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/history")
def history():
    return render_template('history.html')

@app.route("/insights")
def insights():
    return render_template('insights.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/feedback")
def feedback():
    return render_template('feedback.html')


app.debug = True
app.run()
