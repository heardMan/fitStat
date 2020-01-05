# fitStat API
<p>Welcome to the fitStat API Docs</p>
<p>fitStat is an API used to track wokouts</p>

<p>This project was made as my capstone project for the Udacity Fullstack Web Developer Nanodegree</p>

<p>The way the application is currently desiged is that there are two roles: Client and Trainer</p>

<p>The Client role is able to: read exercise templates, read workout templates, read/post/patch/delete their own workouts</p>

<p>Trainers have administrative access and can perform all functions. Trainers also have the ability to read/post/patch/delete client workouts in the database</p>


## Development Set Up Instructions

<p>This application is primarily composed of a Flask microserver.</p>
<p>The Flask service acts as a controller for a PostgresQL Database defined using the SQLAlcemy ORM</p>
<p>The service also employ an Auth0 authentication and authorization schema with role based access controls (RBAC).</p>

### Flask Server Set Up Instruction
<p>Setting up an instance of the Flask Server for development is a fairly stright forward process</p>

  #### 1. Clone the repository to your local machine
  #### 2. Open a Command Line Application an navigate to your cloned application
  #### 3. It is strongly Recommended that you create a python virtual environment for your application (Python 3 is recommended)
  #### 4 .Acitvate your virtual environment locally

  #### 5. Install Dependencies with the following command:
  <code>pip install -r reuirements.txt</code>
    
  
  #### 6. Create a .env file in your root directory and add the following variables to it:
  
  <pre><code>#FLASK DEVELOPMENT VARIABLES
DEBUG = True
TEST = None
FLASK_ENV = 'development'
FLASK_APP = app.py
#DATABASE VARIABLES
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = '' #REPLACE WITH YOUR LOCAL POSTGRES URI
DEVELOPMENT_DATABASE_NAME = 'fitStat'
SQLALCHEMY_TEST_DATABASE_URI = '' #REPLACE WITH YOUR LOCAL POSTGRES URI
TEST_DATABASE_NAME = 'test_fitStat'
SECRET = '' #REPLACE WITH YOUR SECRET
AUTH0_DOMAIN = '' #REPLACE WITH YOUR AUTH0 DOMAIN
ALGORITHMS = ['RS256']
API_AUDIENCE = 'fitStat'
AUTH0_CLIENT_ID = '' #REPLACE WITH YOUR AUTH0 CLIENT ID
AUTH0_CLIENT_SECRET = '' #REPLACE WITH YOUR AUTH0 CLIENT SECRET
TEST_CLIENT_TOKEN = '' #REPLACE WITH A TEST TOKEN
TEST_TRAINER_TOKEN = '' #REPLACE WITH A TEST TOKEN
TEST_CLIENT_USER_ID = '' #REPLACE WITH A TEST ID
TEST_TRAINER_USER_ID = '' #REPLACE WITH A TEST ID</code></pre>
  

<p>Once you have updated all the environmental variables run you will be able to run the server. Simply type the following command into your command prompt at the root directory with your virtual environment active: <code>flask run</code></p>




<p>The proceeding set of commands creates a test database with the name "test_fitStat" then populates that database with some sample data that can be used for testing purposes. To ensure that the application is configured properly run the the folowing command from the project's root directory with the virtual environment active:</p>

### Testing Set Up Instruction
<pre><code>dropdb test_fitStat
createdb test_fitStat
psql test_fitStat < seeds.psql
python test.py</code></pre>

<p>If you see the out put 'OK' your aplpication should be set up correctly a ready for development</p>

<p>Congratulations!!! Your development server should now be available locally on your machine at port 5000</p>


## API Endpoints

### GET exercise templates by ID
<p>Allows a user to get an execise template from the database by its ID</p>
<p>URL: exercise_templates/1</p>

<p>Example Response</p>
<pre><code>{
      "exercise": {
        "description": "multi-joint chest workout",
        "id": 1,
        "name": "bench press"
      },
      "success": true
    }</code></pre>

### GET all exercise templates
<p>Allows a user to get all execise templates from the database</p>
<p>URL: exercise_templates/></p>

<p>Example Response</p>
<pre>
<code>{
  "exercises": [
    {
      "description": "multi-joint chest workout",
      "id": 1,
      "name": "bench press"
    },
    {
      "description": "multi-joint back workout",
      "id": 2,
      "name": "bent over row"
    }
  ],
  "success": true
}</code>
</pre>

### POST exercise templates
<p>Allows a user to post an execise template to the database</p>
<p>URL: exercise_templates/</p>

<p>Example Request</p>
<pre><code>{
	"name": "test_exercise",
	"description": "test_description"
}</code></pre>
<p>Example Response</p>
<pre><code>{
  "new_exercise": {
    "description": "test_description",
    "id": 3,
    "name": "test_exercise"
  },
  "success": true
}</code></pre>

