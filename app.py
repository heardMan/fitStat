import os
import sys
import json
import http.client

from sqlalchemy import exc
from flask_cors import CORS
from flask import (
    Flask, request, Response, jsonify,
    abort, make_response, send_from_directory, render_template
)
from models import (
    setup_db, seed_db, db_rollback, db_close, ExerciseTemplate,
    WorkoutTemplate, WorkoutExercise, Exercise, Workout, ExerciseSet
)
from auth import (
    requires_auth, get_access_token,
    get_role_id, get_fitStat_clients
)
from settings import setup_environment

# set up envoironment variables in from the .env file if there is one
setup_environment()

app = Flask(__name__)
# setup_db(app)

if app.config.get("SQLALCHEMY_DATABASE_URI") is None:
    setup_db(app)
    # seed_db()

CORS(app)


# this function handles internal server error
# that results from bad database transactions
def internal_error(err):
    # set error object properties
    err["status"] = True
    if err["code"] is None:
        err["code"] = 500
    err["msg"] = sys.exc_info()
    # roll back the database session
    db_rollback()
    # log error details to the server
    print("Error: {}".format(sys.exc_info()))

# this function checks the error object and sends an error if necessary


def check_error(err):
    if err["status"] is True:
        abort(err["code"], description=err['msg'])

# this is a simple route for testing purposes
# I plan to possibly host some documentation here eventually
@app.route("/", methods=["GET"])
def hello_world():

    return jsonify({
        "success": True,
    }), 200


"""allows users to read all exercise templates in the database"""
@app.route("/exercise_templates", methods=["GET"])
@requires_auth(['get:exercise_templates'])
def get_exercises(payload):
    # set custom error object
    err = {
        "status": False,
        "code": None,
        "msg": None
    }

    try:
        # query the database for all exercise templates
        query = ExerciseTemplate.query.all()
        # if no templates are found send the user a 404 error
        if query is None:
            err['status'] = True
            err['code'] = 404
            err['msg'] = 'Resource not found'
        else:
            # create a comprhension from the query
            exercises = [exercise.long() for exercise in query]

    except Exception:
        # handle any exception from the database
        internal_error(err)

    finally:
        # check error status
        check_error(err)
        # send response
        return jsonify({
            "exercises": exercises,
            "success": True
        })


"""allows users to read specific exercise templates by ID"""
@app.route("/exercise_templates/<int:exercise_template_id>", methods=["GET"])
@requires_auth(['get:exercise_templates'])
def get_exercise_by_id(payload, exercise_template_id):
    # set custom error object
    err = {
        "status": False,
        "code": None,
        "msg": None
    }

    try:
        exercise_template = ExerciseTemplate.query.get(exercise_template_id)

        # if no templates are found send the user a 404 error
        if exercise_template is None:
            err['status'] = True
            err['code'] = 404
            err['msg'] = 'Resource not found'

    except Exception:
        # handle any exception from the database
        internal_error(err)
    finally:
        # check error status
        check_error(err)
        # send response
        return jsonify({
            "exercise": exercise_template.long(),
            "success": True
        })


"""allow user to post an exercise template to the database"""
@app.route('/exercise_templates', methods=['POST'])
@requires_auth(['post:exercise_templates'])
def post_exercises(payload):
    # set custom error object
    err = {
        "status": False,
        "code": None,
        "msg": None
    }

    try:
        # ensure name property is present
        if request.json.get('name') is None:
            err['status'] = True
            err['code'] = 400
            err['msg'] = 'Bad Request: No Name Property Found'
        # ensure name property is a string
        elif type(request.json.get('name')) is not str:
            err['status'] = True
            err['code'] = 400
            err['msg'] = 'Bad Request: Name Property Must Be a String'
        # ensure name propery is not blank
        elif request.json.get('name') is '':
            err['status'] = True
            err['code'] = 400
            err['msg'] = 'Bad Request: Name Property Cannot Be Blank'
        # ensure description property is present
        elif request.json.get('description') is None:
            err['status'] = True
            err['code'] = 400
            err['msg'] = 'Bad Request: No Description Property Found'
        # ensure description property is a string
        elif type(request.json.get('name')) is not str:
            err['status'] = True
            err['code'] = 400
            err['msg'] = 'Bad Request: Description Property Must Be a String'
        # ensure description property is not blank
        elif request.json.get('description') is '':
            err['status'] = True
            err['code'] = 400
            err['msg'] = 'Bad Request: Description Property Cannot Be Blank'

        else:
            # define a new exercise instance
            new_exercise = ExerciseTemplate(
                name=request.json.get('name'),
                description=request.json.get('description')
            )
            # insert the instance to the database
            new_exercise.insert()

    except Exception:
        # handle any exception from the database
        internal_error(err)

    finally:
        # check error status
        check_error(err)
        # send response
        return jsonify({
            'new_exercise': new_exercise.long(),
            'success': True
        })
        # close database session
        db_close()


