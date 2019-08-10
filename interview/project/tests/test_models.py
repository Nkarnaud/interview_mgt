import unittest
from sqlalchemy.exc import IntegrityError, DataError
import datetime
from project import db
from project.models.models import Interview, Interviewer, Candidates
from project.tests.base import BaseTestCase
from project.tests.utils import add_interview, add_interviewer, add_candidate

class TestInterviewModel(BaseTestCase):

    def test_add_interview(self):
        interview = add_interview("Backend dev interview", "02-09-2019:09:00", "02-09-2019:10:00")
        self.assertTrue(interview.id)
        self.assertEqual(interview.title,"Backend dev interview")
        self.assertEqual(interview.start_time, datetime.datetime.strptime("2019-02-09 09:00:00",'%Y-%m-%d %H:%M:%S'))
        self.assertEqual(interview.end_time, datetime.datetime.strptime("2019-02-09 10:00:00", '%Y-%m-%d %H:%M:%S'))

    def test_add_interviewer(self):
        interviewer = add_interviewer("Irene", "Prinz", "irene.prinz@chemondis.com")
        self.assertTrue(interviewer.id)
        self.assertEqual(interviewer.firstname,"Irene")
        self.assertEqual(interviewer.lastname, "Prinz")
        self.assertEqual(interviewer.email, "irene.prinz@chemondis.com")
    
    def test_add_interviewer_duplicate_email(self):
        add_interviewer("Irene", "Prinz", "irene.prinz@chemondis.com")
        duplicate_interviewer = Interviewer(
            firstname = "chemondis",
            lastname = "test",
            email = "irene.prinz@chemondis.com"
        )
        db.session.add(duplicate_interviewer)
        self.assertRaises(IntegrityError, db.session.commit)
    
    def test_add_candidate(self):
        candidate = add_candidate("Arnaud", "Tsombeng", "arnaud.tsombeng@chemondis.com")
        self.assertTrue(candidate.id)
        self.assertEqual(candidate.firstname,"Arnaud")
        self.assertEqual(candidate.lastname, "Tsombeng")
        self.assertEqual(candidate.email, "arnaud.tsombeng@chemondis.com")
    
    def test_add_candidate_duplicate_email(self):
        add_candidate("Arnaud", "Tsombeng", "arnaud.tsombeng@chemondis.com")
        duplicate_candidate = Candidates(
            firstname = "Test",
            lastname = "test2",
            email = "arnaud.tsombeng@chemondis.com"
        )
        db.session.add(duplicate_candidate)
        self.assertRaises(IntegrityError, db.session.commit)

if __name__ == '__main__':
     unittest.main()
