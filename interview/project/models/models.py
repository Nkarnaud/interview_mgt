# -*- coding: utf-8 -*-
import datetime
from project import db

#Interviewer model
class Interviewer(db.Model):
    __tablename__ = "interviewer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(32), nullable=False)
    lastname = db.Column(db.String(32), nullable=True)
    email = db.Column(db.String(128), nullable=False, unique = True)
    interview = db.relationship('Interview', secondary="interviewer_assigned")
    
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
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), unique=True)
    candidate=db.relationship("Candidates", backref=db.backref("Interview", uselist=False))
    interviewer=db.relationship("Interviewer", secondary = "interviewer_assigned", cascade="all")

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

#assiciation table
class Interviewer_assigned(db.Model):
    __tablename__="interviewer_assigned"
    id = db.Column(db.Integer, primary_key=True)
    interviewer_id= db.Column( db.Integer, db.ForeignKey('interviewer.id'))
    interview_id= db.Column(db.Integer, db.ForeignKey('interview.id'))
    interview = db.relationship("Interview", backref=db.backref("interviewer_assigned", cascade="all") )
    interviewer = db.relationship("Interviewer", backref=db.backref("interviewer_assigned", cascade="all") )

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
