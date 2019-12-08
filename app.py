import os
import sys
import json
import http.client

from sqlalchemy import exc
from flask_cors import CORS
from flask import Flask, request, Response, jsonify, abort, make_response
from models import setup_db, seed_db, db_rollback, db_close, Exercise_Template, Workout_Template, Workout_Exercise, Exercise, Workout, Exercise_Set
from auth import requires_auth, get_access_token, get_role_id, get_fitStat_clients
from settings import setup_environment

setup_environment()

app = Flask(__name__)
if os.getenv("FLASK_ENV") == 'development':
    setup_db(app)
    seed_db()

if app.config.get("SQLALCHEMY_DATABASE_URI") is None:
    setup_db(app)

CORS(app)

#separate into error file later

def internal_error(err):
    err["status"] = True
    if err["code"] is None:
        err["code"] = 500
    err["msg"] = sys.exc_info()
    db_rollback()
    print("Error: {}".format(sys.exc_info()))

def return_error(err):
    if err["status"] == True:
            abort(err["code"])

@app.route("/", methods=["GET"])
def hello_world():

    return jsonify({
        "success": True,
    }), 200

"""allows users to read all exercise templates in the database"""
@app.route("/exercise_templates", methods=["GET"])
@requires_auth(['get:exercise_templates'])
def get_exercises(payload):

    err = {
        "status": False,
        "code": None,
        "status": None
    }

    try:

        query = Exercise_Template.query.all()
        exercises = [exercise.long() for exercise in query]

    except:

        internal_error(err)

    finally:

        return_error(err)

        return jsonify({
            "exercises": exercises,
            "success": True
        })

"""allows users to read specific exercise templates by ID"""
@app.route("/exercise_templates/<int:exercise_template_id>", methods=["GET"])
@requires_auth(['get:exercise_templates'])
def get_exercise_by_id(payload, exercise_template_id):

    err = {
        "status": False,
        "code": None,
        "status": None
    }
    
    try:

        exercise_template = Exercise_Template.query.get(exercise_template_id)

    except:
        internal_error(err)
    finally:
        return_error(err)
        return jsonify({
            "exercise": exercise_template.long(),
            "success": True
        })

"""allow user to post an exercise template to the database"""
@app.route('/exercise_templates', methods=['POST'])
@requires_auth(['post:exercise_templates'])
def post_exercises(payload):

    err = {
        "status": False,
        "code": None,
        "status": None
    }

    try:
        
        new_exercise = Exercise_Template(
            name=request.json.get('name'),
            description=request.json.get('name')
        )
        new_exercise.insert()

    except:

        internal_error(err)

    finally:

        return_error(err)

        return jsonify({
            'new_exercise': new_exercise.long(),
            'success': True
        })

        db_close()

"""allow user to edit an exercise template in the database"""
@app.route('/exercise_templates/<int:exercise_template_id>', methods=['PATCH'])
@requires_auth(['patch:exercise_templates'])
def patch_exercises(payload, exercise_template_id):

    err = {
        "status": False,
        "code": None,
        "status": None
    }

    try:
        exercise = Exercise_Template.query.get(exercise_template_id)
        exercise.name = request.json.get('name')
        exercise.description = request.json.get('description')
        exercise.update()

    except:
        internal_error(err)
    finally:
        return_error(err)
        return jsonify({
            'edited_exercise': exercise.long(),
            'success': True
        })
        db_close()

"""allow user to delete an exercise template in the database"""
@app.route('/exercise_templates/<int:exercise_template_id>', methods=['DELETE'])
@requires_auth(['delete:exercise_templates'])
def delete_exercises(payload, exercise_template_id):

    err = {
        "status": False,
        "code": None,
        "status": None
    }

    try:
        workout_exercises = Workout_Exercise.query.filter_by(
            exercise_template_id=exercise_template_id).all()
        for workout_exercise in workout_exercises:
            workout_exercise.delete()
        exercises = Exercise.query.filter_by(
            exercise_template_id=exercise_template_id).all()
        for exercise in exercises:
            exercise.delete()
        exercise_template = Exercise_Template.query.get(exercise_template_id)
        exercise_template.delete()

    except:
        internal_error(err)
    finally:
        return_error(err)
        return jsonify({
            "success": True,
            "deleted_exercise": exercise_template.long()
        })
        db_close()