"""allow user to edit an exercise template in the database"""
@app.route('/exercise_templates/<int:exercise_template_id>', methods=['PATCH'])
@requires_auth(['patch:exercise_templates'])
def patch_exercises(payload, exercise_template_id):
    # set custom error object
    err = {
        "status": False,
        "code": None,
        "msg": None
    }

    try:
        exercise = ExerciseTemplate.query.get(exercise_template_id)
        # if no template is found send the user a 404 error
        if exercise is None:
            err['status'] = True
            err['code'] = 404
            err['msg'] = 'Resource not found'
        else:
            # ensure name property is present
            if request.json.get('name') is None:
                err['status'] = True
                err['code'] = 400
                err['msg'] = 'Bad Request: No Name Property Found'
            # ensure name property is not blank
            elif request.json.get('name') is '':
                err['status'] = True
                err['code'] = 400
                err['msg'] = 'Bad Request: Name Property Cannot Be Blank'
            # ensure name property is a string
            elif type(request.json.get('name')) is not str:
                err['status'] = True
                err['code'] = 400
                err['msg'] = 'Bad Request: Name Property Must Be a String'
            # ensure description property is present
            elif request.json.get('description') is None:
                err['status'] = True
                err['code'] = 400
                err['msg'] = 'Bad Request: No Description Property Found'
            # ensure description property is not blank
            elif request.json.get('description') is '':
                err['status'] = True
                err['code'] = 400
                err['msg'] = 'Bad Request: Name Property Cannot Be Blank'
            # ensure description property is a string
            elif type(request.json.get('description')) is not str:
                err['status'] = True
                err['code'] = 400
                err['msg'] = 'Bad Request: Name Property Must Be a String'
            else:
                # set exercise name to user input
                exercise.name = request.json.get('name')
                # set exercise description to user input
                exercise.description = request.json.get('description')
                # updated the instance in the database
                exercise.update()

    except Exception:
        # handle any exception from the database
        internal_error(err)
    finally:
        # check error status
        check_error(err)
        # send response
        return jsonify({
            'edited_exercise': exercise.long(),
            'success': True
        })
        # close database session
        db_close()


"""allow user to delete an exercise template in the database"""


@app.route(
    '/exercise_templates/<int:exercise_template_id>',
    methods=['DELETE']
)
@requires_auth(['delete:exercise_templates'])
def delete_exercises(payload, exercise_template_id):
    # set custom error object
    err = {
        "status": False,
        "code": None,
        "msg": None
    }

    try:
        # query for the exercise template
        exercise_template = ExerciseTemplate.query.get(exercise_template_id)
        # if no template is found send the user a 404 error
        if exercise_template is None:
            err['status'] = True
            err['code'] = 404
            err['msg'] = 'Resource not found'
        else:
            # query all the exercise references tied to the workout templates
            workout_exercises = WorkoutExercise.query.filter_by(
                exercise_template_id=exercise_template_id).all()
            # delete all the exercise references tied to the workout instances
            for workout_exercise in workout_exercises:
                workout_exercise.delete()
            # query all the exercise references tied to the workout instances
            exercises = Exercise.query.filter_by(
                exercise_template_id=exercise_template_id).all()
            # query all the exercise references tied to the workout instances
            for exercise in exercises:
                exercise.delete()

            # delete the exercise template
            exercise_template.delete()

    except Exception:
        # handle any exception from the database
        internal_error(err)
    finally:
        # check error status
        check_error(err)
        # send response
        return jsonify({
            "success": True,
            "deleted_exercise": exercise_template.long()
        })
        # close database session
        db_close()


"""allow user to read a workout template from the database"""
@app.route('/workout_templates', methods=['GET'])
@requires_auth(['get:workout_templates'])
def get_workout_templates(payload):
    # set custom error object
    err = {
        "status": False,
        "code": None,
        "msg": None
    }

    try:
        # query the database for all the workout templates
        query = WorkoutTemplate.query.all()
        # if no templates are found send the user a 404 error
        if query is None:
            err['status'] = True
            err['code'] = 404
            err['msg'] = 'Resource not found'
        else:
            # create a formatted list to send as a response
            workouts = [workout.long() for workout in query]
    except Exception:
        # handle any exception from the database
        internal_error(err)
    finally:
        # check error status
        check_error(err)
        # send response
        return jsonify({
            "success": True,
            "workouts": workouts
        })


"""allow user to read specific workout templates from the database"""
@app.route('/workout_templates/<workout_template_id>', methods=['GET'])
@requires_auth(['get:workout_templates'])
def get_workout_template_by_id(payload, workout_template_id):
    # set custom error object
    err = {
        "status": False,
        "code": None,
        "msg": None
    }

    try:
        # query the database for the specified template
        workout_template = WorkoutTemplate.query.get(workout_template_id)
        # if no templates is found send the user a 404 error
        if workout_template is None:
            err['status'] = True
            err['code'] = 404
            err['msg'] = 'Resource not found'

    except Exception:
        # handle any exception from the database
        internal_error(err)
    finally:
        # check error status
        check_error(err)
        # send response
        return jsonify({
            "success": True,
            "workouts": workout_template.long()
        })


