# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request
from project.models.models import Interview, Interviewer, Candidates, Interviewer_assigned
from project import db
from sqlalchemy import not_

#defining end point blueprint
interview_blueprint = Blueprint('interview', __name__)

#Test if the services is acessible
@interview_blueprint.route('/interview/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })

@interview_blueprint.route('/interviewer/create', methods=['POST'])
def create_interviewer():
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
        #check if interviewers exist in the system 
        interviewer = Interviewer.query.filter_by(email=email).first()
        if not interviewer:
            new_interviewer=Interviewer(
                firstname = firstname,
                lastname = lastname,
                email = email
            )
            db.session.add(new_interviewer)
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = 'Interviewer was added.'
            return jsonify(response_object), 201
        else:
            response_object['message'] = 'There exist an interviewer with this same email address.'
            return jsonify(response_object), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500

#Get interviewer details
@interview_blueprint.route('/interviewer/<id>', methods=['GET'])
def interviewer_detaile(id):
    """Get interviewer details giving it id"""
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
            response_object ={
                'status' : 'fail',
                'message': 'interviewers does not exists.'}
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

@interview_blueprint.route('/interviewer/lists', methods=['GET'])
def get_all_interviewer():
    # This function provide the list of all favorite in the system
        response_object = {
            'status': 'success',
            'data': {
                'users': [interviewer.to_json() for interviewer in Interviewer.query.all()]
            }
        }
        return jsonify(response_object), 200

@interview_blueprint.route('/interviewer/update/<id>', methods=['PUT'])
def update_interviewer(id):
    """To update a interviewer in the systeme"""
    response_object = {
        'status': 'fail',
        'message': 'Sorry. The interviewer does not exists'
    }
    post_data = request.get_json()
    try:
        interviewer = Interviewer.query.get(id)
        if not interviewer:
            response_object['message'] = 'Interviewer not found'
            return jsonsify(response_object), 404
        else:
            interviewer.firstname = post_data.get('firstname')
            interviewer.lastname = post_data.get('lastname')
            interviewer.email = post_data.get('email')
            db.session.commit()
            response_object = {
                'status': 'Modified', 
                'message': 'The interviewer has been update'
                }
            return response_object, 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

#To delete interviewer
@interview_blueprint.route('/interviewer/delete/<id>', methods=['DELETE'])
def delete_interviewer(id):
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
            return  jsonify(response_object), 200
        else:
            return jsonify(response_object), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500

#create candidate
@interview_blueprint.route('/candidate/create', methods=['POST'])
def create_candidate():
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
        candidate = Candidates.query.filter_by(email=post_data.get('email')).first()
        if not candidate:
            new_candidate = Candidates(
                firstname = firstname,
                lastname = lastname,
                email = email
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

#Get candidate details
@interview_blueprint.route('/candidate/<id>', methods=['GET'])
def candidate_detail(id):
    """Get Candidate details giving it id"""
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
            response_object ={
                'status' : 'fail',
                'message': 'candidate does not exist.'}
            return jsonify(response_object), 401
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

@interview_blueprint.route('/candidate/lists', methods=['GET'])
def get_all_candidate():
    # This function provide the list of all candidate in the system
        response_object = {
            'status': 'success',
            'data': {
                'users': [candidate.to_json() for candidate in Candidates.query.all()]
            }
        }
        return jsonify(response_object), 200

@interview_blueprint.route('/candidate/update/<id>', methods=['PUT'])
def update_candidate(id):
    """To update a candidate in the systeme"""
    response_object = {
        'status': 'fail',
        'message': 'Sorry. The candidate does not exist'
    }
    post_data = request.get_json()
    try:
        candidate = Candidates.query.get(id)
        if not candidate:
            response_object['message'] = 'Candidate not found'
            return jsonsify(response_object), 404
        else:
            candidate.firstname = post_data.get('firstname')
            candidate.lastname = post_data.get('lastname')
            candidate.email = post_data.get('email')
            db.session.commit()
            response_object = {
                'status': 'Modified', 
                'message': 'The candidate has been update'
                }
            return response_object, 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

#To delete a candidate
@interview_blueprint.route('/candidate/delete/<id>', methods=['DELETE'])
def delete_candidate(id):
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
            return  jsonify(response_object), 200
        else:
            return jsonify(response_object), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500

#create interview slot
@interview_blueprint.route('/interview/create', methods=['POST'])
def create_interview():
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
        interview = Interview.query.filter_by(title=title, start_time=start_time, end_time=end_time).first()
        if not interview:
            new_interview = Interview(
                title = title,
                start_time = start_time,
                end_time = end_time
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

@interview_blueprint.route('/interview/<id>', methods=['GET'])
def get_interview(id):
    """Get interview details giving it id"""
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
                    'id': inteview.id,
                    'start_time': inteview.start_time,
                    'end_time': inteview.end_time
                }
            }
            return jsonify(response_object), 200
        else:
            response_object ={
                'status' : 'fail',
                'message': 'Interview does not exist.'}
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

@interview_blueprint.route('/interview_emptyslot', methods=['GET'])
def interview_emptyslot():
    """Get interview empyty slot for a candidate"""
    
    response_object = {
            'status': 'success',
            'data': {
                'users': [interviewer.to_json() for interviewer in Interview.query.filter(Interview.candidate_id==None).all()]
            }
        }
    return jsonify(response_object), 200
