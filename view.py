from model import Resources,app,db,Comment,Faculty,Event,Internship,Conference,Thesis
from flask import Flask, render_template, request, Response,send_file,send_from_directory,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from itertools import groupby




theses=[]
def thesis_journal_view():
    theses_from_db = Thesis.query.all()
    print(theses_from_db)
    return render_template('thesisjournal.html', theses=theses_from_db)




def homme_view():
    return render_template('index.html')

def home_view():
    return render_template('index.html')

def cinfo_view():
    return render_template('courseinfo.html')

def faculty_view():
    faculty = Faculty.query.all()
    return render_template('faculty.html', faculty=faculty)

def View_view():
    all_resource=Resources.query.all()
    return render_template('view.html',all_resource=all_resource)

def community_view():
    return render_template('community.html')

def Alumni_view():
    return render_template('Alumni.html')

def cse1_view():
    all_resource=Resources.query.filter(Resources.Course_Code.like('cse1%')).all()
    grouped_resources = {}
    
    # Group resources by course code
    all_resource.sort(key=lambda x: x.Course_Code)
    for course_code, resources in groupby(all_resource, key=lambda x: x.Course_Code):
        grouped_resources[course_code] = list(resources)
    
    return render_template('cse1.html', grouped_resources=grouped_resources)


def cse2_view():
    all_resource=Resources.query.filter(Resources.Course_Code.like('cse2%')).all()
    grouped_resources = {}
    
    # Group resources by course code
    all_resource.sort(key=lambda x: x.Course_Code)
    for course_code, resources in groupby(all_resource, key=lambda x: x.Course_Code):
        grouped_resources[course_code] = list(resources)
    
    return render_template('cse2.html', grouped_resources=grouped_resources)


def cse3_view():
    all_resource=Resources.query.filter(Resources.Course_Code.like('cse3%')).all()
    grouped_resources = {}
    
    # Group resources by course code
    all_resource.sort(key=lambda x: x.Course_Code)
    for course_code, resources in groupby(all_resource, key=lambda x: x.Course_Code):
        grouped_resources[course_code] = list(resources)
    
    return render_template('cse3.html', grouped_resources=grouped_resources)


def cse4_view():
    all_resource=Resources.query.filter(Resources.Course_Code.like('cse4%')).all()
    grouped_resources = {}
    
    # Group resources by course code
    all_resource.sort(key=lambda x: x.Course_Code)
    for course_code, resources in groupby(all_resource, key=lambda x: x.Course_Code):
        grouped_resources[course_code] = list(resources)
    
    return render_template('cse4.html', grouped_resources=grouped_resources)


def comment_view(course_codes, Serials, comments, ratings):
    return render_template('comment.html', course_data=zip(course_codes, Serials, comments, ratings))


def alumni_view(names, emails, c_names,c_types, dess):
    return render_template('alumni.html', alumnyy=zip(names, emails, c_names,c_types, dess))

def event_view():
    events_from_db = Event.query.all()
    return render_template('event.html', events=events_from_db)
def intern_view():
    interns_from_db = Internship.query.all()
    return render_template('intern.html', internn=interns_from_db)

def search_view(request):
    query = request.args.get('query', '')

    # Search in the 'Faculty' model
    faculty_results = Faculty.query.filter(Faculty.initial.ilike(f'%{query}%')).all()

    if faculty_results:
        return render_template('search2.html', data=faculty_results)

    # Search in the 'Resources' model
    course_list = Resources.query.filter(
        (Resources.Course_Code.ilike(f'%{query}%'))
        | (Resources.Description.ilike(f'%{query}%'))
    ).all()

    # Grouping the results by course
    grouped_results = {}
    for resource in course_list:
        if resource.Course_Code in grouped_results:
            grouped_results[resource.Course_Code].append(resource)
        else:
            grouped_results[resource.Course_Code] = [resource]

    return render_template('search.html', data=grouped_results)
