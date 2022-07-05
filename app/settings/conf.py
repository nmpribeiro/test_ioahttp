import os
from dotenv import load_dotenv


load_dotenv()

PG_URL = str(os.getenv("PG_URL"))

HOST = str(os.getenv("HOST"))
PORT = int(os.getenv("PORT"))

REDIS = str(os.getenv("REDIS"))

AUTH0_DOMAIN = str(os.getenv("AUTH0_DOMAIN"))
AUTH0_AUDIENCE = str(os.getenv("AUTH0_AUDIENCE"))
AUTH0_CLIENT_ID = str(os.getenv("AUTH0_CLIENT_ID"))
AUTH0_CLIENT_SECRET = str(os.getenv("AUTH0_CLIENT_SECRET"))
AUTH0_SCOPE = str(os.getenv("AUTH0_SCOPE"))
