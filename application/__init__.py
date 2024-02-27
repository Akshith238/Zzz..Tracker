from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt

app=Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:Akshith238@localhost:5432/SleepTrack'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'asojkxb'
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
from application import routes