"""allow user to read a workout template from the database"""
@app.route('/workout_templates', methods=['GET'])
@requires_auth(['get:workout_templates'])
def get_workout_templates(payload):

    err = {
        "status": False,
        "code": None,
        "status": None
    }
    
    try:
        query = Workout_Template.query.all()

        workouts = [workout.long() for workout in query]
        
    except:
        internal_error(err)
    finally:
        return_error(err)
        return jsonify({
            "success": True,
            "workouts": workouts
        })

"""allow user to read specific workout templates from the database"""
@app.route('/workout_templates/<workout_template_id>', methods=['GET'])
@requires_auth(['get:workout_templates'])
def get_workout_template_by_id(payload, workout_template_id):

    err = {
        "status": False,
        "code": None,
        "status": None
    }
    
    try:
        workout_template = Workout_Template.query.get(workout_template_id)
    except:
        internal_error(err)
    finally:
        return_error(err)
        return jsonify({
            "success": True,
            "workouts": workout_template.long()
        })

"""allow user to post a workout template to the database"""
@app.route('/workout_templates', methods=['POST'])
@requires_auth(['post:workout_templates'])
def post_workout_templates(payload):

    err = {
        "status": False,
        "code": None,
        "status": None
    }
    
    try:
        new_workout_template = Workout_Template(
            name=request.json.get('name'),
            description=request.json.get('description')
        )
        new_workout_template.insert()
        for exercise in request.json.get('exercises'):
            new_workout_template_exercise = Workout_Exercise(
                recommended_sets=exercise['recommended_sets'],
                exercise_template_id=exercise['exercise_template_id'],
                workout_template_id=new_workout_template.id
            )
            new_workout_template_exercise.insert()

    except:
        internal_error(err)
    finally:
        return_error(err)
        return jsonify({
            "success": True,
            "new_workout": new_workout_template.long()
        })
        db_close()

"""allow user to edit a workout template in the database"""
@app.route('/workout_templates/<int:workout_template_id>', methods=['PATCH'])
@requires_auth(['patch:workout_templates'])
def patch_workout_templates(payload, workout_template_id):

    err = {
        "status": False,
        "code": None,
        "status": None
    }

    try:

        workout = Workout_Template.query.get(workout_template_id)
        workout.name = request.json.get('name')
        workout.description = request.json.get('description')
        workout.update()
        patched_exercises = [exercise.get(
            'id') for exercise in request.json.get('exercises')]

        for exercise in request.json.get('exercises'):
            if exercise.get('id') == None:
                new_exercise = Workout_Exercise(
                    recommended_sets=exercise['recommended_sets'],
                    exercise_template_id=exercise['exercise_template_id'],
                    workout_template_id=workout.id
                )
                new_exercise.insert()

        for exercise in workout.exercises:

            patch_exercise = Workout_Exercise.query.get(exercise.id)

            if exercise.id in patched_exercises:
                patch_exercise.recommended_sets = exercise.recommended_sets
                patch_exercise.exercise_template_id = exercise.exercise_template_id
                patch_exercise.update()

            if exercise.id not in patched_exercises:
                patch_exercise.delete()

    except:
        internal_error(err)

    finally:
        return_error(err)
        return jsonify({
            "success": True,
            "edited_workout": workout.long()
        })
        db_close()

    return jsonify({
        "success": True,
    })

