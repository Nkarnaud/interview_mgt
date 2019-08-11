# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request
from project.models.models import Interview, Interviewer
from project.models.models import Candidates, Interviewer_assigned
from project import db


# defining end point blueprint
interview_blueprint = Blueprint('interview', __name__)


# Test if the services is acessible
@interview_blueprint.route('/interview/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


# Create interviewer
@interview_blueprint.route('/interviewer/create', methods=['POST'])
def create_interviewer():
    """This endpoint will permit the creation of interviewer.
    Input: firstname, lastname, email
    Output: success if the interviewer is created or fail if not
    """
    # get post data
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_object), 400
    firstname = post_data.get('firstname')
    lastname = post_data.get('lastname')
    email = post_data.get('email')
    try:
        # check if interviewers exist in the system
        interviewer = Interviewer.query.filter_by(email=email).first()
        if not interviewer:
            new_interviewer = Interviewer(
                firstname=firstname,
                lastname=lastname,
                email=email
            )
            db.session.add(new_interviewer)
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = 'Interviewer was added.'
            return jsonify(response_object), 201
        else:
            response_object['message'] =\
                'There exist an interviewer with this same email address.'
            return jsonify(response_object), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


# Get interviewer details
@interview_blueprint.route('/interviewer/<id>', methods=['GET'])
def interviewer_detaile(id):
    """Get interviewer details given it id
        Input: interviewer ID
        Output: interview details if successful and fail if not
    """
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    interviewer = Interviewer.query.filter_by(id=int(id)).first()
    try:
        if interviewer:
            response_object = {
                'status': 'success',
                'data': {
                    'id': interviewer.id,
                    'firstname': interviewer.firstname,
                    'lastname': interviewer.lastname,
                    'email': interviewer.email
                }
            }
            return jsonify(response_object), 200
        else:
            response_object = {
                'status': 'fail',
                'message': 'interviewers does not exists.'}
            return jsonify(response_object), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500


# This function provide the list of all favorite in the system
@interview_blueprint.route('/interviewer/lists', methods=['GET'])
def get_all_interviewer():
    """ Return the list of interviewer in the system.
        No input
        output the list of interviewer if successfull or fail if not
    """
    try:
        response_object = {
            'status': 'success',
            'data': {
                'interviewers': [interviewer.to_json()
                                 for interviewer in Interviewer.query.all()]
            }
        }
        return jsonify(response_object), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500


# Update interviewer
@interview_blueprint.route('/interviewer/update/<id>', methods=['PUT'])
def update_interviewer(id):
    """To update a interviewer in the systeme.
        Input: interviwer id
        output: updated interviewer if successfull and fail if not
    """
    response_object = {
        'status': 'fail',
        'message': 'Sorry. The interviewer does not exists'
    }
    post_data = request.get_json()
    if not post_data:
        return jsonify(response_object), 400
    firstname = post_data.get('firstname')
    lastname = post_data.get('lastname')
    email = post_data.get('email')
    try:
        interviewer = Interviewer.query.get(id)
        if not interviewer:
            response_object['message'] = 'Interviewer not found'
            return jsonify(response_object), 404
        else:
            interviewer.firstname = firstname
            interviewer.lastname = lastname
            interviewer.email = email
            db.session.commit()
            response_object = {
                'status': 'Modified',
                'message': 'The interviewer has been update'
                }
            return jsonify(response_object), 201
    except Exception as e:
        db.session.rollback()
        response_object['message'] = 'Interviewer not found'
        return jsonify(response_object), 404


# To delete interviewer
@interview_blueprint.route('/interviewer/delete/<id>', methods=['DELETE'])
def delete_interviewer(id):
    """ Delete and interviewer in the system.
        Input: interviewer id
        output: success message or fail message
    """
    response_object = {
        'status': 'fail',
        'message': 'Sorry. The interviewer does not exists'
    }
    try:
        interviewer = Interviewer.query.get(int(id))
        if interviewer:
            db.session.delete(interviewer)
            db.session.commit()
            response_object = {
                'status': 'deleted',
                'message': 'The interviewer has been deleted'
                }
            return jsonify(response_object), 200
        else:
            return jsonify(response_object), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


# create candidate
@interview_blueprint.route('/candidate/create', methods=['POST'])
def create_candidate():
    """This endpoint will permit the creation of candidate.
    Input: firstname, lastname, email
    Output: success if the candidate is created or fail if not
    """
    # get post data
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_object), 400
    firstname = post_data.get('firstname')
    lastname = post_data.get('lastname')
    email = post_data.get('email')
    try:
        # fetch the candidate
        candidate = Candidates.query.filter_by(
            email=post_data.get('email')).first()
        if not candidate:
            new_candidate = Candidates(
                firstname=firstname,
                lastname=lastname,
                email=email
            )
            db.session.add(new_candidate)
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = 'A new candidate added.'
            return jsonify(response_object), 201
        else:
            response_object['message'] = 'This candidate already exit.'
            return jsonify(response_object), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


