from flask import Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = '112665d4a46cd2053a877d88dbd4fa5e'
from scheduler import routes