"""allow user to delete a workout template from the database"""
@app.route('/workout_templates/<int:workout_template_id>', methods=['DELETE'])
@requires_auth(['delete:workout_templates'])
def delete_workout_templates(payload, workout_template_id):

    err = {
        "status": False,
        "code": None,
        "status": None
    }

    try:

        workout = Workout_Template.query.get(workout_template_id)

        for exercise in workout.exercises:
            exercise.delete()

        workouts = Workout.query.filter_by(
            workout_template_id=workout_template_id).all()

        for work_out in workouts:

            work_out.delete()

        workout.delete()
    except:
        internal_error(err)
    finally:
        return_error(err)
        return jsonify({
            "success": True,
            "deleted_workout": workout.long()
        })
        db_close()

"""allow user to read their own workouts from the database"""
@app.route('/workouts', methods=['GET'])
@requires_auth(['get:workouts'])
def get_workouts(payload):

    err = {
        "status": False,
        "code": None,
        "status": None
    }

    user_id = payload['sub']

    try:
        query = Workout.query.filter_by(user_id=user_id).all()
        workouts = [workout.long() for workout in query]
        for workout in workouts:
            if user_id != workout['user_id']:
                err['status'] = True
                err['code'] = 403
    except:
        internal_error(err)
    finally:
        return_error(err)
        return jsonify({
            "success": True,
            "workouts": workouts
        })

"""allow user to read their own specific workouts from the database"""
@app.route('/workouts/<int:workout_id>', methods=['GET'])
@requires_auth(['get:workouts'])
def get_workout_by_id(payload, workout_id):

    err = {
        "status": False,
        "code": None,
        "status": None
    }

    user_id = payload['sub']
    try:
        workout = Workout.query.get(workout_id)
        if user_id != workout.user_id:
            err['status'] = True
            err['code'] = 403
    except:
        internal_error(err)
    finally:
        return_error(err)
        return jsonify({
            "success": True,
            "workout": workout.long()
        })

"""allow user to post their own workouts to the database"""
@app.route('/workouts', methods=['POST'])
@requires_auth(['post:workouts'])
def post_workouts(payload):

    err = {
        "status": False,
        "code": None,
        "status": None
    }

    user_id = payload['sub']
    try:
        new_workout = Workout(
            date=request.json.get('date'),
            user_id=user_id,
            workout_template_id=request.json.get('workout_template_id')
        )
        new_workout.insert()
        for exercise in request.json.get('exercises'):
            
            new_exercise = Exercise(
                exercise_template_id=exercise['exercise_template_id'],
                workout_id=new_workout.id
            )
            new_exercise.insert()
            for exercise_set in exercise['exercise_sets']:
                new_exercise_set = Exercise_Set(
                    weight=exercise_set['weight'],
                    repetitions=exercise_set['repetitions'],
                    rest=exercise_set['rest'],
                    exercise_id=new_exercise.id
                )
                new_exercise_set.insert()
    except:
        internal_error(err)
    finally:
        return_error(err)
        return jsonify({
            "success": True,
            "new_workout": new_workout.long()
        })