### PATCH exercise templates
<p>Allows a user to patch an execise templates in the database by its ID</p>
<p>URL: exercise_templates/2</p>

<p>Example Request</p>
<pre><code>{
	"name": "test_exercise_edited",
	"description": "test_description_edited"
}</code></pre>
<p>Example Response</p>
<pre><code>{
  "edited_exercise": {
    "description": "test_description_edited",
    "id": 2,
    "name": "test_exercise_edited"
  },
  "success": true
}</code></pre>

### DELETE exercise templates
<p>Allows a user to delete an execise templates in the database by its ID</p>
<p>URL: exercise_templates/3</p>

<p>Example Response</p>
<pre><code>{
  "deleted_exercise": {
    "description": "test_description",
    "id": 3,
    "name": "test_exercise"
  },
  "success": true
}</code></pre>





### GET workout templates by ID
<p>Allows a user to get an workout template from the database by its ID</p>
<p>URL: workout_templates/1</p>

<p>Example Response</p>
<pre><code>{
  "success": true,
  "workouts": {
    "description": "a good chest workout",
    "exercises": [
      {
        "description": "multi-joint chest workout",
        "exercise_template_id": 1,
        "id": 1,
        "name": "bench press",
        "recommended_sets": 5,
        "workout_template_id": 1
      },
      {
        "description": "test_description_edited",
        "exercise_template_id": 2,
        "id": 2,
        "name": "test_exercise_edited",
        "recommended_sets": 5,
        "workout_template_id": 1
      }
    ],
    "id": 1,
    "name": "workout one"
  }
}</code></pre>

### GET all workout templates
<p>Allows a user to get all workout templates from the database</p>
<p>URL: workout_templates/</p>

<p>Example Response</p>
<pre><code>{
  "success": true,
  "workouts": [
    {
      "description": "a good chest workout",
      "exercises": [
        {
          "description": "multi-joint chest workout",
          "exercise_template_id": 1,
          "id": 1,
          "name": "bench press",
          "recommended_sets": 5,
          "workout_template_id": 1
        },
        {
          "description": "test_description_edited",
          "exercise_template_id": 2,
          "id": 2,
          "name": "test_exercise_edited",
          "recommended_sets": 5,
          "workout_template_id": 1
        }
      ],
      "id": 1,
      "name": "workout one"
    }
  ]
}</code></pre>

### POST workout templates
<p>Allows a user to post all workout templates to the database</p>
<p>URL: workout_templates/</p>

<p>Example Request</p>
<pre><code>{
        "description": "a good leg workout",
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
        "name": "workout one"
    }</code></pre>
<p>Example Response</p>
<pre><code>{
  "new_workout": {
    "description": "a good leg workout",
    "exercises": [
      {
        "description": "test_description_edited",
        "exercise_template_id": 2,
        "id": 3,
        "name": "test_exercise_edited",
        "recommended_sets": 5,
        "workout_template_id": 2
      },
      {
        "description": "test_description_edited",
        "exercise_template_id": 2,
        "id": 4,
        "name": "test_exercise_edited",
        "recommended_sets": 5,
        "workout_template_id": 2
      }
    ],
    "id": 2,
    "name": "workout one"
  },
  "success": true
}</code></pre>

### PATCH workout templates
<p>Allows a user to patch an workout templates in the database by its ID</p>
<p>URL: workout_templates/1</p>