"""allow user to post a workout template to the database"""
@app.route('/workout_templates', methods=['POST'])
@requires_auth(['post:workout_templates'])
def post_workout_templates(payload):
    # set custom error object
    err = {
        "status": False,
        "code": None,
        "msg": None
    }

    try:

        # ensure name property is present
        if request.json.get('name') is None:
            err['status'] = True
            err['code'] = 400
            err['msg'] = 'Bad Request: No Name Property Found'
        # ensure name property is not blank
        elif request.json.get('name') is '':
            err['status'] = True
            err['code'] = 400
            err['msg'] = 'Bad Request: Name Property Cannot Be Blank'
        # ensure name property is a string
        elif type(request.json.get('name')) is not str:
            err['status'] = True
            err['code'] = 400
            err['msg'] = 'Bad Request: Name Property Must Be a String'

        # ensure name property is present
        elif request.json.get('description') is None:
            err['status'] = True
            err['code'] = 400
            err['msg'] = 'Bad Request: No Description Property Found'
        # ensure name property is a string
        elif type(request.json.get('description')) is not str:
            err['status'] = True
            err['code'] = 400
            err['msg'] = 'Bad Request: Description Property Must Be a String'

        # ensure name property is present
        elif request.json.get('exercises') is None:
            err['status'] = True
            err['code'] = 400
            err['msg'] = 'Bad Request: No Name Property Found'

        else:
            # define new workout template instance
            new_workout_template = WorkoutTemplate(
                name=request.json.get('name'),
                description=request.json.get('description')
            )
            # insert the new template into the database
            new_workout_template.insert()

            # define new workout template instance
            for exercise in request.json.get('exercises'):
                # define new workout exercise instance
                new_workout_template_exercise = WorkoutExercise(
                    recommended_sets=exercise['recommended_sets'],
                    exercise_template_id=exercise['exercise_template_id'],
                    workout_template_id=new_workout_template.id
                )
                # insert the new workout exercise instance into the database
                new_workout_template_exercise.insert()

    except Exception:
        # handle any exception from the database
        internal_error(err)
    finally:
        # check error status
        check_error(err)
        # send response
        return jsonify({
            "success": True,
            "new_workout": new_workout_template.long()
        })
        # close database session
        db_close()


"""allow user to edit a workout template in the database"""
@app.route('/workout_templates/<int:workout_template_id>', methods=['PATCH'])
@requires_auth(['patch:workout_templates'])
def patch_workout_templates(payload, workout_template_id):
    # set custom error object
    err = {
        "status": False,
        "code": None,
        "msg": None
    }

    try:
        # query the database for the specified workout template
        workout = WorkoutTemplate.query.get(workout_template_id)

        # ensure name property is present
        if workout is None:
            err['status'] = True
            err['code'] = 404
            err['msg'] = 'Resource not found'
        # ensure name property is present
        elif request.json.get('name') is None:
            err['status'] = True
            err['code'] = 400
            err['msg'] = 'Bad Request: No Name Property Found'
        # ensure name property is not blank
        elif request.json.get('name') is '':
            err['status'] = True
            err['code'] = 400
            err['msg'] = 'Bad Request: Name Property Cannot Be Blank'
        # ensure name property is a string
        elif type(request.json.get('name')) is not str:
            err['status'] = True
            err['code'] = 400
            err['msg'] = 'Bad Request: Name Property Must Be a String'

        # ensure name property is present
        if request.json.get('description') is None:
            err['status'] = True
            err['code'] = 400
            err['msg'] = 'Bad Request: No Name Property Found'
        # ensure name property is not blank
        elif request.json.get('description') is '':
            err['status'] = True
            err['code'] = 400
            err['msg'] = 'Bad Request: Name Property Cannot Be Blank'
        # ensure name property is a string
        elif type(request.json.get('description')) is not str:
            err['status'] = True
            err['code'] = 400
            err['msg'] = 'Bad Request: Name Property Must Be a String'
        else:

            # set the workout template name to user input
            workout.name = request.json.get('name')
            # set the workout template description to user input
            workout.description = request.json.get('description')
            # update workout template in the database
            workout.update()
            # make a list of exercises
            # included in the list of exercises provided by the user
            patched_exercises = [exercise.get(
                'id') for exercise in request.json.get('exercises')]

            # loop through the exercise list
            # this portion of code is responsible for
            # adding new exercises to a workout template
            for exercise in request.json.get('exercises'):
                # if the exercise does not have an id property
                # it will be considered a new exercise
                if exercise.get('id') is None:
                    # define a new workout exercise instance
                    new_exercise = WorkoutExercise(
                        recommended_sets=exercise['recommended_sets'],
                        exercise_template_id=exercise['exercise_template_id'],
                        workout_template_id=workout.id
                    )
                    # add new workout exercise to the database
                    new_exercise.insert()
                    # add the id to the patched exercises list
                    patched_exercises.append(new_exercise.id)

            # loop through the workout exercises in the original model
            # this portion of code is responsible for
            # editing and removing exercises to a workout template
            for exercise in workout.exercises:
                # get the instance currently in the database
                patch_exercise = WorkoutExercise.query.get(exercise.id)

                # if the exercise is in the list the it should be edited
                if exercise.id in patched_exercises:
                    # loop throught the exercises in the user input
                    for _exercise_ in request.json.get('exercises'):
                        # find the matching exercise
                        if _exercise_.get('id') == exercise.id:
                            # update the recommended sets property
                            patch_exercise.recommended_sets = _exercise_.get(
                                'recommended_sets')
                            # update the exercise template ID
                            patch_exercise.exercise_template_id = (
                                _exercise_.get('exercise_template_id'))
                            # update the exercise instance
                            patch_exercise.update()

                # if the exercise ID is not in the patched exercise list
                # then it should be deleted
                if exercise.id not in patched_exercises:
                    # delete the exercise from the database
                    patch_exercise.delete()

    except Exception:
        # handle any exception from the database
        internal_error(err)

    finally:
        # check error status
        check_error(err)
        # send response
        return jsonify({
            "success": True,
            "edited_workout": workout.long()
        })
        # close database session
        db_close()


