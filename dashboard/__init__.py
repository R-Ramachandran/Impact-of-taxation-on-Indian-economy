from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fac5f35dc32ba113029dad3eb831d7d1'

from dashboard import routes