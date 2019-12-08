# fitStat API
<p>Welcome to the fitStat API Docs</p>
<p>fitStat is an API used to track wokouts</p>


## Endpoints

### GET exercise templates
<p>Allows a user to get an execise template from the database by its ID</p>
<p>Example Request</p>
``````
<p>Example Response</p>
``````

### GET all exercise templates
<p>Allows a user to get all execise templates from the database</p>
<p>Example Request</p>
``````
<p>Example Response</p>
``````

### POST exercise templates
<p>Allows a user to post all execise templates to the database</p>
<p>Example Request</p>
``````
<p>Example Response</p>
``````

### PATCH exercise templates
<p>Allows a user to patch an execise templates in the database by its ID</p>
<p>Example Request</p>
``````
<p>Example Response</p>
``````

### DELETE exercise templates
<p>Allows a user to delete an execise templates in the database by its ID</p>
<p>Example Request</p>
``````
<p>Example Response</p>
``````




### GET workout templates
<p>Allows a user to get an workout template from the database by its ID</p>
<p>Example Request</p>
``````
<p>Example Response</p>
``````

### GET all workout templates
<p>Allows a user to get all workout templates from the database</p>
<p>Example Request</p>
``````
<p>Example Response</p>
``````

### POST workout templates
<p>Allows a user to post all workout templates to the database</p>
<p>Example Request</p>
``````
<p>Example Response</p>
``````

### PATCH workout templates
<p>Allows a user to patch an workout templates in the database by its ID</p>
<p>Example Request</p>
``````
<p>Example Response</p>
``````

### DELETE workout templates
<p>Allows a user to delete an workout templates in the database by its ID</p>
<p>Example Request</p>
``````
<p>Example Response</p>
``````





### GET workouts
<p>Allows a user to get their own workout from the database by its ID</p>
<p>Example Request</p>
``````
<p>Example Response</p>
``````

### GET all workouts
<p>Allows a user to get all their own workouts from the database</p>
<p>Example Request</p>
``````
<p>Example Response</p>
``````

### POST workouts
<p>Allows a user to post their own workout to the database</p>
<p>Example Request</p>
``````
<p>Example Response</p>
``````

### PATCH workouts
<p>Allows a user to patch their own workout in the database by its ID</p>
<p>Example Request</p>
``````
<p>Example Response</p>
``````

### DELETE workouts
<p>Allows a user to delete their own workout in the database by its ID</p>
<p>Example Request</p>
``````
<p>Example Response</p>
``````





### GET workouts as trainer
<p>Allows a user to get any workout from the database by its ID</p>
<p>Example Request</p>
``````
<p>Example Response</p>
``````

### GET all workouts as trainer
<p>Allows a user to get all workouts from the database</p>
<p>Example Request</p>
``````
<p>Example Response</p>
``````

### POST workouts as trainer
<p>Allows a user to post all workout for any user to the database</p>
<p>Example Request</p>
``````
<p>Example Response</p>
``````

### PATCH workouts as trainer
<p>Allows a user to patch any workout in the database by its ID</p>
<p>Example Request</p>
``````
<p>Example Response</p>
``````

### DELETE workouts as trainer
<p>Allows a user to delete any workout in the database by its ID</p>
<p>Example Request</p>
``````
<p>Example Response</p>
``````





### GET clients
<p>Allows a user to get a list of clients from the database by their ID</p>
<p>Example Request</p>
``````
<p>Example Response</p>
``````





## Development Set Up Instructions

<p>This application is primarily composed of a Flask microserver.</p>
<p>The Flask service acts as a controller for a PostgresQL Database defined using the SQLAlcemy ORM</p>
<p>The service also employ an Auth0 authentication and authorization schema with role based access controls (RBAC).</p>

### Flask Server
<p>Setting up an instance of the Flask Server for development is a fairly stright forward process</p>

  1. Clone the repository to your local machine
  2. Open a Command Line Application an navigate to your cloned application
  3. It is strongly Recommended that you create a python virtual environment for your application (Python 3 is recommended)
  4 .Acitvate your virtual environment locally

  5. <p>Install Dependencies with the following command:</p>
    ```
    pip install -r reuirements.txt
    ```

  6. <p>Create a .env file in your root directory and add the following variables to it:</p>
  
    ```#FLASK DEVELOPMENT VARIABLES
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
    TEST_TRAINER_USER_ID = '' #REPLACE WITH A TEST ID```
  

<p>Once you have updated all the environmental variables run you will be able to run the server. Simply type the following command into your command prompt at the root directory with your virtual environment active:</p>
```flask run```

<p>To ensure that the application is configured properly run the the folowing command from the project's root directory with the virtual environment active:</p>

```python test.py```

<p>If you see the out put  ```OK``` your aplpication should be set up correctly a ready for development</p>

<p>Congratulations!!! Your development server should now be available at: <a href='localhost:5000'>localhost:5000</a></p>