"""allow user to delete a workout template from the database"""
@app.route('/workout_templates/<int:workout_template_id>', methods=['DELETE'])
@requires_auth(['delete:workout_templates'])
def delete_workout_templates(payload, workout_template_id):
    # set custom error object
    err = {
        "status": False,
        "code": None,
        "msg": None
    }

    try:
        # query the database for the sppecified workout
        workout = WorkoutTemplate.query.get(workout_template_id)
        # if no workout is found send the user a 404 error
        if workout is None:
            err['status'] = True
            err['code'] = 404
            err['msg'] = 'Resource not found'
        else:
            # set a variable to copy the deleted instance for the response
            _workout_ = workout.long()
            # loop through the exercises in the wokrout template
            for exercise in workout.exercises:
                # delete each exercise from the workout template
                exercise.delete()

            # query for all the workouts in the database
            workouts = Workout.query.filter_by(
                workout_template_id=workout_template_id).all()

            for work_out in workouts:
                # delete the workout instances from the database
                work_out.delete()
            # delete the workout template instance
            workout.delete()

    except Exception:
        # handle any exception from the database
        internal_error(err)
    finally:
        # check error status
        check_error(err)
        # send response
        return jsonify({
            "success": True,
            "deleted_workout": _workout_
        })
        # close database session
        db_close()


"""allow user to read their own workouts from the database"""
@app.route('/workouts', methods=['GET'])
@requires_auth(['get:workouts'])
def get_workouts(payload):
    # set custom error object
    err = {
        "status": False,
        "code": None,
        "msg": None
    }

    # set variable to userID from payload
    user_id = payload['sub']

    try:
        # query the database for all Workouts with the user id
        # equal to the user id in the JWT payload
        query = Workout.query.filter_by(user_id=user_id).all()
        # create list of workouts to send in the response
        workouts = [workout.long() for workout in query]
        # check each workout to make sure the user has access to that workout
        for workout in workouts:
            # the user should only have access to
            # their own workouts via this route
            if user_id != workout['user_id']:
                err['status'] = True
                err['code'] = 403
    except Exception:
        # handle any exception from the database
        internal_error(err)
    finally:
        # check error status
        check_error(err)
        # send response
        return jsonify({
            "success": True,
            "workouts": workouts
        })


"""allow user to read their own specific workouts from the database"""
@app.route('/workouts/<int:workout_id>', methods=['GET'])
@requires_auth(['get:workouts'])
def get_workout_by_id(payload, workout_id):
    # set custom error object
    err = {
        "status": False,
        "code": None,
        "msg": None
    }

    # set variable to userID from payload
    user_id = payload['sub']

    try:
        # query the database for a a workout by ID
        workout = Workout.query.get(workout_id)

        # if no workout is found send a 404 error to a user
        if workout is None:
            err['status'] = True
            err['code'] = 404

        # if no workout is found send a 403 error to a user
        if user_id != workout.user_id:
            err['status'] = True
            err['code'] = 403
    except Exception:
        # handle any exception from the database
        internal_error(err)
    finally:
        # check error status
        check_error(err)
        # send response
        return jsonify({
            "success": True,
            "workout": workout.long()
        })