"""allow user to edit their own workouts in the database"""
@app.route('/workouts/<int:workout_id>', methods=['PATCH'])
@requires_auth(['patch:workouts'])
def patch_workouts(payload, workout_id):

    err = {
        "status": False,
        "code": None,
        "status": None
    }

    user_id = payload['sub']
    try:
        workout = Workout.query.get(workout_id)
        if user_id != workout.user_id:
            err['status'] = True
            err['code'] = 403
        else:    
            workout.date = request.json.get('date')
            workout.workout_template_id = request.json.get('workout_template_id')
            workout.update()

            patched_exercises = [exercise.get(
                'id') for exercise in request.json.get('exercises')]

            # check to see if there are any new exercises and add them to the database
            for exercise in request.json.get('exercises'):

                if exercise.get('id') is None:

                    new_exercise = Exercise(
                        exercise_template_id=exercise['exercise_template_id'],
                        workout_id=workout.id
                    )
                    new_exercise.insert()

                    patched_exercises.append(new_exercise.id)

                    for exercise_set in exercise['exercise_sets']:
                        new_set = Exercise_Set(
                            weight=exercise_set['weight'],
                            repetitions=exercise_set['repetitions'],
                            rest=exercise_set['rest'],
                            exercise_id=new_exercise.id
                        )
                        new_set.insert()
                else:

                    patch_exercise = Exercise.query.get(exercise.get('id'))

                    oringial_exercise_ids = [a.id for a in workout.exercises]
                    for exercise_id in oringial_exercise_ids:
                        if exercise_id not in patched_exercises:
                            delete_exercise = Exercise.query.get(exercise_id)
                            for old_exercise_set in delete_exercise.exercise_sets:
                                print(old_exercise_set)
                                delete_exercise_set = Exercise_Set.query.get(
                                    old_exercise_set.id)
                                delete_exercise_set.delete()
                            delete_exercise.delete()

                    if patch_exercise.id in patched_exercises:
                        patch_exercise.exercise_template_id = exercise['exercise_template_id']
                        patch_exercise.update()

                        patched_sets = [_exercise_set_.get(
                            'id') for _exercise_set_ in exercise.get('exercise_sets')]

                        for exercise_set in exercise.get('exercise_sets'):

                            if exercise_set.get('id') is None:
                                new_exercise_set = Exercise_Set(
                                    weight=exercise_set['weight'],
                                    repetitions=exercise_set['repetitions'],
                                    rest=exercise_set['rest'],
                                    exercise_id=patch_exercise.id
                                )
                                new_exercise_set.insert()
                            else:

                                patch_exercise_set = Exercise_Set.query.get(
                                    exercise_set.get('id'))

                                original_exercise_sets = [
                                    a.id for a in patch_exercise.exercise_sets]
                                print(original_exercise_sets)
                                for set_id in original_exercise_sets:
                                    if set_id not in patched_sets:
                                        delete_set = Exercise_Set.query.get(set_id)
                                        delete_set.delete()

                                if patch_exercise_set.id in patched_sets:
                                    patch_exercise_set.weight = exercise_set['weight']
                                    patch_exercise_set.repetitions = exercise_set['repetitions']
                                    patch_exercise_set.rest = exercise_set['rest']
                                    patch_exercise_set.exercise_id = patch_exercise.id
                                    patch_exercise_set.update()

    except:
        internal_error(err)
    finally:
        return_error(err)
        return jsonify({
            "success": True,
            "edited_workout": workout.long()
        })
        db_close()

"""allow user to delete their own workouts in the database"""
@app.route('/workouts/<int:workout_id>', methods=['DELETE'])
@requires_auth(['delete:workouts'])
def delete_workouts(payload, workout_id):

    err = {
        "status": False,
        "code": None,
        "status": None
    }

    user_id = payload['sub']
    
    try:
        workout = Workout.query.get(workout_id)
        
        
        if workout.user_id == None:
            err["status"] = True
            err["code"] = 404
            

        if workout.user_id != user_id:
            err["status"] = True
            err["code"] = 403
        else:
            
            for exercise in workout.exercises:
                delete_exercise = Exercise.query.get(exercise.id)
                for exercise_set in delete_exercise.exercise_sets:
                    delete_set = Exercise_Set.query.get(exercise_set.id)
                    delete_set.delete()
                delete_exercise.delete()
        
            workout.delete()
        

    except:
        internal_error(err)
    finally:
        return_error(err)
        return jsonify({
            "success": True,
            "deleted_workout": workout.long()
        })
        db_close()






"""allow user to read any/all workouts in the database"""
@app.route('/trainer/workouts', methods=['GET'])
@requires_auth(['get:trainer_workouts'])
def get_workouts_as_trainer(payload):

    err = {
        "status": False,
        "code": None,
        "status": None
    }

    try:

        query = Workout.query.all()
        workouts = [workout.long() for workout in query]

    except:

        internal_error(err)

    finally:

        return_error(err)

        return jsonify({
            "success": True,
            "workouts": workouts
        })

