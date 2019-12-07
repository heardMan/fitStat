import os
import json
from sqlalchemy import Column, Boolean, String, Integer, DateTime, ForeignKey, LargeBinary
from flask_sqlalchemy import SQLAlchemy

#from settings import SQLALCHEMY_DATABASE_URI as database_path1
from settings import setup_environment

setup_environment()

TEST_CLIENT_USER_ID = os.getenv('TEST_CLIENT_USER_ID')
TEST_TRAINER_USER_ID = os.getenv('TEST_TRAINER_USER_ID')

'''Instantiate a sequel alchemy instance'''
db = SQLAlchemy()

#database path set as an environment variable
database_path = os.getenv("SQLALCHEMY_DATABASE_URI")
test_database_path = os.getenv("SQLALCHEMY_TEST_DATABASE_URI")

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.drop_all()
    db.create_all()

def db_rollback():
    db.session.rollback()

def db_close():
    db.session.close()

def seed_db():
    exercise_template_one = Exercise_Template(
        name='bench press',
        description='multi-joint chest workout'
    )
    exercise_template_one.insert()

    exercise_template_two = Exercise_Template(
        name='bent over row',
        description='multi-joint back workout'
    )
    exercise_template_two.insert()

    workout_template_one = Workout_Template(
        name='workout one',
        description='a good chest workout',
    )
    workout_template_one.insert()

    workout_template_one_exercise_one=  Workout_Exercise(
        recommended_sets=5,
        exercise_template_id=exercise_template_one.id,
        workout_template_id=workout_template_one.id
    )
    workout_template_one_exercise_one.insert()

    workout_template_one_exercise_two=  Workout_Exercise(
        recommended_sets=5,
        exercise_template_id=exercise_template_two.id,
        workout_template_id=workout_template_one.id
    )
    workout_template_one_exercise_two.insert()

    workout_one = Workout(
         date='March 5',
         user_id=TEST_TRAINER_USER_ID,
         workout_template_id=workout_template_one.id
    )
    workout_one.insert()

    workout_one_exercise_one = Exercise(
        exercise_template_id=exercise_template_one.id,
        workout_id=workout_one.id
    )
    workout_one_exercise_one.insert()

    workout_one_exercise_one_set_one = Exercise_Set(
        weight=15,
        repetitions=5,
        rest=30,
        exercise_id=workout_one_exercise_one.id
    )
    workout_one_exercise_one_set_one.insert()

    workout_one_exercise_one_set_two = Exercise_Set(
        weight=15,
        repetitions=6,
        rest=30,
        exercise_id=workout_one_exercise_one.id
    )
    workout_one_exercise_one_set_two.insert()

    workout_one_exercise_two = Exercise(
        exercise_template_id=exercise_template_two.id,
        workout_id=workout_one.id
    )
    workout_one_exercise_two.insert()

    workout_one_exercise_two_set_one =Exercise_Set(
        weight=150,
        repetitions=6,
        rest=60,
        exercise_id=workout_one_exercise_two.id
    )
    workout_one_exercise_two_set_one.insert()

    workout_one_exercise_two_set_two =Exercise_Set(
        weight=150,
        repetitions=5,
        rest=60,
        exercise_id=workout_one_exercise_two.id
    )
    workout_one_exercise_two_set_two.insert()




    workout_two = Workout(
         date='March 2',
         user_id=TEST_CLIENT_USER_ID,
         workout_template_id=workout_template_one.id
    )
    workout_two.insert()

    workout_two_exercise_one = Exercise(
        exercise_template_id=exercise_template_one.id,
        workout_id=workout_two.id
    )
    workout_two_exercise_one.insert()

    workout_two_exercise_one_set_one = Exercise_Set(
        weight=15,
        repetitions=5,
        rest=30,
        exercise_id=workout_two_exercise_one.id
    )
    workout_two_exercise_one_set_one.insert()

    workout_two_exercise_one_set_two = Exercise_Set(
        weight=15,
        repetitions=6,
        rest=30,
        exercise_id=workout_two_exercise_one.id
    )
    workout_two_exercise_one_set_two.insert()

    workout_two_exercise_two = Exercise(
        exercise_template_id=exercise_template_two.id,
        workout_id=workout_two.id
    )
    workout_two_exercise_two.insert()

    workout_two_exercise_two_set_one =Exercise_Set(
        weight=150,
        repetitions=6,
        rest=60,
        exercise_id=workout_two_exercise_two.id
    )
    workout_two_exercise_two_set_one.insert()

    workout_two_exercise_two_set_two =Exercise_Set(
        weight=150,
        repetitions=5,
        rest=60,
        exercise_id=workout_two_exercise_two.id
    )
    workout_two_exercise_two_set_two.insert()



    workout_three = Workout(
         date='March 2',
         user_id=TEST_CLIENT_USER_ID,
         workout_template_id=workout_template_one.id
    )
    workout_three.insert()

    workout_three_exercise_one = Exercise(
        exercise_template_id=exercise_template_one.id,
        workout_id=workout_three.id
    )
    workout_three_exercise_one.insert()

    workout_three_exercise_one_set_one = Exercise_Set(
        weight=15,
        repetitions=5,
        rest=30,
        exercise_id=workout_three_exercise_one.id
    )
    workout_three_exercise_one_set_one.insert()

    workout_three_exercise_one_set_two = Exercise_Set(
        weight=15,
        repetitions=6,
        rest=30,
        exercise_id=workout_three_exercise_one.id
    )
    workout_three_exercise_one_set_two.insert()

    workout_three_exercise_two = Exercise(
        exercise_template_id=exercise_template_one.id,
        workout_id=workout_three.id
    )
    workout_three_exercise_two.insert()

    workout_three_exercise_two_set_one =Exercise_Set(
        weight=150,
        repetitions=6,
        rest=60,
        exercise_id=workout_three_exercise_two.id
    )
    workout_three_exercise_two_set_one.insert()

    workout_three_exercise_two_set_two =Exercise_Set(
        weight=150,
        repetitions=5,
        rest=60,
        exercise_id=workout_three_exercise_two.id
    )
    workout_three_exercise_two_set_two.insert()




    workout_four = Workout(
         date='March 2',
         user_id=TEST_TRAINER_USER_ID,
         workout_template_id=workout_template_one.id
    )
    workout_four.insert()

    workout_four_exercise_one = Exercise(
        exercise_template_id=exercise_template_one.id,
        workout_id=workout_four.id
    )
    workout_four_exercise_one.insert()

    workout_four_exercise_one_set_one = Exercise_Set(
        weight=15,
        repetitions=5,
        rest=30,
        exercise_id=workout_four_exercise_one.id
    )
    workout_four_exercise_one_set_one.insert()

    workout_four_exercise_one_set_two = Exercise_Set(
        weight=15,
        repetitions=6,
        rest=30,
        exercise_id=workout_four_exercise_one.id
    )
    workout_four_exercise_one_set_two.insert()

    workout_four_exercise_two = Exercise(
        exercise_template_id=exercise_template_one.id,
        workout_id=workout_four.id
    )
    workout_four_exercise_two.insert()

    workout_four_exercise_two_set_one =Exercise_Set(
        weight=150,
        repetitions=6,
        rest=60,
        exercise_id=workout_four_exercise_two.id
    )
    workout_four_exercise_two_set_one.insert()

    workout_four_exercise_two_set_two =Exercise_Set(
        weight=150,
        repetitions=5,
        rest=60,
        exercise_id=workout_four_exercise_two.id
    )
    workout_four_exercise_two_set_two.insert()




