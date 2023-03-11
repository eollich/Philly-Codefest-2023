from flask import render_template, url_for, flash, redirect, request, abort, jsonify
from scheduler import app

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/dataPrivacyPolicy')
def dataPrivacyPolicy():
    return render_template('DataPrivacyPolicy.html', theme ="temp theme string")



@app.route('/analytics')
def analytics():
    return render_template('analytics.html', theme = "temp theme string")


@app.route('/settings')
def settings():
    from scheduler.python_scripts import gpt
    x = gpt.query("as of 2020 what is the longest running tv show")
    x = x['choices'][0]['message']['content']
    return render_template('settings.html', title='settings',theme="temp theme string", gpt=x)

@app.route('/gptTesting', methods=['GET','POST'])
def gptTesting():
    if request.method == "POST":
        data = request.form.get("query")
        from scheduler.python_scripts import gpt
        form_query = request.form.get("query")
        gpt_query = gpt.query(form_query)
        return render_template('gpt.html', gpt=gpt_query['choices'][0]['message']['content'])
    else:
        return render_template("gpt.html", gpt=None)

@app.route('/gptTestin', methods=["POST"])
def gptTestin():
    return "got here"
