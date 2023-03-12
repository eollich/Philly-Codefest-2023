import sys
from flaskwebgui import FlaskUI
from scheduler import app
if __name__ == "__main__":
    #if getattr(sys, 'frozen', False):
    #    app.run(debug=False)
    #else:
    #    app.run(debug = True)
    #final / deployment
    FlaskUI(app=app, server="flask").run()
    #app.run(debug=True)