# Get candidate details
@interview_blueprint.route('/candidate/<id>', methods=['GET'])
def candidate_detail(id):
    """Get Candidate details given it id
        Input: candidate ID
        Output: candidate details if successful and fail if not
    """
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }

    try:
        candidate = Candidates.query.filter_by(id=int(id)).first()
        if candidate:
            response_object = {
                'status': 'success',
                'data': {
                    'id': candidate.id,
                    'firstname': candidate.firstname,
                    'lastname': candidate.lastname,
                    'email': candidate.email
                }
            }
            return jsonify(response_object), 200
        else:
            response_object = {
                'status': 'fail',
                'message': 'candidate does not exist.'}
            return jsonify(response_object), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500


# Return the list of interviewer in the system
@interview_blueprint.route('/candidate/lists', methods=['GET'])
def get_all_candidate():
    """ Return the list of interviewer in the system.
        No input
        output the list of interviewer if successfull or fail if not
    """
    # This function provide the list of all candidate in the system
    try:
        response_object = {
            'status': 'success',
            'data': {
                'candidates': [candidate.to_json()
                               for candidate in Candidates.query.all()]
            }
        }
        return jsonify(response_object), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


# To update a candidate in the systeme
@interview_blueprint.route('/candidate/update/<id>', methods=['PUT'])
def update_candidate(id):
    """To update a candidate in the systeme.
    Input: candidate id
    output: updated candidate if successfull and fail if not
    """
    response_object = {
        'status': 'fail',
        'message': 'Sorry. The candidate does not exist'
    }
    post_data = request.get_json()
    if not post_data:
        return jsonify(response_object), 400
    firstname = post_data.get('firstname')
    lastname = post_data.get('lastname')
    email = post_data.get('email')
    try:
        candidate = Candidates.query.get(int(id))
        if not candidate:
            response_object['message'] = 'Candidate not found'
            return jsonify(response_object), 404
        else:
            candidate.firstname = firstname
            candidate.lastname = lastname
            candidate.email = email
            db.session.commit()
            response_object = {
                'status': 'Modified',
                'message': 'The candidate has been update'
                }
            return jsonify(response_object), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500


# To delete a candidate
@interview_blueprint.route('/candidate/delete/<id>', methods=['DELETE'])
def delete_candidate(id):
    """ Delete and candidate in the system.
        Input: candidate id
        output: success message or fail message
    """
    response_object = {
        'status': 'fail',
        'message': 'Sorry. The candidate does not exists'
    }
    try:
        candidate = Candidates.query.get(int(id))
        if candidate:
            db.session.delete(candidate)
            db.session.commit()
            response_object = {
                'status': 'deleted',
                'message': 'The candidate has been deleted'
                }
            return jsonify(response_object), 200
        else:
            return jsonify(response_object), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


# create interview slot
@interview_blueprint.route('/interview/create', methods=['POST'])
def create_interview():
    """ This end point is used to create and interview slot.
        input: title, start time, end time
        Output: success message if interview slot create or fail if not
    """
    # get post data
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_object), 400
    title = post_data.get('title')
    start_time = post_data.get('start_time')
    end_time = post_data.get('end_time')
    try:
        # fetch the interview
        interview = Interview.query.filter_by(
            title=title, start_time=start_time, end_time=end_time).first()
        if not interview:
            new_interview = Interview(
                title=title,
                start_time=start_time,
                end_time=end_time
            )
            db.session.add(new_interview)
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = 'A new interview slot added.'
            return jsonify(response_object), 201
        else:
            response_object['message'] = 'This interview slot already exit.'
            return jsonify(response_object), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


# Get interview details given it id
@interview_blueprint.route('/interview/<id>', methods=['GET'])
def get_interview(id):
    """Get interview details given it id
        Input: interview ID
        Output: interview details if successful or fail if not
    """
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    inteview = Interview.query.filter_by(id=int(id)).first()
    try:
        if inteview:
            response_object = {
                'status': 'success',
                'data': {
                    'title': inteview.title,
                    'start_time': inteview.start_time,
                    'end_time': inteview.end_time
                }
            }
            return jsonify(response_object), 200
        else:
            response_object = {
                'status': 'fail',
                'message': 'Interview does not exist.'}
            return jsonify(response_object), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500


