from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, Response,send_file,send_from_directory,redirect, url_for
import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///resources.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
db = SQLAlchemy(app)  # Use a single SQLAlchemy instance for the app
app.app_context().push()

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
    department = db.Column(db.String(100), nullable=False)
    thesis_supervision = db.Column(db.String(10), nullable=False)
    research_interest = db.Column(db.String(100), nullable=False)
    routine = db.Column(db.String(255), nullable=True)

    def __repr__(self) -> str:
        return f"{self.sno}, Name: {self.full_name}, Email: {self.email}, Interest in Supervising: {self.thesis_supervision}, Department: {self.department}, Research Interest: {self.research_interest}"

    
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

class Conference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    venue = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    info = db.Column(db.Text, nullable=False)

    
class Thesis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic_name = db.Column(db.String(255), nullable=False)
    department = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(1000), nullable=True)
   
def faculty_form_model(request):
    if request.method == 'POST':
        full_name = request.form['full_name']
        initial = request.form['initial']
        email = request.form['email']
        thesis_supervision = request.form['thesis_supervision']
        department=request.form['department']
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
            department=department,
            thesis_supervision=thesis_supervision,
            research_interest=research_interest,
            routine=filename  # Store the file name in the database
        )   
       
        
        db.session.add(new_faculty)
        db.session.commit()

    
    return render_template('faculty_form.html')
def add_comment_model():
    text = request.form.get('comment_text')
    parent_id = request.form.get('parent_id', None)

    new_comment = Comment(text=text, parent_id=parent_id)
    db.session.add(new_comment)
    db.session.commit()

    return redirect(url_for('postt'))
def delete_comment_model(comment_id):
    comment_to_delete = Comment.query.get(comment_id)

    if comment_to_delete:
        # Delete the comment and its replies
        db.session.delete(comment_to_delete)
        db.session.commit()

    return redirect(url_for('postt'))
def submit1_model(request):
    if 'file_path' in request.files:
        file_path = request.files['file_path']
        if file_path.filename != '':
            # Retrieve form data
            name = request.form.get('name')
            pos = request.form.get('pos')

            # Handle file upload
            filename = secure_filename(file_path.filename)
            file_path.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Save data to the database
            new_thesis = Thesis(topic_name=name, department=pos, file_path=filename)
            db.session.add(new_thesis)
            db.session.commit()

    # Redirect to the page displaying all the theses
    return render_template('community.html')

def delete_model(sno):
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

def Add_resources_model(request):
    filename2 = None
    if request.method == "POST":
        Course_Code = request.form['Course_Code'].upper()
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

def get_file_model(sno):
    resource = Resources.query.get_or_404(sno)
    return Response(resource.up_file, content_type="application/octet-stream") 

def submit_model(comments,ratings,course_codes,Serials):
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
names=[]
emails=[]
c_names=[]
c_types=[]
dess=[]
def submitt_model(request):
    global names,emails,c_names,c_types,dess
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
def get_alumni_info():
    global names,emails,c_names,c_types,dess
    return names,emails,c_names,c_types,dess
def submittt_model(request):
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
def submitttt_model(request):
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
def submittttt_model(request):
    name = request.form.get('name')
    venue = request.form.get('venu')
    description = request.form.get('edes')
    info = request.form.get('info')

    if name and venue and description and info:
        # Save the conference to the database
        new_conference = Conference(name=name, venue=venue, description=description, info=info)
        db.session.add(new_conference)
        db.session.commit()

    return redirect(url_for('conference'))

class Alumni(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    company_name = db.Column(db.String(100), nullable=False)
    company_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
if __name__ == '__main__':
    with app.app_context():

        db.create_all()
    app.run(debug=True)
