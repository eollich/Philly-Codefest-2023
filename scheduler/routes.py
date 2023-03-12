from flask import render_template, url_for, flash, redirect, request, abort, jsonify
from scheduler import app
from scheduler.python_scripts.ics import ics_control
import os

@app.route('/',methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        data = request.form
        offset = 0
        if data["offset"] == "month":
            offset = 30
        else:
            offset = 7
        day = int(data["starting_date"].split("-")[2])
        #return request.form
        partial_path = "scheduler/python_scripts/ics/ics_files"
        files = [partial_path+"/"+x for x in os.listdir(partial_path)]
        available_time_list= ics_control.getAvailableTime(files)
        time_slots = ics_control.find_time_slot(day, int(offset), data["needed"], int(data["hours"]), available_time_list) # starting day, offset days, type of meeting (Lead, General), number of hours needed, lsit of available times
        return render_template("index.html",time_slots = time_slots)
    else:
        return render_template("index.html", time_slots=[None])

@app.route('/dataPrivacyPolicy')
def dataPrivacyPolicy():
    return render_template('DataPrivacyPolicy.html', theme ="temp theme string")




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


@app.route("/generateMeeting", methods=["POST"])
def generateMeeting():
    print(type(request.form.get('time_slot')))
    return render_template("generateMeeting.html", info = request.form)
