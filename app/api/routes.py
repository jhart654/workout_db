from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Exercises, exercise_schema, exercises_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/exercises', methods = ['POST'])
@token_required
def create_exercise(current_user_token):
    name = request.json['name']
    body_part = request.json['body_part']
    equipment = request.json['equipment']
    sets = request.json['sets']
    reps = request.json['reps']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    exercises = Exercises(name, body_part, equipment, sets, reps, user_token = user_token)

    db.session.add(exercises)
    db.session.commit()

    response = exercise_schema.dump(exercises)
    return jsonify(response)

@api.route('/exercises', methods = ['GET'])
@token_required
def get_exercises(current_user_token):
    a_user = current_user_token.token
    exercises = Exercises.query.filter_by(user_token = a_user).all()
    response = exercises_schema.dump(exercises)
    return jsonify(response)

@api.route('/exercises/<id>', methods = ['GET'])
@token_required
def get_single_exercise(current_user_token, id):
    exercises = Exercises.query.get(id)
    response = exercise_schema.dump(exercises)
    return jsonify(response)

@api.route('/exercises/<id>', methods = ['POST', 'PUT'])
@token_required
def update_exercise(current_user_token, id):
    exercises = Exercises.query.get(id)
    exercises.name = request.json['name']
    exercises.body_part = request.json['body_part']
    exercises.equipment = request.json['equipment']
    exercises.sets = request.json['sets']
    exercises.reps = request.json['reps']

    db.session.commit()
    response = exercise_schema.dump(exercises) 
    return jsonify(response)        

@api.route('/exercises/<id>', methods = ['DELETE'])
@token_required
def delete_contact(current_user_token, id):
    exercises = Exercises.query.get(id)
    db.session.delete(exercises)
    db.session.commit()
    response = exercise_schema.dump(exercises)
    return jsonify(response)
