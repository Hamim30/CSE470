from flask import Flask, render_template, request, Response,send_file,send_from_directory,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from itertools import groupby
from model import Resources,app,db,Comment,Faculty,Event,Internship,Conference,Thesis
from flask_mail import Mail, Message
import view
import model



#create a .env.local named file
# Inside .env file
# MAIL_SERVER=smtp.example.com
# MAIL_PORT=587
# MAIL_USERNAME=your_email@example.com
# MAIL_PASSWORD=your_password
# MAIL_USE_TLS=Trues
# MAIL_USE_SSL=False

#Follow THis Instructions for Creating Password to access from mail
# Create & use app passwords
# Important: To create an app password, you need 2-Step Verification on your Google Account.

# If you use 2-Step-Verification and get a "password incorrect" error when you sign in, you can try to use an app password.

# Go to your Google Account.
# Select Security.
# Under "Signing in to Google," select 2-Step Verification.
# At the bottom of the page, select App passwords.
# Enter a name that helps you remember where you’ll use the app password.
# Select Generate.
# To enter the app password, follow the instructions on your screen. The app password is the 16-character code that generates on your device.
# Select Done.



app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL') == 'True'
mail = Mail(app)

@app.route('/postt')
def postt_view():
    comments = Comment.query.filter_by(parent_id=None).all()
    return render_template('postt.html', comments=comments)

@app.route('/add_comment', methods=['POST'])
def add_comment():
    return model.add_comment_model()

@app.route('/delete_comment/<int:comment_id>', methods=['GET'])
def delete_comment(comment_id):
    return model.delete_comment_model(comment_id=comment_id)

@app.route('/thesisjournal')
def thesis_journal():
    return view.thesis_journal_view()

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/submit1', methods=['POST','GET'])
def submit1():
    return model.submit1_model(request=request)

@app.route('/')
def homme():
    return view.homme_view()
@app.route('/index')
def home():
    return view.home_view()
@app.route('/courseinfo')
def cinfo():
    return view.cinfo_view()


#Faculty Section Started
@app.route('/faculty_form', methods=['GET', 'POST'])
def faculty_form():
    return model.faculty_form_model(request)


@app.route('/faculty')
def faculty():
    return view.faculty_view()

@app.route('/faculty_description/<int:sno>', methods=['GET', 'POST'])
def delete(sno):
    return model.delete_model(sno)

@app.route('/Add_resources', methods=['GET', 'POST'])
def Add_resources():
    return model.Add_resources_model(request)


@app.route('/view')
def View():
    return view.View_view()

@app.route('/community')
def community():
    return view.community_view()


@app.route('/Alumni')
def Alumni():
    return view.Alumni_view()

@app.route('/get_file/<int:sno>')
def get_file(sno):

    return model.get_file_model(sno)

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return "No file part"

#     file = request.files['file']

#     if file.filename == '':
#         return "No selected file"

#     # Access the file name
#     filename = file.filename

#     # You can now use the 'filename' variable as needed
#     return f'Uploaded file name: {filename}'
@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


@app.route('/cse1')
def cse1():
    return view.cse1_view()


@app.route('/cse2')
def cse2():
    return view.cse2_view()

@app.route('/cse3')
def cse3():
    return view.cse3_view()

@app.route('/cse4')
def cse4():
    return view.cse4_view()



comments = []
ratings = []
Serials=[]
course_codes=[]


@app.route('/comment')
def comment():
    return view.comment_view(course_codes, Serials, comments, ratings)



@app.route('/submit', methods=['POST'])
def submit():
    return model.submit_model(comments,ratings,course_codes,Serials)




# @app.route('/alumni')
# def alumni():
#     return view.alumni_view(names, emails, c_names,c_types, dess)

# @app.route('/submitt', methods=['POST'])
# def submitt():
#     return model.submitt_model(names,emails,c_names,c_types,dess)

names= []
emails = []
c_names=[]
dess=[]
c_types=[]

@app.route('/alumni')
def alumni():
    alumnyy = [    ]
    for i in range(len(names)):
        alumnyy+=[{'name':names[i],'email':emails[i],'c_name':c_names[i],'c_type':c_types[i],'info':dess[i]}]

    print(alumnyy)
    return render_template('alumni.html', alumnyy=alumnyy)

@app.route('/submitt', methods=['POST'])
def submitt():
    name = request.form.get('name')
    email = request.form.get('email')
    cname=request.form.get('cname')
    c_type=request.form.get('c_type')
    info=request.form.get('info')
   
    if name and email and cname and c_type and info:
        names.append(name)
        emails.append(email)
        c_names.append(cname)
        c_types.append(c_type)
        dess.append(info)
  

    return redirect(url_for('alumni'))



#Event
events = []

@app.route('/event')
def event():
    return view.event_view()

@app.route('/submittt', methods=['POST'])
def submittt():

    return model.submittt_model(request)



#Internship
interns = []

@app.route('/intern')
def intern():
    return view.intern_view()

@app.route('/submitttt', methods=['POST'])
def submitttt():
    return model.submitttt_model(request=request)
#conference
conferences = []

@app.route('/conference')
def conference():
    conferences_from_db = Conference.query.all()
    return render_template('conference.html', conferences=conferences_from_db)

@app.route('/submittttt', methods=['POST'])
def submittttt():
    return model.submittttt_model(request)

@app.route('/search', methods=['GET'])
def search():
    return view.search_view(request)
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)