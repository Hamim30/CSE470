from flask import Flask, render_template, request, Response,send_file,send_from_directory,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from itertools import groupby

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///resources.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'

db = SQLAlchemy(app)

app.app_context().push()

class Resources(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    student_id = db.Column(db.String(20), nullable=False)
    Course_Code = db.Column(db.String(10), nullable=False)
    f_type = db.Column(db.String(10), nullable=False)
    Description = db.Column(db.Text, nullable=False)
    up_file=db.Column(db.String(100), nullable=False)

    date_created = db.Column(db.DateTime, default=datetime.utcnow)