<p>Example Request</p>
<pre><code>{
            "description": "a good chest workout",
            "exercises": [
                {
                    "exercise_template_id": 2,
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
        }</code></pre>
<p>Example Response</p>
<pre><code>{
  "edited_workout": {
    "description": "a good chest workout",
    "exercises": [
      {
        "description": "multi-joint chest workout",
        "exercise_template_id": 1,
        "id": 1,
        "name": "bench press",
        "recommended_sets": 5,
        "workout_template_id": 1
      },
      {
        "description": "multi-joint back workout",
        "exercise_template_id": 2,
        "id": 2,
        "name": "bent over row",
        "recommended_sets": 5,
        "workout_template_id": 1
      }
    ],
    "id": 1,
    "name": "workout one"
  },
  "success": true
}</code></pre>

### DELETE workout templates
<p>Allows a user to delete an workout templates in the database by its ID</p>
<p>URL: workout_templates/2</p>

<p>Example Response</p>
<pre><code>{
  "deleted_workout": {
    "description": "a good leg workout",
    "exercises": [],
    "id": 2,
    "name": "workout one"
  },
  "success": true
}</code></pre>





### GET workouts by ID
<p>Allows a user to get their own workout from the database by its ID</p>
<p>URL: workouts/1</p>

<p>Example Response</p>
<pre><code>{
  "success": true,
  "workout": {
    "date": "March 5",
    "exercises": [
      {
        "description": "multi-joint chest workout",
        "exercise_sets": [
          {
            "exercise_id": 1,
            "id": 1,
            "repetitions": 5,
            "rest": 30,
            "weight": 15
          },
          {
            "exercise_id": 1,
            "id": 2,
            "repetitions": 6,
            "rest": 30,
            "weight": 15
          }
        ],
        "exercise_template_id": 1,
        "id": 1,
        "name": "bench press",
        "workout_id": 1
      },
      {
        "description": "test_description_edited",
        "exercise_sets": [
          {
            "exercise_id": 2,
            "id": 3,
            "repetitions": 6,
            "rest": 60,
            "weight": 150
          },
          {
            "exercise_id": 2,
            "id": 4,
            "repetitions": 5,
            "rest": 60,
            "weight": 150
          }
        ],
        "exercise_template_id": 2,
        "id": 2,
        "name": "test_exercise_edited",
        "workout_id": 1
      }
    ],
    "id": 1,
    "name": "workout one",
    "user_id": "auth0|5de466550364611d2e2bd00b",
    "workout-template": {
      "description": "a good chest workout",
      "exercises": [
        {
          "description": "multi-joint chest workout",
          "exercise_template_id": 1,
          "id": 1,
          "name": "bench press",
          "recommended_sets": 5,
          "workout_template_id": 1
        },
        {
          "description": "test_description_edited",
          "exercise_template_id": 2,
          "id": 2,
          "name": "test_exercise_edited",
          "recommended_sets": 5,
          "workout_template_id": 1
        }
      ],
      "id": 1,
      "name": "workout one"
    },
    "workout_template_id": 1
  }
}</code></pre>

### GET all workouts
<p>Allows a user to get all their own workouts from the database</p>
<p>URL: workouts/</p>

<p>Example Response</p>
<pre><code>{
  "success": true,
  "workouts": [
    {
      "date": "March 5",
      "exercises": [
        {
          "description": "multi-joint chest workout",
          "exercise_sets": [
            {
              "exercise_id": 1,
              "id": 1,
              "repetitions": 5,
              "rest": 30,
              "weight": 15
            },
            {
              "exercise_id": 1,
              "id": 2,
              "repetitions": 6,
              "rest": 30,
              "weight": 15
            }
          ],
          "exercise_template_id": 1,
          "id": 1,
          "name": "bench press",
          "workout_id": 1
        },
        {
          "description": "multi-joint back workout",
          "exercise_sets": [
            {
              "exercise_id": 2,
              "id": 3,
              "repetitions": 6,
              "rest": 60,
              "weight": 150
            },
            {
              "exercise_id": 2,
              "id": 4,
              "repetitions": 5,
              "rest": 60,
              "weight": 150
            }
          ],
          "exercise_template_id": 2,
          "id": 2,
          "name": "bent over row",
          "workout_id": 1
        }
      ],
      "id": 1,
      "name": "workout one",
      "user_id": "auth0|5de466550364611d2e2bd00b",
      "workout-template": {
        "description": "a good chest workout",
        "exercises": [
          {
            "description": "multi-joint chest workout",
            "exercise_template_id": 1,
            "id": 1,
            "name": "bench press",
            "recommended_sets": 5,
            "workout_template_id": 1
          },
          {
            "description": "multi-joint back workout",
            "exercise_template_id": 2,
            "id": 2,
            "name": "bent over row",
            "recommended_sets": 5,
            "workout_template_id": 1
          }
        ],
        "id": 1,
        "name": "workout one"
      },
      "workout_template_id": 1
    },
    {
      "date": "March 2",
      "exercises": [
        {
          "description": "multi-joint chest workout",
          "exercise_sets": [
            {
              "exercise_id": 7,
              "id": 13,
              "repetitions": 5,
              "rest": 30,
              "weight": 15
            },
            {
              "exercise_id": 7,
              "id": 14,
              "repetitions": 6,
              "rest": 30,
              "weight": 15
            }
          ],
          "exercise_template_id": 1,
          "id": 7,
          "name": "bench press",
          "workout_id": 4
        },
        {
          "description": "multi-joint chest workout",
          "exercise_sets": [
            {
              "exercise_id": 8,
              "id": 15,
              "repetitions": 6,
              "rest": 60,
              "weight": 150
            },
            {
              "exercise_id": 8,
              "id": 16,
              "repetitions": 5,
              "rest": 60,
              "weight": 150
            }
          ],
          "exercise_template_id": 1,
          "id": 8,
          "name": "bench press",
          "workout_id": 4
        }
      ],
      "id": 4,
      "name": "workout one",
      "user_id": "auth0|5de466550364611d2e2bd00b",
      "workout-template": {
        "description": "a good chest workout",
        "exercises": [
          {
            "description": "multi-joint chest workout",
            "exercise_template_id": 1,
            "id": 1,
            "name": "bench press",
            "recommended_sets": 5,
            "workout_template_id": 1
          },
          {
            "description": "multi-joint back workout",
            "exercise_template_id": 2,
            "id": 2,
            "name": "bent over row",
            "recommended_sets": 5,
            "workout_template_id": 1
          }
        ],
        "id": 1,
        "name": "workout one"
      },
      "workout_template_id": 1
    }
  ]
}</code></pre>

### POST workouts
<p>Allows a user to post their own workout to the database</p>
<p>URL: workouts/</p>

<p>Example Request</p>
<pre><code>{
	"date":"Mar 5",
	"workout_template_id":1,
	"exercises":[
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
}</code></pre>
<p>Example Response</p>
<pre><code>{
  "new_workout": {
    "date": "Mar 5",
    "exercises": [
      {
        "description": "multi-joint chest workout",
        "exercise_sets": [
          {
            "exercise_id": 9,
            "id": 17,
            "repetitions": 5,
            "rest": 30,
            "weight": 15
          },
          {
            "exercise_id": 9,
            "id": 18,
            "repetitions": 5,
            "rest": 30,
            "weight": 15
          }
        ],
        "exercise_template_id": 1,
        "id": 9,
        "name": "bench press",
        "workout_id": 5
      },
      {
        "description": "multi-joint back workout",
        "exercise_sets": [
          {
            "exercise_id": 10,
            "id": 19,
            "repetitions": 6,
            "rest": 55,
            "weight": 125
          },
          {
            "exercise_id": 10,
            "id": 20,
            "repetitions": 7,
            "rest": 65,
            "weight": 125
          }
        ],
        "exercise_template_id": 2,
        "id": 10,
        "name": "bent over row",
        "workout_id": 5
      }
    ],
    "id": 5,
    "name": "workout one",
    "user_id": "auth0|5de466550364611d2e2bd00b",
    "workout-template": {
      "description": "a good chest workout",
      "exercises": [
        {
          "description": "multi-joint chest workout",
          "exercise_template_id": 1,
          "id": 1,
          "name": "bench press",
          "recommended_sets": 5,
          "workout_template_id": 1
        },
        {
          "description": "multi-joint back workout",
          "exercise_template_id": 2,
          "id": 2,
          "name": "bent over row",
          "recommended_sets": 5,
          "workout_template_id": 1
        }
      ],
      "id": 1,
      "name": "workout one"
    },
    "workout_template_id": 1
  },
  "success": true
}</code></pre>

### PATCH workouts
<p>Allows a user to patch their own workout in the database by its ID</p>
<p>URL: workouts/1</p>

<p>Example Request</p>

<pre><code>{
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
}</code></pre>

<p>Example Response</p>
<pre><code>{
  "edited_workout": {
    "date": "March 6",
    "exercises": [
      {
        "description": "multi-joint chest workout",
        "exercise_sets": [
          {
            "exercise_id": 1,
            "id": 1,
            "repetitions": 5,
            "rest": 30,
            "weight": 15
          },
          {
            "exercise_id": 1,
            "id": 21,
            "repetitions": 234,
            "rest": 234,
            "weight": 234
          }
        ],
        "exercise_template_id": 1,
        "id": 1,
        "name": "bench press",
        "workout_id": 1
      },
      {
        "description": "multi-joint chest workout",
        "exercise_sets": [
          {
            "exercise_id": 11,
            "id": 22,
            "repetitions": 123,
            "rest": 123,
            "weight": 123
          }
        ],
        "exercise_template_id": 1,
        "id": 11,
        "name": "bench press",
        "workout_id": 1
      }
    ],
    "id": 1,
    "name": "workout one",
    "user_id": "auth0|5de466550364611d2e2bd00b",
    "workout-template": {
      "description": "a good chest workout",
      "exercises": [
        {
          "description": "multi-joint chest workout",
          "exercise_template_id": 1,
          "id": 1,
          "name": "bench press",
          "recommended_sets": 5,
          "workout_template_id": 1
        },
        {
          "description": "multi-joint back workout",
          "exercise_template_id": 2,
          "id": 2,
          "name": "bent over row",
          "recommended_sets": 5,
          "workout_template_id": 1
        }
      ],
      "id": 1,
      "name": "workout one"
    },
    "workout_template_id": 1
  },
  "success": true
}</code></pre>

### DELETE workouts
<p>Allows a user to delete their own workout in the database by its ID</p>
<p>URL: workouts/1</p>

<p>Example Response</p>
<pre><code>{
  "deleted_workout": {
    "date": "March 5",
    "exercises": [
      {
        "description": "multi-joint chest workout",
        "exercise_sets": [
          {
            "exercise_id": 1,
            "id": 1,
            "repetitions": 5,
            "rest": 30,
            "weight": 15
          },
          {
            "exercise_id": 1,
            "id": 2,
            "repetitions": 6,
            "rest": 30,
            "weight": 15
          }
        ],
        "exercise_template_id": 1,
        "id": 1,
        "name": "bench press",
        "workout_id": 1
      },
      {
        "description": "multi-joint back workout",
        "exercise_sets": [
          {
            "exercise_id": 2,
            "id": 3,
            "repetitions": 6,
            "rest": 60,
            "weight": 150
          },
          {
            "exercise_id": 2,
            "id": 4,
            "repetitions": 5,
            "rest": 60,
            "weight": 150
          }
        ],
        "exercise_template_id": 2,
        "id": 2,
        "name": "bent over row",
        "workout_id": 1
      }
    ],
    "id": 1,
    "name": "workout one",
    "user_id": "auth0|5de466550364611d2e2bd00b",
    "workout-template": {
      "description": "a good chest workout",
      "exercises": [
        {
          "description": "multi-joint chest workout",
          "exercise_template_id": 1,
          "id": 1,
          "name": "bench press",
          "recommended_sets": 5,
          "workout_template_id": 2
        },
        {
          "description": "multi-joint back workout",
          "exercise_template_id": 2,
          "id": 2,
          "name": "bent over row",
          "recommended_sets": 5,
          "workout_template_id": 2
        }
      ],
      "id": 2,
      "name": "workout one"
    },
    "workout_template_id": 2
  },
  "success": true
}</code></pre>





### GET workouts as trainer
<p>Allows a user to get any workout from the database by its ID</p>
<p>URL: trainer/workouts/1</p>

<p>Example Response</p>
<pre><code>{
  "success": true,
  "workout": {
    "date": "March 5",
    "exercises": [
      {
        "description": "multi-joint chest workout",
        "exercise_sets": [
          {
            "exercise_id": 1,
            "id": 1,
            "repetitions": 5,
            "rest": 30,
            "weight": 15
          },
          {
            "exercise_id": 1,
            "id": 2,
            "repetitions": 6,
            "rest": 30,
            "weight": 15
          }
        ],
        "exercise_template_id": 1,
        "id": 1,
        "name": "bench press",
        "workout_id": 1
      },
      {
        "description": "multi-joint back workout",
        "exercise_sets": [
          {
            "exercise_id": 2,
            "id": 3,
            "repetitions": 6,
            "rest": 60,
            "weight": 150
          },
          {
            "exercise_id": 2,
            "id": 4,
            "repetitions": 5,
            "rest": 60,
            "weight": 150
          }
        ],
        "exercise_template_id": 2,
        "id": 2,
        "name": "bent over row",
        "workout_id": 1
      }
    ],
    "id": 1,
    "name": "workout one",
    "user_id": "auth0|5de466550364611d2e2bd00b",
    "workout-template": {
      "description": "a good chest workout",
      "exercises": [
        {
          "description": "multi-joint chest workout",
          "exercise_template_id": 1,
          "id": 1,
          "name": "bench press",
          "recommended_sets": 5,
          "workout_template_id": 2
        },
        {
          "description": "multi-joint back workout",
          "exercise_template_id": 2,
          "id": 2,
          "name": "bent over row",
          "recommended_sets": 5,
          "workout_template_id": 2
        }
      ],
      "id": 2,
      "name": "workout one"
    },
    "workout_template_id": 2
  }
}</code></pre>

### GET all workouts as trainer
<p>Allows a user to get all workouts from the database</p>
<p>URL: /trainer/workouts</p>

<p>Example Response</p>
<pre><code>{
  "success": true,
  "workouts": [
    {
      "date": "March 5",
      "exercises": [
        {
          "description": "multi-joint chest workout",
          "exercise_sets": [
            {
              "exercise_id": 1,
              "id": 1,
              "repetitions": 5,
              "rest": 30,
              "weight": 15
            },
            {
              "exercise_id": 1,
              "id": 2,
              "repetitions": 6,
              "rest": 30,
              "weight": 15
            }
          ],
          "exercise_template_id": 1,
          "id": 1,
          "name": "bench press",
          "workout_id": 1
        },
        {
          "description": "multi-joint back workout",
          "exercise_sets": [
            {
              "exercise_id": 2,
              "id": 3,
              "repetitions": 6,
              "rest": 60,
              "weight": 150
            },
            {
              "exercise_id": 2,
              "id": 4,
              "repetitions": 5,
              "rest": 60,
              "weight": 150
            }
          ],
          "exercise_template_id": 2,
          "id": 2,
          "name": "bent over row",
          "workout_id": 1
        }
      ],
      "id": 1,
      "name": "workout one",
      "user_id": "auth0|5de466550364611d2e2bd00b",
      "workout-template": {
        "description": "a good chest workout",
        "exercises": [
          {
            "description": "multi-joint chest workout",
            "exercise_template_id": 1,
            "id": 1,
            "name": "bench press",
            "recommended_sets": 5,
            "workout_template_id": 2
          },
          {
            "description": "multi-joint back workout",
            "exercise_template_id": 2,
            "id": 2,
            "name": "bent over row",
            "recommended_sets": 5,
            "workout_template_id": 2
          }
        ],
        "id": 2,
        "name": "workout one"
      },
      "workout_template_id": 2
    },
    {
      "date": "March 2",
      "exercises": [
        {
          "description": "multi-joint chest workout",
          "exercise_sets": [
            {
              "exercise_id": 3,
              "id": 5,
              "repetitions": 5,
              "rest": 30,
              "weight": 15
            },
            {
              "exercise_id": 3,
              "id": 6,
              "repetitions": 6,
              "rest": 30,
              "weight": 15
            }
          ],
          "exercise_template_id": 1,
          "id": 3,
          "name": "bench press",
          "workout_id": 2
        },
        {
          "description": "multi-joint back workout",
          "exercise_sets": [
            {
              "exercise_id": 4,
              "id": 7,
              "repetitions": 6,
              "rest": 60,
              "weight": 150
            },
            {
              "exercise_id": 4,
              "id": 8,
              "repetitions": 5,
              "rest": 60,
              "weight": 150
            }
          ],
          "exercise_template_id": 2,
          "id": 4,
          "name": "bent over row",
          "workout_id": 2
        }
      ],
      "id": 2,
      "name": "workout one",
      "user_id": "auth0|5de466550364611d2e2bd00b",
      "workout-template": {
        "description": "a good chest workout",
        "exercises": [
          {
            "description": "multi-joint chest workout",
            "exercise_template_id": 1,
            "id": 1,
            "name": "bench press",
            "recommended_sets": 5,
            "workout_template_id": 2
          },
          {
            "description": "multi-joint back workout",
            "exercise_template_id": 2,
            "id": 2,
            "name": "bent over row",
            "recommended_sets": 5,
            "workout_template_id": 2
          }
        ],
        "id": 2,
        "name": "workout one"
      },
      "workout_template_id": 2
    },
    {
      "date": "March 2",
      "exercises": [
        {
          "description": "multi-joint chest workout",
          "exercise_sets": [
            {
              "exercise_id": 5,
              "id": 9,
              "repetitions": 5,
              "rest": 30,
              "weight": 15
            },
            {
              "exercise_id": 5,
              "id": 10,
              "repetitions": 6,
              "rest": 30,
              "weight": 15
            }
          ],
          "exercise_template_id": 1,
          "id": 5,
          "name": "bench press",
          "workout_id": 3
        },
        {
          "description": "multi-joint chest workout",
          "exercise_sets": [
            {
              "exercise_id": 6,
              "id": 11,
              "repetitions": 6,
              "rest": 60,
              "weight": 150
            },
            {
              "exercise_id": 6,
              "id": 12,
              "repetitions": 5,
              "rest": 60,
              "weight": 150
            }
          ],
          "exercise_template_id": 1,
          "id": 6,
          "name": "bench press",
          "workout_id": 3
        }
      ],
      "id": 3,
      "name": "workout one",
      "user_id": "auth0|5de466550364611d2e2bd00b",
      "workout-template": {
        "description": "a good chest workout",
        "exercises": [
          {
            "description": "multi-joint chest workout",
            "exercise_template_id": 1,
            "id": 1,
            "name": "bench press",
            "recommended_sets": 5,
            "workout_template_id": 2
          },
          {
            "description": "multi-joint back workout",
            "exercise_template_id": 2,
            "id": 2,
            "name": "bent over row",
            "recommended_sets": 5,
            "workout_template_id": 2
          }
        ],
        "id": 2,
        "name": "workout one"
      },
      "workout_template_id": 2
    },
    {
      "date": "March 2",
      "exercises": [
        {
          "description": "multi-joint chest workout",
          "exercise_sets": [
            {
              "exercise_id": 7,
              "id": 13,
              "repetitions": 5,
              "rest": 30,
              "weight": 15
            },
            {
              "exercise_id": 7,
              "id": 14,
              "repetitions": 6,
              "rest": 30,
              "weight": 15
            }
          ],
          "exercise_template_id": 1,
          "id": 7,
          "name": "bench press",
          "workout_id": 4
        },
        {
          "description": "multi-joint chest workout",
          "exercise_sets": [
            {
              "exercise_id": 8,
              "id": 15,
              "repetitions": 6,
              "rest": 60,
              "weight": 150
            },
            {
              "exercise_id": 8,
              "id": 16,
              "repetitions": 5,
              "rest": 60,
              "weight": 150
            }
          ],
          "exercise_template_id": 1,
          "id": 8,
          "name": "bench press",
          "workout_id": 4
        }
      ],
      "id": 4,
      "name": "workout one",
      "user_id": "auth0|5de466550364611d2e2bd00b",
      "workout-template": {
        "description": "a good chest workout",
        "exercises": [
          {
            "description": "multi-joint chest workout",
            "exercise_template_id": 1,
            "id": 1,
            "name": "bench press",
            "recommended_sets": 5,
            "workout_template_id": 2
          },
          {
            "description": "multi-joint back workout",
            "exercise_template_id": 2,
            "id": 2,
            "name": "bent over row",
            "recommended_sets": 5,
            "workout_template_id": 2
          }
        ],
        "id": 2,
        "name": "workout one"
      },
      "workout_template_id": 2
    }
  ]
}</code></pre>

### GET workouts as trainer by User ID
<p>Allows a user to post all workout for any user to the database</p>
<p>URL: trainer/workouts-by-user/auth0|5de466550364611d2e2bd00b</p>

<p>Example Response</p>
<pre><code>{
  "success": true,
  "workouts": [
    {
      "date": "March 2",
      "exercises": [
        {
          "description": "multi-joint chest workout",
          "exercise_sets": [
            {
              "exercise_id": 3,
              "id": 5,
              "repetitions": 5,
              "rest": 30,
              "weight": 15
            },
            {
              "exercise_id": 3,
              "id": 6,
              "repetitions": 6,
              "rest": 30,
              "weight": 15
            }
          ],
          "exercise_template_id": 1,
          "id": 3,
          "name": "bench press",
          "workout_id": 2
        },
        {
          "description": "multi-joint back workout",
          "exercise_sets": [
            {
              "exercise_id": 4,
              "id": 7,
              "repetitions": 6,
              "rest": 60,
              "weight": 150
            },
            {
              "exercise_id": 4,
              "id": 8,
              "repetitions": 5,
              "rest": 60,
              "weight": 150
            }
          ],
          "exercise_template_id": 2,
          "id": 4,
          "name": "bent over row",
          "workout_id": 2
        }
      ],
      "id": 2,
      "name": "workout one",
      "user_id": "auth0|5de466550364611d2e2bd00b",
      "workout-template": {
        "description": "a good chest workout",
        "exercises": [
          {
            "description": "multi-joint chest workout",
            "exercise_template_id": 1,
            "id": 1,
            "name": "bench press",
            "recommended_sets": 5,
            "workout_template_id": 2
          },
          {
            "description": "multi-joint back workout",
            "exercise_template_id": 2,
            "id": 2,
            "name": "bent over row",
            "recommended_sets": 5,
            "workout_template_id": 2
          }
        ],
        "id": 2,
        "name": "workout one"
      },
      "workout_template_id": 2
    },
    {
      "date": "March 2",
      "exercises": [
        {
          "description": "multi-joint chest workout",
          "exercise_sets": [
            {
              "exercise_id": 5,
              "id": 9,
              "repetitions": 5,
              "rest": 30,
              "weight": 15
            },
            {
              "exercise_id": 5,
              "id": 10,
              "repetitions": 6,
              "rest": 30,
              "weight": 15
            }
          ],
          "exercise_template_id": 1,
          "id": 5,
          "name": "bench press",
          "workout_id": 3
        },
        {
          "description": "multi-joint chest workout",
          "exercise_sets": [
            {
              "exercise_id": 6,
              "id": 11,
              "repetitions": 6,
              "rest": 60,
              "weight": 150
            },
            {
              "exercise_id": 6,
              "id": 12,
              "repetitions": 5,
              "rest": 60,
              "weight": 150
            }
          ],
          "exercise_template_id": 1,
          "id": 6,
          "name": "bench press",
          "workout_id": 3
        }
      ],
      "id": 3,
      "name": "workout one",
      "user_id": "auth0|5de466550364611d2e2bd00b",
      "workout-template": {
        "description": "a good chest workout",
        "exercises": [
          {
            "description": "multi-joint chest workout",
            "exercise_template_id": 1,
            "id": 1,
            "name": "bench press",
            "recommended_sets": 5,
            "workout_template_id": 2
          },
          {
            "description": "multi-joint back workout",
            "exercise_template_id": 2,
            "id": 2,
            "name": "bent over row",
            "recommended_sets": 5,
            "workout_template_id": 2
          }
        ],
        "id": 2,
        "name": "workout one"
      },
      "workout_template_id": 2
    }
  ]
}</code></pre>

### POST workouts as trainer
<p>Allows a user to post all workout for any user to the database</p>
<p>URL: </p>

<p>Example Request</p>
<pre><code>{
	"date":"Mar 5",
	"workout_template_id":1,
	"user_id":"auth0|5de466550364611d2e2bd00b",
	"exercises":[
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
}</code></pre>
<p>Example Response</p>
<pre><code>{
  "new_workout": {
    "date": "Mar 5",
    "exercises": [
      {
        "description": "multi-joint chest workout",
        "exercise_sets": [
          {
            "exercise_id": 9,
            "id": 17,
            "repetitions": 5,
            "rest": 30,
            "weight": 15
          },
          {
            "exercise_id": 9,
            "id": 18,
            "repetitions": 5,
            "rest": 30,
            "weight": 15
          }
        ],
        "exercise_template_id": 1,
        "id": 9,
        "name": "bench press",
        "workout_id": 5
      },
      {
        "description": "multi-joint back workout",
        "exercise_sets": [
          {
            "exercise_id": 10,
            "id": 19,
            "repetitions": 6,
            "rest": 55,
            "weight": 125
          },
          {
            "exercise_id": 10,
            "id": 20,
            "repetitions": 7,
            "rest": 65,
            "weight": 125
          }
        ],
        "exercise_template_id": 2,
        "id": 10,
        "name": "bent over row",
        "workout_id": 5
      }
    ],
    "id": 5,
    "name": "custom workout",
    "user_id": "auth0|5de466550364611d2e2bd00b",
    "workout-template": {
      "description": "custom workout",
      "exercises": [],
      "id": 1,
      "name": "custom workout"
    },
    "workout_template_id": 1
  },
  "success": true
}</code></pre>

### PATCH workouts as trainer
<p>Allows a user to patch any workout in the database by its ID</p>
<p>URL:</p>

<p>Example Request</p>
<pre><code>{
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
        "user_id": "auth0|5de466550364611d2e2bd00b",
        "workout_template_id": 2
  }</code></pre>
<p>Example Response</p>
<pre><code>{
  "edited_workout": {
    "date": "March 6",
    "exercises": [
      {
        "description": "multi-joint chest workout",
        "exercise_sets": [
          {
            "exercise_id": 9,
            "id": 18,
            "repetitions": 123,
            "rest": 123,
            "weight": 123
          }
        ],
        "exercise_template_id": 1,
        "id": 9,
        "name": "bench press",
        "workout_id": 2
      }
    ],
    "id": 2,
    "name": "workout one",
    "user_id": "auth0|5de466550364611d2e2bd00b",
    "workout-template": {
      "description": "a good chest workout",
      "exercises": [
        {
          "description": "multi-joint chest workout",
          "exercise_template_id": 1,
          "id": 1,
          "name": "bench press",
          "recommended_sets": 5,
          "workout_template_id": 2
        },
        {
          "description": "multi-joint back workout",
          "exercise_template_id": 2,
          "id": 2,
          "name": "bent over row",
          "recommended_sets": 5,
          "workout_template_id": 2
        }
      ],
      "id": 2,
      "name": "workout one"
    },
    "workout_template_id": 2
  },
  "success": true
}</code></pre>

### DELETE workouts as trainer
<p>Allows a user to delete any workout in the database by its ID</p>
<p>URL: trainer/workouts/2</p>

<p>Example Response</p>
<pre><code>{
  "deleted_workout": {
    "date": "March 6",
    "exercises": [
      {
        "description": "multi-joint chest workout",
        "exercise_sets": [
          {
            "exercise_id": 11,
            "id": 22,
            "repetitions": 123,
            "rest": 123,
            "weight": 123
          }
        ],
        "exercise_template_id": 1,
        "id": 11,
        "name": "bench press",
        "workout_id": 2
      }
    ],
    "id": 2,
    "name": "custom workout",
    "user_id": "auth0|5de466550364611d2e2bd00b",
    "workout-template": {
      "description": "custom workout",
      "exercises": [],
      "id": 1,
      "name": "custom workout"
    },
    "workout_template_id": 1
  },
  "success": true
}</code></pre>





### GET clients
<p>Allows a user to get a list of clients from the database by their ID</p>
<p>URL:</p>

<p>Example Response</p>
<pre><code>{
  "clients": [
    {
      "email": "someguy@gmail.com",
      "id": "auth0|5de466550364611d2e2bd00b",
      "name": "someguy@gmail.com"
    }
  ],
  "success": true
}</code></pre>