'''
EXERCISE TEMPLATE MODEL
'''

class Exercise_Template(db.Model):

    __tablename__ = 'Exercise_Template'

    '''Model Definition'''

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    archived = Column(Boolean)

    '''Init Method'''

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.archived = False


    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def long(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
    
'''
WORKOUT TEMPLATE MODEL
'''

class Workout_Template(db.Model):

    __tablename__ = 'Workout_Template'

    '''Model Definition'''

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    archived = Column(Boolean)
    exercises = db.relationship('Workout_Exercise', backref='Workout_Template')
    

    '''Init Method'''

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.archived = False
       
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def long(self):
        exercises = [exercise.long() for exercise in self.exercises]
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'exercises': exercises
        }

'''
WORKOUT EXERCISE MODEL
'''
#workout template exercise

class Workout_Exercise(db.Model):

    __tablename__ = 'Workout_Exercise'

    '''Model Definition'''

    id = Column(Integer, primary_key=True)
    recommended_sets = Column(Integer)
    exercise_template_id = Column(Integer, ForeignKey('Exercise_Template.id'))
    workout_template_id = Column(Integer, ForeignKey('Workout_Template.id'))

    '''Init Method'''

    def __init__(self, recommended_sets, exercise_template_id, workout_template_id):
        self.recommended_sets = recommended_sets
        self.exercise_template_id = exercise_template_id
        self.workout_template_id = workout_template_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def long(self):
        return {
            'id': self.id,
            'recommended_sets': self.recommended_sets,
            'exercise_template_id': self.exercise_template_id,
            'workout_template_id': self.workout_template_id
        }

