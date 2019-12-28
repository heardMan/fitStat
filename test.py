import os
import json
import unittest
import http.client
from app import app
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, seed_db, test_database_path, Exercise_Template, Workout_Template

TEST_CLIENT_TOKEN = os.getenv("TEST_CLIENT_TOKEN")
TEST_TRAINER_TOKEN = os.getenv("TEST_TRAINER_TOKEN")
TEST_CLIENT_USER_ID = os.getenv("TEST_CLIENT_USER_ID")
TEST_TRAINER_USER_ID = os.getenv("TEST_TRAINER_USER_ID")


class APITestCase(unittest.TestCase):
    """This class represents the trivia test case"""
    @classmethod
    def setUpClass(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.database_name = "test_fitStat"
        self.database_path = 'postgresql://mark@localhost:5432/test_fitStat'
        setup_db(self.app, 'postgresql://mark@localhost:5432/test_fitStat')

        # print(token)
        self.client_headers = {
            'Authorization': 'Bearer {}'.format(TEST_CLIENT_TOKEN)
        }
        self.trainer_headers = {
            'Authorization': 'Bearer {}'.format(TEST_TRAINER_TOKEN)
        }

        # binds the app to the current context
        # with self.app.app_context():
        #     self.db = SQLAlchemy()
        #     self.db.init_app(self.app)
            # create all tables
            #self.db.create_all()
            

    

    def test_get_exercise_templates(self):
        """Test the get exercise templates route"""
        

        """Test Authentication"""

        unauthenticated_get = self.client().get('/exercise_templates')
        unauthenticated_get_data = unauthenticated_get.json

        self.assertEqual(unauthenticated_get.status_code, 401)
        self.assertEqual(unauthenticated_get_data['success'], False)

        """Test Client Functionality"""

        client_get = self.client().get('/exercise_templates', headers=self.client_headers)
        client_data = client_get.json

        self.assertEqual(client_get.status_code, 200)
        self.assertEqual(client_data['success'], True)

        self.assertGreater(len(client_data['exercises']), 0)

        """Test Trainer Functionality"""

        trainer_get = self.client().get('/exercise_templates', headers=self.trainer_headers)
        trainer_data = trainer_get.json

        self.assertEqual(trainer_get.status_code, 200)
        self.assertEqual(trainer_data['success'], True)

        self.assertGreater(len(trainer_data['exercises']), 0)

    def test_get_exercise_templates_by_id(self):
        """Test the get exercise templates by id route"""

        """Test Authentication"""

        unauthenticated_get = self.client().get('/exercise_templates/1')
        unauthenticated_get_data = unauthenticated_get.json

        self.assertEqual(unauthenticated_get.status_code, 401)
        self.assertEqual(unauthenticated_get_data['success'], False)

        """Test Client Functionality"""

        client_get = self.client().get('/exercise_templates/1', headers=self.client_headers)
        client_data = client_get.json

        self.assertEqual(client_get.status_code, 200)
        self.assertEqual(client_data['success'], True)

        self.assertGreater(len(client_data['exercise']), 0)

        """Test Trainer Functionality"""

        trainer_get = self.client().get('/exercise_templates/1',
                                        headers=self.trainer_headers)
        trainer_data = trainer_get.json

        self.assertEqual(trainer_get.status_code, 200)
        self.assertEqual(trainer_data['success'], True)

        self.assertGreater(len(trainer_data['exercise']), 0)

    def test_post_exercise_templates(self):
        """Test the post exercise templates route"""

        test_exercise = {
            "name": "test_exercise",
            "description": "test_description"
        }

        """Test Authentication"""

        unauthenticated_post = self.client().post(
            '/exercise_templates', json=test_exercise)
        unauthenticated_post_data = unauthenticated_post.json

        self.assertEqual(unauthenticated_post.status_code, 401)
        self.assertEqual(unauthenticated_post_data['success'], False)

        """Test Client Functionality"""

        client_post = self.client().post('/exercise_templates',
                                         json=test_exercise, headers=self.client_headers)
        client_data = client_post.json

        self.assertEqual(client_post.status_code, 403)
        self.assertEqual(client_data['success'], False)

        """Test Trainer Functionality"""

        trainer_post = self.client().post('/exercise_templates',
                                          json=test_exercise, headers=self.trainer_headers)
        trainer_data = trainer_post.json

        self.assertEqual(trainer_post.status_code, 200)
        self.assertEqual(trainer_data['success'], True)

        self.assertGreater(len(trainer_data['new_exercise']), 0)

    def test_patch_exercise_templates(self):
        """Test the patch exercise templates by id route"""

        test_patch = {
            "name": "test_exercise_patch",
            "description": "test_patch_description"
        }

        """Test Authentication"""

        unauthenticated_patch = self.client().patch(
            '/exercise_templates/1', json=test_patch)
        unauthenticated_patch_data = unauthenticated_patch.json

        self.assertEqual(unauthenticated_patch.status_code, 401)
        self.assertEqual(unauthenticated_patch_data['success'], False)

        """Test Client Functionality"""

        client_patch = self.client().patch('/exercise_templates/1',
                                           json=test_patch, headers=self.client_headers)
        client_data = client_patch.json

        self.assertEqual(client_patch.status_code, 403)
        self.assertEqual(client_data['success'], False)

        """Test Trainer Functionality"""

        trainer_patch = self.client().patch('/exercise_templates/1',
                                            json=test_patch, headers=self.trainer_headers)
        trainer_data = trainer_patch.json

        self.assertEqual(trainer_patch.status_code, 200)
        self.assertEqual(trainer_data['success'], True)

        self.assertGreater(len(trainer_data['edited_exercise']), 0)

    def test_delete_exercise_templates(self):
        """Test the delete exercise templates by id route"""

        """Test Authentication"""

        unauthenticated_delete = self.client().delete('/exercise_templates/1')
        unauthenticated_delete_data = unauthenticated_delete.json

        self.assertEqual(unauthenticated_delete.status_code, 401)
        self.assertEqual(unauthenticated_delete_data['success'], False)

        """Test Client Functionality"""

        client_delete = self.client().delete(
            '/exercise_templates/3', headers=self.client_headers)
        client_data = client_delete.json

        self.assertEqual(client_delete.status_code, 403)
        self.assertEqual(client_data['success'], False)

        """Test Trainer Functionality"""

        trainer_delete = self.client().delete(
            '/exercise_templates/3', headers=self.trainer_headers)
        trainer_data = trainer_delete.json

        self.assertEqual(trainer_delete.status_code, 200)
        self.assertEqual(trainer_data['success'], True)

        self.assertGreater(len(trainer_data['deleted_exercise']), 0)

    def test_get_workout_templates(self):
        """Test the get workout templates route"""

        """Test Authentication"""

        unauthenticated_get = self.client().get('/workout_templates')
        unauthenticated_get_data = unauthenticated_get.json

        self.assertEqual(unauthenticated_get.status_code, 401)
        self.assertEqual(unauthenticated_get_data['success'], False)

        """Test Client Functionality"""

        client_get = self.client().get('/workout_templates', headers=self.client_headers)
        client_data = client_get.json

        self.assertEqual(client_get.status_code, 200)
        self.assertEqual(client_data['success'], True)
        self.assertGreater(len(client_data['workouts']), 0)

        """Test Trainer Functionality"""

        trainer_get = self.client().get('/workout_templates', headers=self.trainer_headers)
        trainer_data = trainer_get.json

        self.assertEqual(trainer_get.status_code, 200)
        self.assertEqual(trainer_data['success'], True)

        self.assertGreater(len(trainer_data['workouts']), 0)

    def test_get_workout_templates_by_id(self):
        """Test the get workout templates by ID route"""

        """Test Authentication"""

        unauthenticated_get = self.client().get('/workout_templates/1')
        unauthenticated_get_data = unauthenticated_get.json

        self.assertEqual(unauthenticated_get.status_code, 401)
        self.assertEqual(unauthenticated_get_data['success'], False)

        """Test Client Functionality"""

        client_get = self.client().get('/workout_templates/1', headers=self.client_headers)
        client_data = client_get.json

        self.assertEqual(client_get.status_code, 200)
        self.assertEqual(client_data['success'], True)
        self.assertGreater(len(client_data['workouts']), 0)

        """Test Trainer Functionality"""

        trainer_get = self.client().get('/workout_templates/1',
                                        headers=self.trainer_headers)
        trainer_data = trainer_get.json

        self.assertEqual(trainer_get.status_code, 200)
        self.assertEqual(trainer_data['success'], True)

        self.assertGreater(len(trainer_data['workouts']), 0)

    def test_post_workout_templates(self):
        """Test the post workout templates route"""

        test_workout = {
            "description": "test workout",
            "exercises": [
                {
                    "exercise_template_id": 2,
                    "recommended_sets": 5
                },
                {
                    "exercise_template_id": 2,
                    "recommended_sets": 5
                }
            ],
            "name": "test workout"
        }

        """Test Authentication"""

        unauthenticated_post = self.client().post(
            '/exercise_templates', json=test_workout)
        unauthenticated_post_data = unauthenticated_post.json

        self.assertEqual(unauthenticated_post.status_code, 401)
        self.assertEqual(unauthenticated_post_data['success'], False)

        """Test Client Functionality"""

        client_post = self.client().post('/workout_templates',
                                         json=test_workout, headers=self.client_headers)
        client_data = client_post.json

        self.assertEqual(client_post.status_code, 403)
        self.assertEqual(client_data['success'], False)

        """Test Trainer Functionality"""

        trainer_post = self.client().post('/workout_templates', json=test_workout,
                                          headers=self.trainer_headers)
        trainer_data = trainer_post.json

        self.assertEqual(trainer_post.status_code, 200)
        self.assertEqual(trainer_data['success'], True)

        self.assertGreater(len(trainer_data['new_workout']), 0)

    def test_patch_workout_templates(self):
        """Test the patch workout templates by id route"""

        test_patch = {
            "description": "a good chest workout",
            "exercises": [
                {
                    "exercise_template_id": 1,
                    "id": 1,
                    "recommended_sets": 5,
                    "workout_template_id": 1
                },
                {
                    "exercise_template_id": 2,
                    "id": 2,
                    "recommended_sets": 5,
                    "workout_template_id": 1
                },
                {
                    "exercise_template_id": 2,
                    "recommended_sets": 20
                }
            ],
            "id": 1,
            "name": "workout one"
        }

        """Test Authentication"""

        unauthenticated_patch = self.client().patch(
            '/exercise_templates/1', json=test_patch)
        unauthenticated_patch_data = unauthenticated_patch.json

        self.assertEqual(unauthenticated_patch.status_code, 401)
        self.assertEqual(unauthenticated_patch_data['success'], False)

        """Test Client Functionality"""

        client_patch = self.client().patch('/workout_templates/1',
                                           json=test_patch, headers=self.client_headers)
        client_data = client_patch.json

        self.assertEqual(client_patch.status_code, 403)
        self.assertEqual(client_data['success'], False)

        """Test Trainer Functionality"""

        trainer_patch = self.client().patch('/workout_templates/1',
                                            json=test_patch, headers=self.trainer_headers)
        trainer_data = trainer_patch.json

        self.assertEqual(trainer_patch.status_code, 200)
        self.assertEqual(trainer_data['success'], True)

        self.assertGreater(len(trainer_data['edited_workout']), 0)

    def test_delete_workout_templates(self):
        """Test the delete workout templates by id route"""

        """Test Authentication"""

        unauthenticated_delete = self.client().delete('/workout_templates/3')
        unauthenticated_delete_data = unauthenticated_delete.json

        self.assertEqual(unauthenticated_delete.status_code, 401)
        self.assertEqual(unauthenticated_delete_data['success'], False)

        """Test Client Functionality"""

        client_delete = self.client().delete(
            '/workout_templates/3', headers=self.client_headers)
        client_data = client_delete.json

        self.assertEqual(client_delete.status_code, 403)
        self.assertEqual(client_data['success'], False)

        """Test Trainer Functionality"""

        trainer_delete = self.client().delete(
            '/workout_templates/3', headers=self.trainer_headers)
        trainer_data = trainer_delete.json

        self.assertEqual(trainer_delete.status_code, 200)
        self.assertEqual(trainer_data['success'], True)

        self.assertGreater(len(trainer_data['deleted_workout']), 0)

    def test_get_workouts(self):
        """Test the get own workouts route"""

        """Test Authentication"""

        unauthenticated_get = self.client().get('/workouts')
        unauthenticated_get_data = unauthenticated_get.json

        self.assertEqual(unauthenticated_get.status_code, 401)
        self.assertEqual(unauthenticated_get_data['success'], False)

        """Test Client Functionality"""

        client_get = self.client().get('/workouts', headers=self.client_headers)
        client_data = client_get.json

        self.assertEqual(client_get.status_code, 200)
        self.assertEqual(client_data['success'], True)
        self.assertGreater(len(client_data['workouts']), 0)

        """Test Trainer Functionality"""

        trainer_get = self.client().get('/workouts', headers=self.trainer_headers)
        trainer_data = trainer_get.json

        self.assertEqual(trainer_get.status_code, 200)
        self.assertEqual(trainer_data['success'], True)

        self.assertGreater(len(trainer_data['workouts']), 0)

    def test_get_workouts_by_id(self):
        """Test the get own workouts by ID route"""

        """Test Authentication"""

        unauthenticated_get = self.client().get('/workouts/2')
        unauthenticated_get_data = unauthenticated_get.json

        self.assertEqual(unauthenticated_get.status_code, 401)
        self.assertEqual(unauthenticated_get_data['success'], False)

        """Test Client Functionality"""

        client_get = self.client().get('/workouts/7', headers=self.client_headers)
        client_data = client_get.json

        self.assertEqual(client_get.status_code, 200)
        self.assertEqual(client_data['success'], True)
        self.assertGreater(len(client_data['workout']), 0)

        """Test Trainer Functionality"""

        trainer_get = self.client().get('/workouts/2', headers=self.trainer_headers)
        trainer_data = trainer_get.json

        self.assertEqual(trainer_get.status_code, 200)
        self.assertEqual(trainer_data['success'], True)

        self.assertGreater(len(trainer_data['workout']), 0)

    def test_post_workouts(self):
        """Test the post own workout route"""

        test_workout = {
            "date": "Mar 5",
            "workout_template_id": 1,
            "exercises": [
                {
                    "exercise_template_id": 1,
                    "exercise_sets": [
                        {
                            "repetitions": 5,
                            "rest": 30,
                            "weight": 15
                        },
                        {
                            "repetitions": 5,
                            "rest": 30,
                            "weight": 15
                        }
                    ]
                },
                {
                    "exercise_template_id": 2,
                    "exercise_sets": [
                        {
                            "repetitions": 6,
                            "rest": 55,
                            "weight": 125
                        },
                        {
                            "repetitions": 7,
                            "rest": 65,
                            "weight": 125
                        }
                    ]
                }
            ]
        }

        """Test Authentication"""

        unauthenticated_post = self.client().post(
            '/workouts', json=test_workout)
        unauthenticated_post_data = unauthenticated_post.json

        self.assertEqual(unauthenticated_post.status_code, 401)
        self.assertEqual(unauthenticated_post_data['success'], False)

        """Test Client Functionality"""

        client_post = self.client().post('/workouts',
                                         json=test_workout, headers=self.client_headers)
        client_data = client_post.json
        self.assertEqual(client_post.status_code, 200)
        self.assertEqual(client_data['success'], True)
        self.assertGreater(len(client_data['new_workout']), 0)

        """Test Trainer Functionality"""

        trainer_post = self.client().post('/workouts', json=test_workout,
                                          headers=self.trainer_headers)
        trainer_data = trainer_post.json

        self.assertEqual(trainer_post.status_code, 200)
        self.assertEqual(trainer_data['success'], True)

        self.assertGreater(len(trainer_data['new_workout']), 0)

    def test_patch_workouts(self):
        """Test the patch own workouts by id route"""

        test_patch = {
            "date": "Mar 5",
            "workout_template_id": 1,
            "exercises": [
                {
                    "exercise_template_id": 1,
                    "exercise_sets": [
                        {
                            "repetitions": 5,
                            "rest": 30,
                            "weight": 15
                        },
                        {
                            "repetitions": 5,
                            "rest": 30,
                            "weight": 15
                        }
                    ]
                },
                {
                    "exercise_template_id": 2,
                    "exercise_sets": [
                        {
                            "repetitions": 6,
                            "rest": 55,
                            "weight": 125
                        },
                        {
                            "repetitions": 7,
                            "rest": 65,
                            "weight": 125
                        }
                    ]
                }
            ]
        }

        """Test Authentication"""

        unauthenticated_patch = self.client().patch('/workouts/1', json=test_patch)
        unauthenticated_patch_data = unauthenticated_patch.json

        self.assertEqual(unauthenticated_patch.status_code, 401)
        self.assertEqual(unauthenticated_patch_data['success'], False)

        """Test Client Functionality"""
        # test the unauthorized /drinks route
        client_patch = self.client().patch('/workouts/7',
                                           json=test_patch, headers=self.client_headers)
        client_data = client_patch.json
        # ensure request was good
        self.assertEqual(client_patch.status_code, 200)
        self.assertEqual(client_data['success'], True)
        # ensure we have at least one exercise
        self.assertGreater(len(client_data['edited_workout']), 0)

        """Test Trainer Functionality"""
        # test the unauthorized /drinks route
        trainer_patch = self.client().patch(
            '/workouts/7', json=test_patch, headers=self.trainer_headers)
        trainer_data = trainer_patch.json

        # ensure request was good
        self.assertEqual(trainer_patch.status_code, 403)
        self.assertEqual(trainer_data['success'], False)

    # def test_delete_workouts(self):

    def test_delete_workouts(self):
        """Test the delete own workouts by id route"""

        """Test Authentication"""

        unauthenticated_delete = self.client().delete('/workouts/2')
        unauthenticated_delete_data = unauthenticated_delete.json

        self.assertEqual(unauthenticated_delete.status_code, 401)
        self.assertEqual(unauthenticated_delete_data['success'], False)

        """Test Trainer Functionality"""
        # test the unauthorized /drinks route
        trainer_delete = self.client().delete('workouts/6', headers=self.trainer_headers)
        trainer_data = trainer_delete.json
        # ensure request was good
        self.assertEqual(trainer_delete.status_code, 403)
        self.assertEqual(trainer_data['success'], False)

        """Test Client Functionality"""
        # test the unauthorized /drinks route
        client_delete = self.client().delete('/workouts/10', headers=self.client_headers)
        client_data = client_delete.json
        # ensure request was good
        self.assertEqual(client_delete.status_code, 200)
        self.assertEqual(client_data['success'], True)
        # ensure we have at least one exercise
        self.assertGreater(len(client_data['deleted_workout']), 0)

    # def test_get_workouts_as_trainer(self):

    def test_get_workouts_as_trainer(self):
        """Test the get workouts as trainer route"""

        """Test Authentication"""

        unauthenticated_get = self.client().get('/trainer/workouts')
        unauthenticated_get_data = unauthenticated_get.json

        self.assertEqual(unauthenticated_get.status_code, 401)
        self.assertEqual(unauthenticated_get_data['success'], False)

        """Test Client Functionality"""
        # test the unauthorized /drinks route
        client_get = self.client().get('/trainer/workouts', headers=self.client_headers)
        client_data = client_get.json
        # ensure request was good
        self.assertEqual(client_get.status_code, 403)
        self.assertEqual(client_data['success'], False)

        """Test Trainer Functionality"""
        # test the unauthorized /drinks route
        trainer_get = self.client().get('/trainer/workouts', headers=self.trainer_headers)
        trainer_data = trainer_get.json
        # ensure request was good
        self.assertEqual(trainer_get.status_code, 200)
        self.assertEqual(trainer_data['success'], True)
        # ensure we have at least one exercise
        self.assertGreater(len(trainer_data['workouts']), 0)

    # # def test_get_workouts_by_id_as_trainer(self):
    def test_get_workouts_by_id_as_trainer(self):
        """Test the get workouts by ID as trainer route"""

        """Test Authentication"""

        unauthenticated_get = self.client().get('/trainer/workouts/1')
        unauthenticated_get_data = unauthenticated_get.json

        self.assertEqual(unauthenticated_get.status_code, 401)
        self.assertEqual(unauthenticated_get_data['success'], False)

        """Test Client Functionality"""
        # test the unauthorized /drinks route
        client_get = self.client().get('/trainer/workouts/1', headers=self.client_headers)
        client_data = client_get.json
        # ensure request was good
        self.assertEqual(client_get.status_code, 403)
        self.assertEqual(client_data['success'], False)

        """Test Trainer Functionality"""
        # test the unauthorized /drinks route
        trainer_get = self.client().get('/trainer/workouts/1', headers=self.trainer_headers)
        trainer_data = trainer_get.json
        # ensure request was good
        self.assertEqual(trainer_get.status_code, 200)
        self.assertEqual(trainer_data['success'], True)
        # ensure we have at least one exercise
        self.assertGreater(len(trainer_data['workout']), 0)

    # # def test_get_workouts_by_user_id_as_trainer(self):
    def test_get_workouts_by_user_id_as_trainer(self):
        """Test the get workouts by user id as trainer route"""

        """Test Authentication"""

        unauthenticated_get = self.client().get(
            '/trainer/workouts-by-user/{}'.format(TEST_CLIENT_USER_ID))
        unauthenticated_get_data = unauthenticated_get.json

        self.assertEqual(unauthenticated_get.status_code, 401)
        self.assertEqual(unauthenticated_get_data['success'], False)

        """Test Client Functionality"""
        # test the unauthorized /drinks route
        client_get = self.client().get(
            '/trainer/workouts-by-user/{}'.format(TEST_CLIENT_USER_ID), headers=self.client_headers)
        client_data = client_get.json
        # ensure request was good
        self.assertEqual(client_get.status_code, 403)
        self.assertEqual(client_data['success'], False)

        """Test Trainer Functionality"""
        # test the unauthorized /drinks route
        trainer_get = self.client().get(
            '/trainer/workouts-by-user/{}'.format(TEST_CLIENT_USER_ID), headers=self.trainer_headers)
        trainer_data = trainer_get.json
        # ensure request was good
        self.assertEqual(trainer_get.status_code, 200)
        self.assertEqual(trainer_data['success'], True)
        # ensure we have at least one exercise
        self.assertGreater(len(trainer_data['workouts']), 0)

    # # def test_post_workouts_as_trainer(self):
    def test_post_workouts_as_trainer_templates(self):
        """Test the post workout as trainer route"""

        test_workout = {
            "date": "Mar 5",
            "workout_template_id": 1,
            "user_id": "auth0|5dd9ed38a40c120ed15c6277",
            "exercises": [
                {
                    "exercise_template_id": 1,
                    "exercise_sets": [
                        {
                            "repetitions": 5,
                            "rest": 30,
                            "weight": 15
                        },
                        {
                            "repetitions": 5,
                            "rest": 30,
                            "weight": 15
                        }
                    ]
                },
                {
                    "exercise_template_id": 2,
                    "exercise_sets": [
                        {
                            "repetitions": 6,
                            "rest": 55,
                            "weight": 125
                        },
                        {
                            "repetitions": 7,
                            "rest": 65,
                            "weight": 125
                        }
                    ]
                }
            ]
        }

        """Test Authentication"""

        unauthenticated_post = self.client().post(
            '/trainer/workouts', json=test_workout)
        unauthenticated_post_data = unauthenticated_post.json

        self.assertEqual(unauthenticated_post.status_code, 401)
        self.assertEqual(unauthenticated_post_data['success'], False)

        """Test Client Functionality"""
        # test the unauthorized /drinks route
        client_post = self.client().post('/trainer/workouts', json=test_workout,
                                         headers=self.client_headers)
        client_data = client_post.json
        # ensure request was good
        self.assertEqual(client_post.status_code, 403)
        self.assertEqual(client_data['success'], False)

        """Test Trainer Functionality"""
        # test the unauthorized /drinks route
        trainer_post = self.client().post('/trainer/workouts', json=test_workout,
                                          headers=self.trainer_headers)
        trainer_data = trainer_post.json
        #print('TRAINER_DATA: {}'.format(trainer_data))
        # ensure request was good
        self.assertEqual(trainer_post.status_code, 200)
        self.assertEqual(trainer_data['success'], True)
        # ensure we have at least one exercise
        self.assertGreater(len(trainer_data['new_workout']), 0)

    # # def test_patch_workouts_as_trainer(self):
    def test_patch_workouts_as_trainer(self):
        """Test the patch workouts by id route"""

        test_patch = {
            "date": "March 6",
            "exercises": [
                {
                    "exercise_sets": [
                        {
                            "exercise_id": 1,
                            "id": 1,
                            "repetitions": 5,
                            "rest": 30,
                            "weight": 15
                        },
                        {
                            "repetitions": 234,
                            "rest": 234,
                            "weight": 234
                        }
                    ],
                    "exercise_template_id": 1,
                    "id": 1,
                    "workout_id": 1
                },
                {
                    "exercise_template_id": 1,
                    "exercise_sets": [
                        {
                            "repetitions": 123,
                            "rest": 123,
                            "weight": 123
                        }
                    ]

                }
            ],
            "id": 1,
            "user_id": "5dd9ed38a40c120ed15c6277",
            "workout_template_id": 1
        }

        """Test Authentication"""

        unauthenticated_patch = self.client().patch(
            '/trainer/workouts/5', json=test_patch)
        unauthenticated_patch_data = unauthenticated_patch.json

        self.assertEqual(unauthenticated_patch.status_code, 401)
        self.assertEqual(unauthenticated_patch_data['success'], False)

        """Test Client Functionality"""
        # test the unauthorized /drinks route
        client_patch = self.client().patch('/trainer/workouts/2',
                                           json=test_patch, headers=self.client_headers)
        client_data = client_patch.json
        # ensure request was good
        self.assertEqual(client_patch.status_code, 403)
        self.assertEqual(client_data['success'], False)

        """Test Trainer Functionality"""
        # test the unauthorized /drinks route
        trainer_patch = self.client().patch('/trainer/workouts/2',
                                            json=test_patch, headers=self.trainer_headers)
        trainer_data = trainer_patch.json

        # ensure request was good
        self.assertEqual(trainer_patch.status_code, 200)
        self.assertEqual(trainer_data['success'], True)
        # ensure we have at least one exercise
        self.assertGreater(len(trainer_data['edited_workout']), 0)

    # def test_delete_workouts_as_trainer(self):
    def test_delete_workouts_as_trainer(self):
        """Test the delete workouts as trainer by id route"""

        """Test Authentication"""

        unauthenticated_delete = self.client().delete('/trainer/workouts/3')
        unauthenticated_delete_data = unauthenticated_delete.json

        self.assertEqual(unauthenticated_delete.status_code, 401)
        self.assertEqual(unauthenticated_delete_data['success'], False)

        """Test Client Functionality"""
        # test the unauthorized /drinks route
        client_delete = self.client().delete(
            '/trainer/workouts/3', headers=self.client_headers)
        client_data = client_delete.json
        # ensure request was good
        self.assertEqual(client_delete.status_code, 403)
        self.assertEqual(client_data['success'], False)

        """Test Trainer Functionality"""
        # test the unauthorized /drinks route
        trainer_delete = self.client().delete(
            '/trainer/workouts/4', headers=self.trainer_headers)
        trainer_data = trainer_delete.json
        # ensure request was good
        self.assertEqual(trainer_delete.status_code, 200)
        self.assertEqual(trainer_data['success'], True)
        # ensure we have at least one exercise
        self.assertGreater(len(trainer_data['deleted_workout']), 0)

    # def test_get_clients(self):
    def test_get_clients(self):
        """Test the get clients route"""

        """Test Authentication"""
        unauthenticated_get = self.client().get('/clients')
        unauthenticated_get_data = unauthenticated_get.json

        self.assertEqual(unauthenticated_get.status_code, 401)
        self.assertEqual(unauthenticated_get_data['success'], False)

        """Test Client Functionality"""
        # test the unauthorized /drinks route
        client_get = self.client().get('/clients', headers=self.client_headers)
        client_data = client_get.json
        # ensure request was good
        self.assertEqual(client_get.status_code, 403)
        self.assertEqual(client_data['success'], False)

        """Test Trainer Functionality"""
        # test the unauthorized /drinks route
        trainer_get = self.client().get('/clients', headers=self.trainer_headers)
        trainer_data = trainer_get.json
        # ensure request was good
        self.assertEqual(trainer_get.status_code, 200)
        self.assertEqual(trainer_data['success'], True)
        # ensure we have at least one exercise
        self.assertGreater(len(trainer_data['clients']), 0)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