"""allow user to post their own workouts to the database"""
@app.route('/workouts', methods=['POST'])
@requires_auth(['post:workouts'])
def post_workouts(payload):
    # set custom error object
    err = {
        "status": False,
        "code": None,
        "msg": None
    }
    # set variable to userID from payload
    user_id = payload['sub']

    try:
        # ensure name property is present
        if request.json.get('date') is None:
            err['status'] = True
            err['code'] = 400
            err['msg'] = 'Bad Request: No Date Property Found'
        # ensure name property is not blank
        elif request.json.get('date') is '':
            err['status'] = True
            err['code'] = 400
            err['msg'] = 'Bad Request: Date Property Cannot Be Blank'
        # ensure name property is a string
        elif type(request.json.get('date')) is not str:
            err['status'] = True
            err['code'] = 400
            err['msg'] = 'Bad Request: Date Property Must Be a String'
        else:

            # define a new exercise instance
            new_workout = Workout(
                date=request.json.get('date'),
                user_id=user_id,
                workout_template_id=request.json.get('workout_template_id')
            )
            # insert a new exercise instance into the database
            new_workout.insert()
            #
            for exercise in request.json.get('exercises'):

                new_exercise = Exercise(
                    exercise_template_id=exercise['exercise_template_id'],
                    workout_id=new_workout.id
                )
                new_exercise.insert()
                for exercise_set in exercise['exercise_sets']:
                    new_exercise_set = ExerciseSet(
                        weight=exercise_set['weight'],
                        repetitions=exercise_set['repetitions'],
                        rest=exercise_set['rest'],
                        exercise_id=new_exercise.id
                    )
                    new_exercise_set.insert()
    except Exception:
        # handle any exception from the database
        internal_error(err)
    finally:
        # check error status
        check_error(err)
        # send response
        return jsonify({
            "success": True,
            "new_workout": new_workout.long()
        })


"""allow user to edit their own workouts in the database"""
@app.route('/workouts/<int:workout_id>', methods=['PATCH'])
@requires_auth(['patch:workouts'])
def patch_workouts(payload, workout_id):
    # set custom error object
    err = {
        "status": False,
        "code": None,
        "msg": None
    }

    # set variable to userID from payload
    user_id = payload['sub']

    try:
        # query the database for workouts with the specified ID
        workout = Workout.query.get(workout_id)

        # make sure the user has access to the workout
        if user_id != workout.user_id:
            err['status'] = True
            err['code'] = 403

        else:
            # update the date property of the workout
            workout.date = request.json.get('date')
            # update the associated workout template
            workout.workout_template_id = request.json.get(
                'workout_template_id')
            # update the instance in the database
            workout.update()
            # create a list of all exerises included the specified workout
            patched_exercises = [exercise.get(
                'id') for exercise in request.json.get('exercises')]

            # check to see if there are any new exercises
            # and add them to the database
            for exercise in request.json.get('exercises'):
                # if the exercise has no ID then it is new exercise
                if exercise.get('id') is None:
                    # define a new workout exercise instance
                    new_exercise = Exercise(
                        exercise_template_id=exercise['exercise_template_id'],
                        workout_id=workout.id
                    )
                    # insert the new exercise instance into the database
                    new_exercise.insert()

                    # add the exercise ID to the patched exercises list
                    patched_exercises.append(new_exercise.id)

                    # if the exercise is new we must also
                    # add sets for the workout exercise
                    for exercise_set in exercise['exercise_sets']:
                        # define a exercise set instance
                        new_set = ExerciseSet(
                            weight=exercise_set['weight'],
                            repetitions=exercise_set['repetitions'],
                            rest=exercise_set['rest'],
                            exercise_id=new_exercise.id
                        )

                        # insert the exercise set instance into the database
                        new_set.insert()
                else:

                    # find the workout exercise instance in the database
                    patch_exercise = Exercise.query.get(exercise.get('id'))

                    # create a list of exercises
                    # in the original workout instance
                    oringial_exercise_ids = [a.id for a in workout.exercises]

                    # check each exercise ID
                    for exercise_id in oringial_exercise_ids:

                        # if the exercise ID is not
                        # in the patched exercises list
                        # then it should be deleted
                        if exercise_id not in patched_exercises:

                            # find the exercise instance in the database
                            delete_exercise = Exercise.query.get(exercise_id)

                            # loop through the list of exercise sets
                            delete_list = delete_exercise.exercise_sets
                            for old_exercise_set in delete_list:
                                # query database for set instance
                                delete_exercise_set = ExerciseSet.query.get(
                                    old_exercise_set.id)
                                # delete set instance in the database
                                delete_exercise_set.delete()

                            # delete the workout exercise in the database
                            delete_exercise.delete()

                    # if the exercise ID is in the patched exercises list
                    # then it should be updated
                    if patch_exercise.id in patched_exercises:
                        # update the exercise template ID property
                        patch_exercise.exercise_template_id = (
                            exercise['exercise_template_id'])
                        # update the exercise instance in the database
                        patch_exercise.update()

                        # create a list of the set in the
                        # exercise IDs sent with the request
                        patched_sets = [_exercise_set_.get(
                            'id') for _exercise_set_ in exercise.get(
                                'exercise_sets')]

                        # loop through each set in the list
                        for exercise_set in exercise.get('exercise_sets'):

                            # if there is no exercise property
                            # then we will consider this a new exercise
                            if exercise_set.get('id') is None:
                                # define a new exercise set
                                new_exercise_set = ExerciseSet(
                                    weight=exercise_set['weight'],
                                    repetitions=exercise_set['repetitions'],
                                    rest=exercise_set['rest'],
                                    exercise_id=patch_exercise.id
                                )
                                # insert the new exercise
                                # set in the the database
                                new_exercise_set.insert()

                            else:
                                # query the database for
                                # the original workout exercise instance
                                patch_exercise_set = ExerciseSet.query.get(
                                    exercise_set.get('id'))
                                # create a list of the set ID from
                                # the original workout exercise instance
                                original_exercise_sets = [
                                    a.id for a in patch_exercise.exercise_sets]

                                # loop through each set
                                for set_id in original_exercise_sets:
                                    # if the set ID is not in the patched sets
                                    if set_id not in patched_sets:
                                        # query the database
                                        # for the original set instance
                                        delete_set = ExerciseSet.query.get(
                                            set_id)
                                        # delete the exercise set
                                        delete_set.delete()

                                # if the exercise set is in
                                # patched sets then it should be updated
                                if patch_exercise_set.id in patched_sets:
                                    # update the weight property of the set
                                    patch_exercise_set.weight = (
                                        exercise_set['weight'])
                                    # update the repetitions
                                    # property of the set
                                    patch_exercise_set.repetitions = (
                                        exercise_set['repetitions'])
                                    # update the rest
                                    # property of the set
                                    patch_exercise_set.rest = (
                                        exercise_set['rest'])
                                    # update the exercise
                                    # ID property of the set
                                    patch_exercise_set.exercise_id = (
                                        patch_exercise.id)
                                    # update the set instance
                                    # in the database
                                    patch_exercise_set.update()

    except Exception:
        # handle any exception from the database
        internal_error(err)
    finally:
        # check error status
        check_error(err)
        # send response
        return jsonify({
            "success": True,
            "edited_workout": workout.long()
        })
        # close database session
        db_close()


