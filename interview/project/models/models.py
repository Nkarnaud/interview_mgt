# -*- coding: utf-8 -*-
import datetime
from flask import current_app
from project import db
#association table
interviewer_assigned= db.Table('associate_table',
    db.Column('interviewer_id', db.Integer, db.ForeignKey('interviewer.id'), primary_key=True),
    db.Column('interview_id', db.Integer, db.ForeignKey('interview.id'), primary_key=True)
)
#Interviewer model
class Interviewer(db.Model):
    __tablename__ = "interviewer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(32), nullable=False)
    lastname = db.Column(db.String(32), nullable=True)
    email = db.Column(db.String(128), nullable=False, unique = True)
     = db.relationship('Category', foreign_keys=categorie_id)
    
    #Class constructor 
    def __init__(self, firstname, lastname, email):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
    
    # Returning class attribute in a json format
    def to_json(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email
        }

#Interview table
class Interview(db.Model):
    __tablename__ = "interview"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(32))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'), unique=True)
    candidate=relationship("Candidate", back_populates="interview", uselist=False)

    #Class constuctor
    def __init__(self, title, start_time, end_time):
        self.title = title
        self.start_time = start_time
        self.end_time = end_time
    
    #Returning class attribute in json format
    def to_json(self):
        return{
            "id": self.id,
            "title": self.title,
            "start_time": self.start_time,
            "end_time": self.end_time
        }

#Candidate table
class Candidates(db.Model):
    __tablename__ = "candidates"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(32), nullable=False)
    lastname = db.Column(db.String(32), nullable=True)
    email = db.Column(db.String(128), nullable=False, unique = True)

    #Class constructor 
    def __init__(self, firstname, lastname, email):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
    
    # Returning class attribute in a json format
    def to_json(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email
        }
