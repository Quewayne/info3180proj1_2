from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://wjnonwavrglabx:YQe4s9WC1BrREXcIS0zHtwer_3@ec2-107-22-246-250.compute-1.amazonaws.com:5432/d8fp3kgeebcmqn'
db = SQLAlchemy(app)

from app import views, models