'''
USER WORKOUT MODEL
'''

class Workout(db.Model):

    __tablename__ = 'Workout'

    '''Model Definition'''

    id = Column(Integer, primary_key=True)
    date = Column(String)
    #date = Column(DateTime(timezone=False), nullable=False)
    exercises = db.relationship('Exercise', backref='Workout')
    user_id = Column(String)
    workout_template_id = Column(Integer, ForeignKey('Workout_Template.id'))

    '''Init Method'''

    def __init__(self, date, user_id, workout_template_id):
        self.date = date
        self.user_id = user_id
        self.workout_template_id = workout_template_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def long(self):
        return {
            'id': self.id,
            'date': self.date,
            'exercises': [exercise.long() for exercise in self.exercises],
            'user_id': self.user_id,
            'workout_template_id': self.workout_template_id
        }

'''
USER EXERCISE MODEL
    This model is used to map user work outs to predefined exercises
    these work out instances are also mapped to a recorded number of sets
    in a one to many relationship
    (one UserExercise maps to many Sets)
'''

class Exercise(db.Model):

    __tablename__ = 'Exercise'

    '''Model Definition'''

    id = Column(Integer, primary_key=True)
    exercise_template_id = Column(Integer, ForeignKey('Exercise_Template.id'))
    workout_id = Column(Integer, ForeignKey('Workout.id'))
    exercise_sets = db.relationship('Exercise_Set', backref='Exercise')

    '''Init Method'''

    def __init__(self, exercise_template_id, workout_id):
        self.exercise_template_id = exercise_template_id
        self.workout_id = workout_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def long(self):
        return {
            'id': self.id,
            'exercise_template_id': self.exercise_template_id,
            'workout_id': self.workout_id,
            'exercise_sets': [exercise_set.long() for exercise_set in self.exercise_sets]
        }

'''
SET MODEL
    This model is for an exercise set and is designed to
    track weight, repetitions, rest, etc.
    This model has a many to one relationship with the UserExercise Model
    (Many Sets map to One User Exercise)
'''

class Exercise_Set(db.Model):

    __tablename__ = 'Exercise_Set'

    '''Model Definition'''

    id = Column(Integer, primary_key=True)
    weight = Column(Integer)
    repetitions = Column(Integer)
    rest = Column(Integer)
    exercise_id = Column(Integer, ForeignKey('Exercise.id'))

    '''Init Method'''

    def __init__(self, weight, repetitions, rest, exercise_id,):
        self.weight = weight
        self.repetitions = repetitions
        self.rest = rest
        self.exercise_id = exercise_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def long(self):
        return {
            'id': self.id,
            'weight': self.weight,
            'repetitions': self.repetitions,
            'rest': self.rest,
            'exercise_id': self.exercise_id
        }