"""allow user to delete their own workouts in the database"""
@app.route('/workouts/<int:workout_id>', methods=['DELETE'])
@requires_auth(['delete:workouts'])
def delete_workouts(payload, workout_id):
    # set custom error object
    err = {
        "status": False,
        "code": None,
        "msg": None
    }

    # set variable to userID from payload
    user_id = payload['sub']

    try:
        # get the specified workout in the database
        workout = Workout.query.get(workout_id)
        # save a instance of the workout to send with the response
        _workout_ = workout.long()

        # if no workout is found send the user a 404 error
        if workout is None:
            err["status"] = True
            err["code"] = 404

        # make sure the user is authorized to delete this database
        if workout.user_id != user_id:
            err["status"] = True
            err["code"] = 403

        else:
            # if the workout was found loop throught workout exercises
            for exercise in workout.exercises:
                # query the database for the specified exercise
                delete_exercise = Exercise.query.get(exercise.id)

                # loop through each exercise set
                for exercise_set in delete_exercise.exercise_sets:
                    # query the database for the specified exercise set
                    delete_set = ExerciseSet.query.get(exercise_set.id)
                    # delete the exercise set instance in the database
                    delete_set.delete()
                # delete the exercise instance in the database
                delete_exercise.delete()

            # delete the workout instance in the database
            workout.delete()

    except Exception:
        # handle any exception from the database
        internal_error(err)
    finally:
        # check error status
        check_error(err)
        # send response
        return jsonify({
            "success": True,
            "deleted_workout": _workout_
        })
        # close database session
        db_close()


"""allow user to read any/all workouts in the database"""
@app.route('/trainer/workouts', methods=['GET'])
@requires_auth(['get:client_workouts'])
def get_workouts_as_trainer(payload):
    # set custom error object
    err = {
        "status": False,
        "code": None,
        "msg": None
    }

    try:
        # uery the database for all workout outs
        query = Workout.query.all()

        # if workouts are found in the database send a list of all the workouts
        if query is not None:
            workouts = [workout.long() for workout in query]

    except Exception:
        # handle any exception from the database
        internal_error(err)

    finally:
        # check error status
        check_error(err)
        # send response
        return jsonify({
            "success": True,
            "workouts": workouts
        })


"""allow user to read any/all specific workouts in the database by ID"""
@app.route('/trainer/workouts/<int:workout_id>', methods=['GET'])
@requires_auth(['get:client_workouts'])
def get_workout_by_id_as_trainer(payload, workout_id):
    # set custom error object
    err = {
        "status": False,
        "code": None,
        "msg": None
    }

    try:
        # query the database for the specified workout
        workout = Workout.query.get(workout_id)
        # if no workout is found in the database send the user a 404 error
        if workout is None:
            err['status'] = True
            err['code'] = 404

    except Exception:
        # handle any exception from the database
        internal_error(err)

    finally:
        # check error status
        check_error(err)
        # send response
        return jsonify({
            "success": True,
            "workout": workout.long()
        })


