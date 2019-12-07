import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(verbose=False)

def setup_environment():
    if os.getenv("FLASK_ENV") is 'development':
        load_dotenv(find_dotenv(".env", raise_error_if_not_found=True))
    else:
        return True