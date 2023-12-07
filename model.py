from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///resources.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
db = SQLAlchemy(app)  # Use a single SQLAlchemy instance for the app

class Resources(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    student_id = db.Column(db.String(20), nullable=False)
    Course_Code = db.Column(db.String(10), nullable=False)
    f_type = db.Column(db.String(10), nullable=False)
    Description = db.Column(db.Text, nullable=False)
    up_file = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500))
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]))

class Faculty(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    initial = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    thesis_supervision = db.Column(db.String(10), nullable=False)
    research_interest = db.Column(db.String(100), nullable=False)
    routine = db.Column(db.String(255), nullable=True)

    def __repr__(self) -> str:
        return f"{self.sno}, Name: {self.full_name}, Email: {self.email}, Interest in Supervising: {self.thesis_supervision}, Research Interest: {self.research_interest}"
    
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    venue = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    info = db.Column(db.String(500), nullable=False)

class Internship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    requirements = db.Column(db.String(500), nullable=False)
    info = db.Column(db.String(500), nullable=False)

if __name__ == '__main__':
    with app.app_context():

        db.create_all()
    app.run(debug=True)