"""allow user to read any/all specific workouts in the database by ID"""
@app.route('/trainer/workouts-by-user/<string:user_id>', methods=['GET'])
@requires_auth(['get:client_workouts'])
def get_workout_by_user_id_as_trainer(payload, user_id):
    # set custom error object
    err = {
        "status": False,
        "code": None,
        "msg": None
    }

    try:
        # query the database for workouts with the specified user_id
        query = Workout.query.filter_by(user_id=user_id)
        # create a list of workouts to send in the response
        workouts = [workout.long() for workout in query]

    except Exception:
        # handle any exception from the database
        internal_error(err)

    finally:
        # check error status
        check_error(err)
        # send response
        return jsonify({
            "success": True,
            "workouts": workouts
        })


"""allow user to post any/all workouts to the database"""
@app.route('/trainer/workouts', methods=['POST'])
@requires_auth(['post:client_workouts'])
def post_workouts_as_trainer(payload):
    # set custom error object
    err = {
        "status": False,
        "code": None,
        "msg": None
    }

    try:

        # _workout_template_id_ = request.json.get('workout_template_id')
        # ensure name property is present
        if request.json.get('date') is None:
            err['status'] = True
            err['code'] = 400
            err['msg'] = 'Bad Request: No Date Property Found'
        # ensure name property is not blank
        elif request.json.get('date') is '':
            err['status'] = True
            err['code'] = 400
            err['msg'] = 'Bad Request: Date Property Cannot Be Blank'
        # ensure name property is a string
        elif type(request.json.get('date')) is not str:
            err['status'] = True
            err['code'] = 400
            err['msg'] = 'Bad Request: Date Property Must Be a String'
        else:

            # define a new workout instance
            new_workout = Workout(
                date=request.json.get('date'),
                user_id=request.json.get('user_id'),
                workout_template_id=request.json.get('workout_template_id')
            )
            # insert a new workout instance in the database
            new_workout.insert()
            # loop through the exercise list in request
            for exercise in request.json.get('exercises'):
                # define a workout exercise instance
                # for each worout exercise in the rquest
                new_exercise = Exercise(
                    exercise_template_id=exercise['exercise_template_id'],
                    workout_id=new_workout.id
                )
                # insert the workout exercise in the database
                new_exercise.insert()
                # loop through the sets in each exercise set
                for exercise_set in exercise['exercise_sets']:
                    # define a new exercise set instance in the database
                    new_exercise_set = ExerciseSet(
                        weight=exercise_set['weight'],
                        repetitions=exercise_set['repetitions'],
                        rest=exercise_set['rest'],
                        exercise_id=new_exercise.id
                    )
                    # insert the new exerise instance in the database
                    new_exercise_set.insert()

    except Exception:
        # handle any exception from the database
        internal_error(err)
    finally:
        # check error status
        check_error(err)
        # send response
        return jsonify({
            "success": True,
            "new_workout": new_workout.long()
        })


