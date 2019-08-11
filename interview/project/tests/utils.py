from project import db
from project.models.models import Interview, Interviewer, Candidates


# Adding Interviews into the system
def add_interview(title, start_time, end_time):
    interview = Interview(title=title,
                          start_time=start_time, end_time=end_time)
    db.session.add(interview)
    db.session.commit()
    return interview


# Adding interviewers into the system
def add_interviewer(firstname, lastname, email):
    interviewer = Interviewer(firstname=firstname,
                              lastname=lastname, email=email)
    db.session.add(interviewer)
    db.session.commit()
    return interviewer


# Adding Candidate in to the system for test
def add_candidate(firstname, lastname, email):
    candidate = Candidates(firstname=firstname,
                           lastname=lastname, email=email)
    db.session.add(candidate)
    db.session.commit()
    return candidate


# Get interviewer from database
def get_interviewer(email):
    interviewer = Interviewer.query.filter_by(email=email).first()
    return interviewer


# Get candidate from de database
def get_candidate(email):
    candidate = Candidates.query.filter_by(email=email).first()
    return candidate
