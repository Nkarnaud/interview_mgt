import json
import unittest
import datetime
from sqlalchemy.exc import IntegrityError
from project import db
from project.models.models import Interview, Interviewer, Candidates
from project.tests.base import BaseTestCase
from project.tests.utils import add_interview, add_interviewer, add_candidate, get_interviewer, get_candidate

class TestInterviewService(BaseTestCase):
    #test if interviewer is successfully add
    def test_add_interviewerapi(self):
        with self.client:
            response = self.client.post(
                '/interviewer/create',
                data=json.dumps({
                    'firstname': 'michael',
                    'lastname': 'greaterthaneight',
                    'email': 'arnaud@arnaud.org'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('Interviewer was added', data['message'])
            self.assertIn('success', data['status'])
    #test if we can not add interviewer with thesame email
    def test_add_interviewer_duplicate_email(self):
        add_interviewer("Irene", "Prinz", "prinz@chemondis.com")
        response = self.client.post(
                '/interviewer/create',
                data=json.dumps({
                    'firstname': 'michael',
                    'lastname': 'greaterthaneight',
                    'email': 'prinz@chemondis.com'
                }),
                content_type='application/json',
            )
        response = self.client.post(
                '/interviewer/create',
                data=json.dumps({
                    'firstname': 'testt',
                    'lastname': 'testt',
                    'email': 'prinz@chemondis.com'
                }),
                content_type='application/json',
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            'There exist an interviewer with this same email address.', data['message'])
        self.assertIn('fail', data['status']) 
    #Test create interviewer with empty json
    def test_create_interviewer_empty_json(self):
        with self.client:
            response = self.client.post('/interviewer/create', 
                data=json.dumps({
                }),
                content_type='application/json',
                ) 
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])
    #test if we can not add interviewer with wrong json input
    def test_add_interviewer_error_json_key(self):
        response = self.client.post(
                '/interviewer/create',
                data=json.dumps({
                    'firstname': 'testt',
                    'lastname': 'testt',
                }),
                content_type='application/json',
            ) 
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 500)

    #test get interviewer details
    def test_interviewer_details(self):
        interviewer = add_interviewer("Irene", "Prinz", "prinz@chemondis.com")
        with self.client:
            response = self.client.get(f'/interviewer/{interviewer.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn("Irene", data['data']['firstname'])
            self.assertIn("Prinz", data['data']['lastname'])
            self.assertIn("prinz@chemondis.com", data['data']['email'])
    
    #Test get  interviewer details with and un existing id 
    def test_interviewer_detail_invalid_id(self):
        Interviewer = add_interviewer("Irene", "Prinz", "prinz@chemondis.com")
        with self.client:
            response = self.client.get(f'/interviewer/9000')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('interviewers does not exists.', data['message'])
    #Test get interviewer list in the system 
    def test_interviewer_list(self):
        add_interviewer("Irene", "Prinz", "prinz@chemondis.com")
        add_interviewer("Test", "test", "test@chemondis.com")
        with self.client:
            response = self.client.get('/interviewer/lists')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['interviewers']), 2)
            self.assertIn('Irene', data['data']['interviewers'][0]['firstname'])
            self.assertIn('Prinz', data['data']['interviewers'][0]['lastname'])
            self.assertIn('prinz@chemondis.com', data['data']['interviewers'][0]['email'])
            self.assertIn('Test', data['data']['interviewers'][1]['firstname'])
            self.assertIn('test', data['data']['interviewers'][1]['lastname'])
            self.assertIn('test@chemondis.com', data['data']['interviewers'][1]['email'])
            self.assertIn('success', data['status'])
    #Test data update interviewer
    def test_interviewer_update(self):
        add_interviewer("Irene", "Pri<nz", "prinz@chemondis.com")
        interviewer = get_interviewer("prinz@chemondis.com")
        with self.client:
            response = self.client.put(f'/interviewer/update/{interviewer.id}', 
            data=json.dumps({
                'firstname': 'testt',
                'lastname': 'testt',
                'email': 'prinz@chemondis.com',
            }),
            content_type='application/json',
            ) 
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('The interviewer has been update', data['message'])
            self.assertIn('Modified', data['status'])
    #Test update data with empty post data
    def test_interviewer_update_with_empty_json(self):
        add_interviewer("Irene", "Pri<nz", "prinz@chemondis.com")
        interviewer = get_interviewer("prinz@chemondis.com")
        with self.client:
            response = self.client.put(f'/interviewer/update/{interviewer.id}', 
            data=json.dumps({
            }),
            content_type='application/json',
            ) 
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Sorry. The interviewer does not exists', data['message'])
            self.assertIn('fail', data['status'])
    #Test update of interviewer that does not exist
    def test_update_interviewer_not_exist(self):
        with self.client:
            response = self.client.put('/interviewer/update/99', 
            data=json.dumps({
                'firstname': 'testt',
                'lastname': 'testt',
                'email': 'prinz@chemondis.com',
            }),
            content_type='application/json',
            ) 
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Interviewer not found', data['message'])
            self.assertIn('fail', data['status'])
    #Test interviewer delete 
    def test_interviewer_delete(self):
        add_interviewer("Irene", "Pri<nz", "prinz@chemondis.com")
        interviewer = get_interviewer("prinz@chemondis.com")
        with self.client:
            response = self.client.delete(f'/interviewer/delete/{interviewer.id}',)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('The interviewer has been deleted', data['message'])
            self.assertIn('deleted', data['status'])
    #Test delete and un existing data
    def test_delete_not_exist_interviewer(self):
        add_interviewer("Irene", "Pri<nz", "prinz@chemondis.com")
        with self.client:
            response = self.client.delete('/interviewer/delete/1000',)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Sorry. The interviewer does not exists', data['message'])
            self.assertIn('fail', data['status'])
    #Testing for candidate creation
    def test_add_candidate(self):
        with self.client:
            response = self.client.post(
                '/candidate/create',
                data=json.dumps({
                    'firstname': 'michael',
                    'lastname': 'greaterthaneight',
                    'email': 'arnaud@arnaud.org'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('A new candidate added', data['message'])
            self.assertIn('success', data['status'])
    #test if we can not add candidate with thesame email
    def test_add_candidate_duplicate_email(self):
        with self.client:
            response = self.client.post(
                    '/candidate/create',
                    data=json.dumps({
                        'firstname': 'michael',
                        'lastname': 'greaterthaneight',
                        'email': 'arnaud@chemondis.com'
                    }),
                    content_type='application/json',
                )
            response = self.client.post(
                    '/candidate/create',
                    data=json.dumps({
                        'firstname': 'testt',
                        'lastname': 'testt',
                        'email': 'arnaud@chemondis.com'
                    }),
                    content_type='application/json',
                )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('This candidate already exit.', data['message'])
            self.assertIn('fail', data['status']) 
    #Test create candidate with empty json
    def test_create_candidate_empty_json(self):
        with self.client:
            response = self.client.post('/candidate/create', 
                data=json.dumps({
                }),
                content_type='application/json',
                ) 
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])
    #test if we can not add candidate with wrong json input
    def test_add_candidate_error_json_key(self):
        response = self.client.post(
                '/candidate/create',
                data=json.dumps({
                    'firstname': 'testt',
                    'lastname': 'testt',
                }),
                content_type='application/json',
            ) 
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 500)

    #test get candidate details
    def test_candidate_details(self):
        candidate = add_candidate("Arnaud", "Tsombeng", "arnaud.tsombeng@chemondis.com")
        with self.client:
            response = self.client.get(f'/candidate/{candidate.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn("Arnaud", data['data']['firstname'])
            self.assertIn("Tsombeng", data['data']['lastname'])
            self.assertIn("arnaud.tsombeng@chemondis.com", data['data']['email'])
            self.assertIn('success', data['status'])
    
    #Test get  candidate details with and un existing id 
    def test_candidate_detail_invalid_id(self):
        candidate = add_candidate("Arnaud", "Tsombeng", "arnaud.tsombeng@chemondis.com")
        with self.client:
            response = self.client.get(f'/candidate/9000')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('candidate does not exist.', data['message'])
    #Test get candidate list in the system 
    def test_candidate_list(self):
        add_candidate("test25", "test462", "testrfd@chemondis.com")
        add_candidate("Test", "test", "test@chemondis.com")
        with self.client:
            response = self.client.get('/candidate/lists')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['candidates']), 2)
            self.assertIn('test25', data['data']['candidates'][0]['firstname'])
            self.assertIn('test462', data['data']['candidates'][0]['lastname'])
            self.assertIn('testrfd@chemondis.com', data['data']['candidates'][0]['email'])
            self.assertIn('Test', data['data']['candidates'][1]['firstname'])
            self.assertIn('test', data['data']['candidates'][1]['lastname'])
            self.assertIn('test@chemondis.com', data['data']['candidates'][1]['email'])
            self.assertIn('success', data['status'])
    #Test data update candidate
    def test_candidate_update(self):
        candidate = add_candidate("test25", "test462", "test@chemondis.com")
        with self.client:
            response = self.client.put(f'/candidate/update/{candidate.id}', 
                data=json.dumps({
                    'firstname': 'testt2',
                    'lastname': 'testt4654',
                    'email': 'prinz@chemondis.com',
                }),
                content_type='application/json',
                ) 
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('The candidate has been update', data['message'])
            self.assertIn('Modified', data['status'])
    #Test update candidate with empty post data
    def test_candidate_update_with_empty_json(self):
        add_candidate("Irene", "Pri<nz", "prinz@chemondis.com")
        candidate = get_candidate("prinz@chemondis.com")
        with self.client:
            response = self.client.put(f'/candidate/update/{candidate.id}', 
            data=json.dumps({
            }),
            content_type='application/json',
            ) 
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Sorry. The candidate does not exist', data['message'])
            self.assertIn('fail', data['status'])
    #Test update of candidate that does not exist
    def test_update_candidate_not_exist(self):
        with self.client:
            response = self.client.put('/candidate/update/99', 
            data=json.dumps({
                'firstname': 'testt',
                'lastname': 'testt',
                'email': 'prinz@chemondis.com',
            }),
            content_type='application/json',
            ) 
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Candidate not found', data['message'])
            self.assertIn('fail', data['status'])
    #Test candidate delete 
    def test_candidate_delete(self):
        add_candidate("Irene", "Pri<nz", "prinz@chemondis.com")
        candidate = get_candidate("prinz@chemondis.com")
        with self.client:
            response = self.client.delete(f'/candidate/delete/{candidate.id}',)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('The candidate has been deleted', data['message'])
            self.assertIn('deleted', data['status'])
    #Test delete and un existing data
    def test_delete_not_exist_candidate(self):
        add_candidate("Irene", "Pri<nz", "prinz@chemondis.com")
        with self.client:
            response = self.client.delete('/candidate/delete/1000',)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Sorry. The candidate does not exists', data['message'])
            self.assertIn('fail', data['status'])
    #create interview slot
    def test_create_interview(self):
        with self.client:
            response = self.client.post(
                '/interview/create',
                data=json.dumps({
                    'title': 'Backend dev interview',
                    'start_time': '02-09-2019:09:00',
                    'end_time': '02-09-2019:10:00'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('A new interview slot added.', data['message'])
            self.assertIn('success', data['status'])
    #Test if the creation of duplicate interview is not possible
    def test_creation_of_duplicate_interview(self):
        interview = add_interview("Backend dev interview", "02-09-2019:09:00", "02-09-2019:10:00")
        with self.client:
            response = self.client.post(
                '/interview/create',
                data=json.dumps({
                    'title': 'Backend dev interview',
                    'start_time': '02-09-2019:09:00',
                    'end_time': '02-09-2019:10:00'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('This interview slot already exit.', data['message'])
            self.assertIn('fail', data['status'])
    #Test get interview detail
    def test_get_interview_detail(self):
        interview = add_interview("Backend dev interview", "02-09-2019:09:00", "02-09-2019:10:00")
        with self.client:
            response = self.client.get(f'/interview/{interview.id}')
            data = json.loads(response.data.decode())
            self.assertIn('Backend dev interview', data['data']['title'])
            self.assertIn('Sat, 09 Feb 2019 09:00:00 GMT', data['data']['start_time'])
            self.assertIn('Sat, 09 Feb 2019 10:00:00 GMT', data['data']['end_time'])
            self.assertIn('success', data['status'])
    #Test get interview detail with wrong id
    def test_get_interview_detail_id_error(self):
        with self.client:
            response = self.client.get('/interview/100')
            data = json.loads(response.data.decode())
            self.assertEqual('Interview does not exist.', data['message'])
            self.assertIn('fail', data['status'])
    #Test get interview list 
    def test_get_interview_list(self):
        interview = add_interview("Backend dev interview", "02-09-2019:09:00", "02-09-2019:10:00")
        interview = add_interview("Frontend dev interview", "02-09-2019:09:00", "02-09-2019:10:00")
        with self.client:
            response = self.client.get('/interview_list')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['interviews']), 2)
            self.assertIn('Backend dev interview', data['data']['interviews'][0]['title'])
            self.assertIn('Sat, 09 Feb 2019 09:00:00 GMT', data['data']['interviews'][0]['start_time'])
            self.assertIn('Sat, 09 Feb 2019 10:00:00 GMT', data['data']['interviews'][0]['end_time'])
            self.assertIn('Frontend dev interview', data['data']['interviews'][1]['title'])
            self.assertIn('Sat, 09 Feb 2019 09:00:00 GMT', data['data']['interviews'][1]['start_time'])
            self.assertIn('Sat, 09 Feb 2019 10:00:00 GMT', data['data']['interviews'][1]['end_time'])
            self.assertIn('success', data['status'])
    #test delete interview
    def test_delete_interview(self):
        interview = add_interview("Backend dev interview", "02-09-2019:09:00", "02-09-2019:10:00")
        with self.client:
            response = self.client.delete(f'/interview/delete/{interview.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('The interview has been deleted', data['message'])
            self.assertIn('deleted', data['status'])
    #Test delete a user that does not exist in the system
    def test_delete_interview_wrong_id(self):
        with self.client:
            response = self.client.delete('/interview/delete/1000')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Sorry. The interview does not exists', data['message'])
            self.assertIn('fail', data['status'])
    def test_get_interview_emptyslot(self):
        with self.client:
            response = self.client.get('/interview_emptyslot')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
    #Test assigne candidate to and interview
    def test_candidate_assigned_interview(self):
        interview = add_interview("Backend dev interview", "02-09-2019:09:00", "02-09-2019:10:00")
        candidate = add_candidate("test25", "test462", "test@chemondis.com")
        with self.client:
            response = self.client.post(f'/candidate_assign/{candidate.id}/{interview.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('This candidate hase been assigned to the interview.', data['message'])
            self.assertIn('Success', data['status'])
    #Test that a candidate can not be assign to thesame interview twice
    def test_thesame_candidate_assigned_thesame_interview(self):
        interview = add_interview("Backend dev interview", "02-09-2019:09:00", "02-09-2019:10:00")
        candidate = add_candidate("test25", "test462", "test@chemondis.com")
        with self.client:
            response = self.client.post(f'/candidate_assign/{candidate.id}/{interview.id}')
            response = self.client.post(f'/candidate_assign/{candidate.id}/{interview.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('This candidate is already assigned to this interview', data['message'])
            self.assertIn('fail', data['status'])
    #Test if Each interview consist of exactly one candidate
    def test_candidate_assigned_interview_with_candidate(self):
        interview = add_interview("Backend dev interview", "02-09-2019:09:00", "02-09-2019:10:00")
        candidate = add_candidate("test25", "test462", "test@chemondis.com")
        candidate1 = add_candidate("arnaud", "Tsomben", "arnaud@chemondis.com")
        with self.client:
            response = self.client.post(f'/candidate_assign/{candidate.id}/{interview.id}')
            response = self.client.post(f'/candidate_assign/{candidate1.id}/{interview.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('This Interview already have a candidate assigned to', data['message'])
            self.assertIn('fail', data['status'])
    #Test interviewer assigne to interview
    def test_interviewer_assign_to_interview(self):
        interview = add_interview("Backend dev interview", "02-09-2019:09:00", "02-09-2019:10:00")
        interviewer = add_interviewer("Irene", "Pri<nz", "prinz@chemondis.com")
        with self.client:
            response = self.client.post(f'/interviewer_assign/{interviewer.id}/{interview.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('This interviewer has been assigned to the interview.', data['message'])
            self.assertIn('Success', data['status'])
    #Test interviewer assigne to  many interview
    def test_interviewer_assign_to_many_interview(self):
        interview = add_interview("Backend dev interview", "02-09-2019:09:00", "02-09-2019:10:00")
        interview1 = add_interview("Frontend dev interview", "02-09-2019:09:00", "02-09-2019:10:00")
        interviewer = add_interviewer("Irene", "Pri<nz", "prinz@chemondis.com")
        with self.client:
            response = self.client.post(f'/interviewer_assign/{interviewer.id}/{interview.id}')
            response = self.client.post(f'/interviewer_assign/{interviewer.id}/{interview1.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('This interviewer has been assigned to the interview.', data['message'])
            self.assertIn('Success', data['status'])
    #Test assigne interviewer to thesame intervier
    def test_interviewer_assign_to_thesame_interview(self):
        interview = add_interview("Backend dev interview", "02-09-2019:09:00", "02-09-2019:10:00")
        interviewer = add_interviewer("Irene", "Pri<nz", "prinz@chemondis.com")
        with self.client:
            response = self.client.post(f'/interviewer_assign/{interviewer.id}/{interview.id}')
            response = self.client.post(f'/interviewer_assign/{interviewer.id}/{interview.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('This interviewer is already assigned to this interview.', data['message'])
            self.assertIn('Fail', data['status'])
    #Test get the list of interview of an interviewer
    def test_interviewers_interview_list(self):
        interview = add_interview("Backend dev interview", "02-09-2019:09:00", "02-09-2019:10:00")
        interview1 = add_interview("Frontend dev interview", "02-09-2019:09:00", "02-09-2019:10:00")
        interviewer = add_interviewer("Irene", "Pri<nz", "prinz@chemondis.com")
        with self.client:
            response = self.client.post(f'/interviewer_assign/{interviewer.id}/{interview.id}')
            response = self.client.post(f'/interviewer_assign/{interviewer.id}/{interview1.id}')
            response = self.client.get(f'/interview/interviewer/list/{interviewer.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['interviews']), 2)
            self.assertIn('Backend dev interview', data['data']['interviews'][0]['title'])
            self.assertIn('Sat, 09 Feb 2019 09:00:00 GMT', data['data']['interviews'][0]['start_time'])
            self.assertIn('Sat, 09 Feb 2019 10:00:00 GMT', data['data']['interviews'][0]['end_time'])
            self.assertIn('Frontend dev interview', data['data']['interviews'][1]['title'])
            self.assertIn('Sat, 09 Feb 2019 09:00:00 GMT', data['data']['interviews'][1]['start_time'])
            self.assertIn('Sat, 09 Feb 2019 10:00:00 GMT', data['data']['interviews'][1]['end_time'])
            self.assertIn('success', data['status'])
    #test get candidate interview detail
    def test_get_candidate_interview_detail(self):
        interview = add_interview("Backend dev interview", "02-09-2019:09:00", "02-09-2019:10:00")
        candidate = add_candidate("test25", "test462", "test@chemondis.com")
        with self.client:
            response = self.client.post(f'/candidate_assign/{candidate.id}/{interview.id}')
            response = self.client.get(f'/interview/candidate/{candidate.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['interview']), 1)
            self.assertIn('Backend dev interview', data['data']['interview'][0]['title'])
            self.assertIn('Sat, 09 Feb 2019 09:00:00 GMT', data['data']['interview'][0]['start_time'])
            self.assertIn('Sat, 09 Feb 2019 10:00:00 GMT', data['data']['interview'][0]['end_time'])
            self.assertIn('success', data['status'])