"""allow user to patch any/all workouts in the database"""
@app.route('/trainer/workouts/<int:workout_id>', methods=['PATCH'])
@requires_auth(['patch:client_workouts'])
def patch_workouts_as_trainer(payload, workout_id):
    # set custom error object
    err = {
        "status": False,
        "code": None,
        "msg": None
    }

    try:
        # query the database for the specified workout
        workout = Workout.query.get(workout_id)
        # make sure the user has access to the workout
        if workout is None:
            err['status'] = True
            err['code'] = 404

        else:
            # update the date property
            workout.date = request.json.get('date')
            # update the workout property remplate id
            workout.workout_template_id = request.json.get(
                'workout_template_id')
            # update the user_id property
            workout.user_id = request.json.get('user_id')
            # update the workout instance in the database
            workout.update()

            # create a list of exercise IDs
            # from the exercise list in the request
            patched_exercises = [exercise.get(
                'id') for exercise in request.json.get('exercises')]

            # loop through the exercise list loking for new exercises in the
            for exercise in request.json.get('exercises'):
                # if the workout exercise has  no ID then it is a new exercise
                if exercise.get('id') is None:
                    # define a new exercise instance
                    new_exercise = Exercise(
                        exercise_template_id=exercise['exercise_template_id'],
                        workout_id=workout.id
                    )
                    # insert the exercise instance into the database
                    new_exercise.insert()
                    # add the new exercise ID to the patched exercise list
                    patched_exercises.append(new_exercise.id)
                    # loop through the exercise sets in the
                    # exercise instance and add each one to the database
                    for exercise_set in exercise['exercise_sets']:
                        # define a new exercise set instance
                        new_set = ExerciseSet(
                            weight=exercise_set['weight'],
                            repetitions=exercise_set['repetitions'],
                            rest=exercise_set['rest'],
                            exercise_id=new_exercise.id
                        )
                        # insert the new exercise set into the database
                        new_set.insert()
                else:
                    # if the exercise has an ID query it in the database
                    patch_exercise = Exercise.query.get(exercise.get('id'))
                    # create a list of the exercise IDs
                    # on the original workout instance
                    oringial_exercise_ids = [a.id for a in workout.exercises]

                    # loop through the original exercise IDs
                    for exercise_id in oringial_exercise_ids:

                        # if the exercise ID is not in patched exercise
                        if exercise_id not in patched_exercises:
                            # query the database for the workout exercise
                            delete_exercise = Exercise.query.get(exercise_id)

                            # loop through the old exercise sets
                            delete_list = delete_exercise.exercise_sets
                            for old_exercise_set in delete_list:
                                # query the database for
                                # the specified exercise set
                                delete_exercise_set = ExerciseSet.query.get(
                                    old_exercise_set.id)
                                # delete the exercise set
                                # instance in the database
                                delete_exercise_set.delete()

                            # delete the exercise instance in the database
                            delete_exercise.delete()
                    # if the patched ID is in the patched exercise list
                    if patch_exercise.id in patched_exercises:
                        # update the exercise template ID propertyy
                        patch_exercise.exercise_template_id = (
                            exercise['exercise_template_id'])
                        # updated the exercise instance in the database
                        patch_exercise.update()
                        # create a list of exercise set IDs
                        patched_sets = [_exercise_set_.get(
                            'id') for _exercise_set_ in exercise.get(
                                'exercise_sets')]

                        # loop through exercise sets
                        for exercise_set in exercise.get('exercise_sets'):
                            # if the exercise set has
                            # no ID then it is a new exercise
                            if exercise_set.get('id') is None:
                                # define a new exercise set instance
                                new_exercise_set = ExerciseSet(
                                    weight=exercise_set['weight'],
                                    repetitions=exercise_set['repetitions'],
                                    rest=exercise_set['rest'],
                                    exercise_id=patch_exercise.id
                                )
                                # insert a new exercise set into the database
                                new_exercise_set.insert()

                            else:
                                # query sepcified exercise set in the database
                                patch_exercise_set = ExerciseSet.query.get(
                                    exercise_set.get('id'))
                                # create a list of exercise sets
                                # on the original workout exercise instance
                                original_exercise_sets = [
                                    a.id for a in patch_exercise.exercise_sets]
                                # loop through ids in the original
                                for set_id in original_exercise_sets:
                                    # if the exercise set ID
                                    # is not in patch sets
                                    if set_id not in patched_sets:
                                        # query the database for
                                        # the specified exercise set
                                        delete_set = ExerciseSet.query.get(
                                            set_id)
                                        # delete the exercise
                                        # set instance in the database
                                        delete_set.delete()
                                # if the exercise set ID is in patch sets
                                if patch_exercise_set.id in patched_sets:
                                    # update the weight property
                                    patch_exercise_set.weight = (
                                        exercise_set['weight'])
                                    # update the repetitions property
                                    patch_exercise_set.repetitions = (
                                        exercise_set['repetitions'])
                                    # update the rest property
                                    patch_exercise_set.rest = (
                                        exercise_set['rest'])
                                    # update the id property
                                    patch_exercise_set.exercise_id = (
                                        patch_exercise.id)
                                    # update the exercise
                                    # set instance in the database
                                    patch_exercise_set.update()

    except Exception:
        # handle any exception from the database
        internal_error(err)
    finally:
        # check error status
        check_error(err)
        # send response
        return jsonify({
            "success": True,
            "edited_workout": workout.long()
        })
        # close database session
        db_close()


"""allow user to delete any/all workouts in the database"""
@app.route('/trainer/workouts/<int:workout_id>', methods=['DELETE'])
@requires_auth(['delete:client_workouts'])
def delete_workouts_as_trainer(payload, workout_id):
    # set custom error object
    err = {
        "status": False,
        "code": None,
        "msg": None
    }

    try:
        # query the database for a workout with the specified ID
        workout = Workout.query.get(workout_id)
        # make sure the user has access to the workout
        if workout is None:
            err['status'] = True
            err['code'] = 404
        else:
            # save a copy of the instance
            _workout_ = workout.long()
            # loop through the exercise list
            for exercise in workout.exercises:
                # query the database for the specified workout exercise
                delete_exercise = Exercise.query.get(exercise.id)
                # loop through the exercise set list
                for exercise_set in delete_exercise.exercise_sets:
                    # query the database for the specified  exercise set
                    delete_set = ExerciseSet.query.get(exercise_set.id)
                    # delte the exrecise set instance in the database
                    delete_set.delete()
                # delete the exercise instance in the database
                delete_exercise.delete()
            # delete the workout instance in the database
            workout.delete()

    except Exception:
        # handle any exception from the database
        internal_error(err)
    finally:
        # check error status
        check_error(err)
        return jsonify({
            "success": True,
            "deleted_workout": _workout_
        })
        # close database session
        db_close()


"""allow user to read clients in the database"""
@app.route('/clients', methods=['GET'])
@requires_auth(['get:fitStat_clients'])
def get_clients(payload):
    # set custom error object
    err = {
        "status": False,
        "code": None,
        "msg": None
    }

    try:
        clients = get_fitStat_clients()
    except Exception:
        # handle any exception from the database
        internal_error(err)
    finally:
        # check error status
        check_error(err)
        # send response
        return jsonify({
            "success": True,
            "clients": clients
        })
        # close database session
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