# Return the list of all interview
@interview_blueprint.route('/interview_list', methods=['GET'])
def get_interview_list():
    """ Return list of all interviews in the system.
        input : no input
        output: list of all interviews in the system.
    """
    response_object = {
        'status': 'success',
        'data': {
            'interviews': [interview.to_json()
                           for interview in Interview.query.all()]
        }
    }
    return jsonify(response_object), 200


# To delete a interview
@interview_blueprint.route('/interview/delete/<id>', methods=['DELETE'])
def delete_interview(id):
    """ Delete an interview in the system
        input: interview id
        output: success or fail"""
    response_object = {
        'status': 'fail',
        'message': 'Sorry. The interview does not exists'
    }
    try:
        interview = Interview.query.get(int(id))
        if interview:
            db.session.delete(interview)
            db.session.commit()
            response_object = {
                'status': 'deleted',
                'message': 'The interview has been deleted'
                }
            return jsonify(response_object), 200
        else:
            return jsonify(response_object), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


# Get interview empyty slot
@interview_blueprint.route('/interview_emptyslot', methods=['GET'])
def interview_emptyslot():
    """Get interview empyty slot
        Input: no in put
        output: list of empty interview slot
    """
    response_object = {
            'status': 'success',
            'data': {
                'interview_empty_slot': [
                    interview.to_json() for interview in
                    Interview.query.filter
                    (Interview.candidate_id == None).all()]
            }
        }
    return jsonify(response_object), 200


# Assign a one customer to one and only one interview
@interview_blueprint.route(
    '/candidate_assign/<candidate_id>/<interview_id>', methods=['POST'])
def candidate_assigned_interview(candidate_id, interview_id):
    """ Assign a candidates to an interview
        This end point takes in a candidate id and interview id and assign
        the candidate to that interview slot if the slot is empty.
        The output is the interview with the assigne candidate
        """
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload'
    }
    try:
        candidate = Candidates.query.get(int(candidate_id))
        interview = Interview.query.get(int(interview_id))
        if interview.candidate_id == int(candidate_id):
            response_object['message'] =\
                'This candidate is already assigned to interview.'
            return jsonify(response_object), 400
        elif interview.candidate_id:
            response_object['message'] =\
                'This Interview already have a candidate assigned.'
            return jsonify(response_object), 400
        else:
            interview.candidates = candidate
            interview.candidate_id = candidate.id
            db.session.commit()
            response_object['status'] = 'Success'
            response_object['message'] =\
                'This candidate hase been assigned to interview.'
            return jsonify(response_object), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500


# Assigning an interviewer to and interview slot
@interview_blueprint.route(
    '/interviewer_assign/<interviewer_id>/<interview_id>', methods=['POST'])
def interviewer_assign_to_interview(interviewer_id, interview_id):
    """
        Assigning an interviewer to and interview slot.
        And interviewer can be assign to many interviewer
        Input:{interviewer id, interview id}
        Output: { }
    """
    response_object = {
        'status': 'Fail.',
        'message': 'Invalid Payload'
    }
    try:
        interviewer = Interviewer.query.get(int(interviewer_id))
        interview = Interview.query.get(int(interview_id))
        if interview in interviewer.interview:
            response_object['message'] =\
                'This interviewer is already assigned to interview.'
            return jsonify(response_object), 400
        else:
            interviewer.interview.append(interview)
            db.session.commit()
            response_object['status'] = 'Success'
            response_object['message'] =\
                'This interviewer has been assigned to interview.'
            return jsonify(response_object), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500


# Return the list of interview of an interviewer
@interview_blueprint.route(
    '/interview/interviewer/list/<interviewer_id>', methods=['GET'])
def interviewers_interview(interviewer_id):
    """ Return the list of interviewers interview
        input: candidate id
        output:  interview details
    """
    try:
        response_object = {
            'status': 'success.',
            'data': {
                'interviews': [interview.to_json() for
                               interview in Interview.query.join
                               (Interviewer_assigned).filter_by
                               (interviewer_id=int(interviewer_id))]
            }
        }
        return jsonify(response_object), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500


# Return the candidate interview details
@interview_blueprint.route(
    '/interview/candidate/<candidates_id>', methods=['GET'])
def candidate_interview(candidates_id):
    """ Return the candidate interview details
        input: interviewer id
        output: list of interviews
    """
    try:
        response_object = {
            'status': 'success.',
            'data': {
                'interview': [interview.to_json() for
                              interview in Interview.query.filter_by
                              (candidate_id=candidates_id).all()]
                }
        }
        return jsonify(response_object), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500
