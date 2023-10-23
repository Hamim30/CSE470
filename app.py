from flask import Flask, render_template, request, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import FileField
from sqlalchemy import LargeBinary
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
    up_file=db.Column(db.LargeBinary)

    date_created = db.Column(db.DateTime, default=datetime.utcnow)


    # def __repr__(self) -> str:
    #     return f"{self.Course_Code} - {self.Description}"
  
@app.route('/')
def home():
    
    
    
    return render_template('index.html')


@app.route('/Add_resources',methods=['GET','POST'])
def Add_resources():
    if request.method=="POST":
        Course_Code = request.form['Course_Code']
        email = request.form['email']
        student_id = request.form['student_id']
        f_type = request.form['f_type']
        Description = request.form['Description']

        up_file = request.files['up_file'] 

        if up_file:
            file_data = up_file.read()

            resource = Resources(
                email=email,up_file=file_data, student_id=student_id, Course_Code=Course_Code,
                f_type=f_type, Description=Description
            )

            db.session.add(resource)
            db.session.commit()
    all_resource=Resources.query.all()
    return render_template('Add_resources.html',all_resource=all_resource)


    return render_template('Add_resources.html')
 
# from flask import send_file
# import io
# @app.route('/view/<int:sno>')
# def View(sno):
#     resource = Resources.query.get(sno)
#     if resource is None:
#         return "Resource not found", 404
#     return send_file(io.BytesIO(resource.up_file), mimetype='image/png')


from flask import Flask, render_template
import base64

# ... (previous code) ...

@app.route('/view')
def View():
    images = Resources.query.all()
    
    base64_images = [[base64.b64encode(image.up_file).decode("utf-8"),image] for image in images]
    return render_template('view.html', base64_images=base64_images)

# ... (previous code) ...


@app.route('/show')
def Show():
    all_resource=Resources.query.all()
    print(all_resource,"=============")
    
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)