from flask import Flask, render_template, request, Response,send_file,send_from_directory,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from itertools import groupby
from model import Resources,app,db,Comment,Faculty,Event,Internship
from flask_mail import Mail, Message
from dotenv import load_dotenv





load_dotenv('.env.local') #I might hide it because of security issues

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
def postt():
    comments = Comment.query.filter_by(parent_id=None).all()
    return render_template('postt.html', comments=comments)

@app.route('/add_comment', methods=['POST'])
def add_comment():
    text = request.form.get('comment_text')
    parent_id = request.form.get('parent_id', None)

    new_comment = Comment(text=text, parent_id=parent_id)
    db.session.add(new_comment)
    db.session.commit()

    return redirect(url_for('postt'))
@app.route('/delete_comment/<int:comment_id>', methods=['GET'])
def delete_comment(comment_id):
    comment_to_delete = Comment.query.get(comment_id)

    if comment_to_delete:
        # Delete the comment and its replies
        db.session.delete(comment_to_delete)
        db.session.commit()

    return redirect(url_for('postt'))

@app.route('/')
def homme():
    return render_template('index.html')
@app.route('/index')
def home():
    return render_template('index.html')
@app.route('/courseinfo')
def cinfo():
    return render_template('courseinfo.html')


#Faculty Section Started
@app.route('/faculty_form', methods=['GET', 'POST'])
def faculty_form():
    if request.method == 'POST':
        full_name = request.form['full_name']
        initial = request.form['initial']
        email = request.form['email']
        thesis_supervision = request.form['thesis_supervision']
        research_interest = request.form['research_interest']
        #routine = request.files['routine'].read()  # Read image file as binary data
        routine_file = request.files['routine']

        #routine = request.files['routine']
        #filename = secure_filename(routine.filename) 

        
        filename = secure_filename(routine_file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        routine_file.save(file_path)

        new_faculty = Faculty(
            full_name=full_name,
            initial=initial,
            email=email,
            thesis_supervision=thesis_supervision,
            research_interest=research_interest,
            routine=filename  # Store the file name in the database
        )   
       
      

        
        
        db.session.add(new_faculty)
        db.session.commit()

    
    return render_template('faculty_form.html')


@app.route('/faculty')
def faculty():
    faculty = Faculty.query.all()
    return render_template('faculty.html', faculty=faculty)

@app.route('/faculty_description/<int:sno>', methods=['GET', 'POST'])
def delete(sno):
    faculty = Faculty.query.filter_by(sno=sno).first()
    faculty_email= faculty.email 
    print(faculty_email)
    if request.method == 'POST':
        sender = request.form['sender']
        subject = request.form['subject']
        body = request.form['body']
        print(sender)
        print(subject) 
        print(body)
        # Create a message object
        message = Message(subject=subject,
                          sender=sender,
                          recipients=[faculty_email],
                          body=body)

        try:
    # Send the email
            mail.send(message)
            return 'Email sent successfully!'
        except Exception as e:
            app.logger.error(f"Failed to send email: {str(e)}")
            return 'Failed to send email. Please check logs for more details.'

    
    return render_template('faculty_description.html', faculty=faculty)

#faculty Section Ended

@app.route('/Add_resources', methods=['GET', 'POST'])
def Add_resources():
    filename2 = None
    if request.method == "POST":
        Course_Code = request.form['Course_Code']
        email = request.form['email']
        student_id = request.form['student_id']
        f_type = request.form['f_type']
        Description = request.form['Description']


        up_file = request.files['up_file']

        if up_file:
            
            # file_data = up_file.read()
            filename2 = up_file.filename  # Get the filename
           
            resource = Resources(
                email=email, up_file=filename2, student_id=student_id, Course_Code=Course_Code,
                f_type=f_type, Description=Description
            )

            db.session.add(resource)
            db.session.commit()
            up_file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(up_file.filename)))
    all_resource = Resources.query.all()
    return render_template('Add_resources.html', all_resource=all_resource, filename2=filename2)


@app.route('/view')
def View():
    all_resource=Resources.query.all()
    return render_template('view.html',all_resource=all_resource)
@app.route('/community')
def community():
    return render_template('community.html')


@app.route('/Alumni')
def Alumni():
    return render_template('Alumni.html')
@app.route('/get_file/<int:sno>')
def get_file(sno):
    resource = Resources.query.get_or_404(sno)
    return Response(resource.up_file, content_type="application/octet-stream")  # Update the content type based on the file type

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    # Access the file name
    filename = file.filename

    # You can now use the 'filename' variable as needed
    return f'Uploaded file name: {filename}'
@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/serve_file/<filename>')
def serve_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)






@app.route('/cse1')
def cse1():
    all_resource=Resources.query.filter(Resources.Course_Code.like('cse1%')).all()
    grouped_resources = {}
    
    # Group resources by course code
    all_resource.sort(key=lambda x: x.Course_Code)
    for course_code, resources in groupby(all_resource, key=lambda x: x.Course_Code):
        grouped_resources[course_code] = list(resources)
    
    return render_template('cse1.html', grouped_resources=grouped_resources)

comments = []
ratings = []
Serials=[]
course_codes=[]


@app.route('/comment')
def comment():
    return render_template('comment.html', course_data=zip(course_codes, Serials, comments, ratings))



@app.route('/submit', methods=['POST'])
def submit():
    comment = request.form.get('comment')
    rating = request.form.get('rating')
    course_code=request.form.get('course_code')
    Serial=request.form.get('num')
   

    if comment and rating and course_code and Serial:
        comments.append(comment)
        ratings.append(int(rating))
        course_codes.append(course_code)
        Serials.append(Serial)

    return redirect(url_for('comment'))


#alumny
names= []
emails = []
c_names=[]
dess=[]
c_types=[]

@app.route('/alumni')
def alumni():
   
    return render_template('alumni.html', alumnyy=zip(names, emails, c_names,c_types, dess))

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
    events_from_db = Event.query.all()
    return render_template('event.html', events=events_from_db)

@app.route('/submittt', methods=['POST'])
def submittt():
    name = request.form.get('name')
    venue = request.form.get('venu')
    description = request.form.get('edes')
    info = request.form.get('info')

    if name and venue and description and info:
        # Save the event to the database
        event = Event(name=name, venue=venue, description=description, info=info)
        db.session.add(event)
        db.session.commit()

    return redirect(url_for('event'))



#Internship
interns = []

@app.route('/intern')
def intern():
    interns_from_db = Internship.query.all()
    return render_template('intern.html', internn=interns_from_db)

@app.route('/submitttt', methods=['POST'])
def submitttt():
    name = request.form.get('name')
    pos = request.form.get('pos')
    req = request.form.get('req')
    info = request.form.get('info')

    if name and pos and req and info:
        # Save the internship to the database
        intern = Internship(name=name, position=pos, requirements=req, info=info)
        db.session.add(intern)
        db.session.commit()

    return redirect(url_for('intern'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)