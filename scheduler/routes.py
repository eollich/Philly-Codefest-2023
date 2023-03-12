from flask import render_template, url_for, flash, redirect, request, abort, jsonify, json
from scheduler import app
from scheduler.python_scripts.ics import ics_control
from scheduler.python_scripts.gpt import query2, generateQueryString
import os

ICS_DIR_PATH="scheduler/python_scripts/ics/ics_files"


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
        files = [ICS_DIR_PATH+"/"+x for x in os.listdir(ICS_DIR_PATH)]
        available_time_list= ics_control.getAvailableTime(files)
        time_slots = ics_control.find_time_slot(day, int(offset), data["needed"], int(data["hours"]), available_time_list) # starting day, offset days, type of meeting (Senior, General), number of hours needed, lsit of available times
        return render_template("index.html",time_slots = time_slots,title="schedule meeting" )
    else:
        return render_template("index.html", time_slots=[None], title="schedule meeting")

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
    return render_template("generateMeeting.html", info = request.form['time_slot'])

@app.route("/updateMeeting", methods=["POST"])
def updateMeeting():
    form = request.form
    time = form.get("time")
    time_list = time.split("-")
    day = int(time_list[0])
    start_hour = int(time_list[1].split(":")[0])
    end_hour = int(time_list[1].split(":")[1])
    title = form.get("title")
    desc = form.get("desc")
    roles = form.getlist("role")
    roles = [" ".join(role.split(":")) for role in roles]
    for role in roles:
        queryString = generateQueryString(title, desc, role)
        summary = query2(queryString)
        ics_control.add_new_event(ICS_DIR_PATH, role, title, summary, day, start_hour, end_hour)

    flash("Meeting successfully added to all relevant calendars", "success")
    #return render_template("generateMeeting.html", info= [day, start_hour, end_hour, title, summary, roles])
    return redirect(url_for('viewCalendar'))

@app.route("/viewCalendar", methods=["GET","POST"], defaults={'optional': None})
@app.route("/viewCalendar/<optional>", methods=["GET","POST"])
def viewCalendar(optional):
    import icalendar
    cal_data = None
    fil = None
    files = [x for x in os.listdir(ICS_DIR_PATH)]

    if request.method == "GET":
        if optional == None:
            fil = files[0]
        else:
            fil = optional
        cal_name = fil
        print(type(optional))
        print(f"OPTIONAL {optional}")
        with open(ICS_DIR_PATH+"/"+fil) as cal_file_data:
            calendar = icalendar.Calendar.from_ical(cal_file_data.read())
            events = []
            for component in calendar.walk():
                if component.name == "VEVENT":
                    start_date = component.get("dtstart").dt
                    end_date = component.get("dtend").dt
                    day = start_date.day
                    start_hour = start_date.hour
                    end_hour = end_date.hour
                    summary = component.get("summary")
                    title = component.get("title")
                    start_date = start_date.strftime("%Y-%m-%dT%H:%M:%S")
                    end_date = end_date.strftime("%Y-%m-%dT%H:%M:%S")
                    events.append((title, start_date, end_date, day, start_hour, end_hour, summary))
    else:
        return request.form

    return render_template("viewCalendar.html", cal_files = files, events = json.dumps(events), cal_name = cal_name, title="calender")

@app.route("/test")
def test():
    return render_template("temp.html")

@app.route("/cals/<name>")
def cal(name): 
    path = ICS_DIR_PATH+"/"+name
    with open(path, "r") as f:
        return f.read()