"""allow user to read any/all specific workouts in the database by ID"""
@app.route('/trainer/workouts/<int:workout_id>', methods=['GET'])
@requires_auth(['get:trainer_workouts'])
def get_workout_by_id_as_trainer(payload, workout_id):

    err = {
        "status": False,
        "code": None,
        "status": None
    }

    try:

        workout = Workout.query.get(workout_id)

    except:

        internal_error(err)

    finally:

        return_error(err)

        return jsonify({
            "success": True,
            "workout": workout.long()
        })

"""allow user to read any/all specific workouts in the database by ID"""
@app.route('/trainer/workouts-by-user/<string:user_id>', methods=['GET'])
@requires_auth(['get:trainer_workouts'])
def get_workout_by_user_id_as_trainer(payload, user_id):

    err = {
        "status": False,
        "code": None,
        "status": None
    }

    try:

        query = Workout.query.filter_by(user_id=user_id)
        workouts = [workout.long() for workout in query]
        
    except:

        internal_error(err)

    finally:

        return_error(err)

        return jsonify({
            "success": True,
            "workouts": workouts
        })

"""allow user to post any/all workouts to the database"""
@app.route('/trainer/workouts', methods=['POST'])
@requires_auth(['post:trainer_workouts'])
def post_workouts_as_trainer(payload):

    err = {
        "status": False,
        "code": None,
        "status": None
    }

    user_id = payload['sub']

    try:
        new_workout = Workout(
            date=request.json.get('date'),
            user_id=request.json.get('user_id'),
            workout_template_id=request.json.get('workout_template_id')
        )
        new_workout.insert()
        for exercise in request.json.get('exercises'):
            print(exercise)
            new_exercise = Exercise(
                exercise_template_id=exercise['exercise_template_id'],
                workout_id=new_workout.id
            )
            new_exercise.insert()
            for exercise_set in exercise['exercise_sets']:
                new_exercise_set = Exercise_Set(
                    weight=exercise_set['weight'],
                    repetitions=exercise_set['repetitions'],
                    rest=exercise_set['rest'],
                    exercise_id=new_exercise.id
                )
                new_exercise_set.insert()
    except:
        internal_error(err)
    finally:
        return_error(err)
        return jsonify({
            "success": True,
            "new_workout": new_workout.long()
        })

