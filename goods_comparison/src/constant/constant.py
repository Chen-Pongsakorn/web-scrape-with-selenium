import os

# from dotenv import load_dotenv, find_dotenv

# load_dotenv(find_dotenv(".env"))

TIMEOUT_FOR_EACH_ELEMENT = int(os.environ.get("TIMEOUT_FOR_EACH_ELEMENT", 30))
WAIT_TIME_FOR_STARTING_SITE = int(os.environ.get("WAIT_TIME_FOR_STARTING_SITE", 10))