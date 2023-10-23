from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# from flask_wtf import csrf

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///resources.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.app_context().push()

class Resources(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    student_id = db.Column(db.String(20), nullable=False)
    Course_Code = db.Column(db.String(10), nullable=False)
    f_type = db.Column(db.String(10), nullable=False)
    Description = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # def __repr__(self) -> str:
    #     return f"{self.Course_Code} - {self.Description}"
    
@app.route('/')
def home():
    resource=Resources(email='admin.gmail',student_id='20301357',Course_Code='cse110',f_type='lab',Description='lab files')
    db.session.add(resource)
    db.session.commit()
    
    
    return render_template('index.html')


@app.route('/Add_resources',methods=['GET','POST'])
def Add_resources():
    if request.method=="POST":
        print(request.form['Course_Code'])
    return render_template('Add_resources.html')

@app.route('/view')
def View():
    all_resource=Resources.query.all()
    return render_template('view.html',all_resource=all_resource)


@app.route('/show')
def Show():
    all_resource=Resources.query.all()
    print(all_resource)
    return 'show'
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)