"""allow user to patch any/all workouts in the database"""
@app.route('/trainer/workouts/<int:workout_id>', methods=['PATCH'])
@requires_auth(['patch:trainer_workouts'])
def patch_workouts_as_trainer(payload, workout_id):

    err = {
        "status": False,
        "code": None,
        "status": None
    }

    user_id = payload['sub']

    try:
        workout = Workout.query.get(workout_id)
        
        workout.date = request.json.get('date')
        workout.workout_template_id = request.json.get('workout_template_id')
        workout.user_id = request.json.get('user_id')
        workout.update()

        patched_exercises = [exercise.get(
            'id') for exercise in request.json.get('exercises')]

        # check to see if there are any new exercises and add them to the database
        for exercise in request.json.get('exercises'):

            if exercise.get('id') is None:

                new_exercise = Exercise(
                    exercise_template_id=exercise['exercise_template_id'],
                    workout_id=workout.id
                )
                new_exercise.insert()

                patched_exercises.append(new_exercise.id)

                for exercise_set in exercise['exercise_sets']:
                    new_set = Exercise_Set(
                        weight=exercise_set['weight'],
                        repetitions=exercise_set['repetitions'],
                        rest=exercise_set['rest'],
                        exercise_id=new_exercise.id
                    )
                    new_set.insert()
            else:

                patch_exercise = Exercise.query.get(exercise.get('id'))

                oringial_exercise_ids = [a.id for a in workout.exercises]
                for exercise_id in oringial_exercise_ids:
                    if exercise_id not in patched_exercises:
                        delete_exercise = Exercise.query.get(exercise_id)
                        for old_exercise_set in delete_exercise.exercise_sets:
                            print(old_exercise_set)
                            delete_exercise_set = Exercise_Set.query.get(
                                old_exercise_set.id)
                            delete_exercise_set.delete()
                        delete_exercise.delete()

                if patch_exercise.id in patched_exercises:
                    patch_exercise.exercise_template_id = exercise['exercise_template_id']
                    patch_exercise.update()

                    patched_sets = [_exercise_set_.get(
                        'id') for _exercise_set_ in exercise.get('exercise_sets')]

                    for exercise_set in exercise.get('exercise_sets'):

                        if exercise_set.get('id') is None:
                            new_exercise_set = Exercise_Set(
                                weight=exercise_set['weight'],
                                repetitions=exercise_set['repetitions'],
                                rest=exercise_set['rest'],
                                exercise_id=patch_exercise.id
                            )
                            new_exercise_set.insert()
                        else:

                            patch_exercise_set = Exercise_Set.query.get(
                                exercise_set.get('id'))

                            original_exercise_sets = [
                                a.id for a in patch_exercise.exercise_sets]
                            print(original_exercise_sets)
                            for set_id in original_exercise_sets:
                                if set_id not in patched_sets:
                                    delete_set = Exercise_Set.query.get(set_id)
                                    delete_set.delete()

                            if patch_exercise_set.id in patched_sets:
                                patch_exercise_set.weight = exercise_set['weight']
                                patch_exercise_set.repetitions = exercise_set['repetitions']
                                patch_exercise_set.rest = exercise_set['rest']
                                patch_exercise_set.exercise_id = patch_exercise.id
                                patch_exercise_set.update()

    except:
        internal_error(err)
    finally:
        return_error(err)
        return jsonify({
            "success": True,
            "edited_workout": workout.long()
        })
        db_close()

"""allow user to delete any/all workouts in the database"""
@app.route('/trainer/workouts/<int:workout_id>', methods=['DELETE'])
@requires_auth(['delete:trainer_workouts'])
def delete_workouts_as_trainer(payload, workout_id):

    err = {
        "status": False,
        "code": None,
        "status": None
    }

    user_id = payload['sub']
    try:
        workout = Workout.query.get(workout_id)
        for exercise in workout.exercises:
            delete_exercise = Exercise.query.get(exercise.id)
            for exercise_set in delete_exercise.exercise_sets:
                delete_set = Exercise_Set.query.get(exercise_set.id)
                delete_set.delete()
            delete_exercise.delete()
        workout.delete()

    except:
        internal_error(err)
    finally:
        return_error(err)
        return jsonify({
            "success": True,
            "deleted_workout": workout.long()
        })
        db_close()

"""allow user to read clients in the database"""
@app.route('/clients', methods=['GET'])
@requires_auth(['get:fitStat_clients'])
def get_clients(payload):

    err = {
        "status": False,
        "code": None,
        "status": None
    }

    try:
        clients = get_fitStat_clients()
    except:
        internal_error(err)
    finally:
        return_error(err)
        return jsonify({
            "success": True,
            "workout": clients
        })
        db_close()

# handle bad request errors
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": error.description,
    }), 400

# handle bad request errors
@app.errorhandler(401)
def unathenticated_request(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": error.description,
    }), 401

# handle bad request errors
@app.errorhandler(403)
def unauthorized_request(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": error.description,
    }), 403

    # handle bad request errors
@app.errorhandler(404)
def unauthorized_request(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": error.description,
    }), 404

# handle bad request errors
@app.errorhandler(405)
def intentional_error(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": error.description,
    }), 405

# handle bad request errors
@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": error.description,
    }), 500


if __name__ == '__main__':
    app.run()
