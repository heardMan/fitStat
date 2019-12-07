from dotenv import load_dotenv, find_dotenv
load_dotenv(verbose=False)

def setup_environment():
    load_dotenv(find_dotenv(".env", raise_error_if_not_found=True))