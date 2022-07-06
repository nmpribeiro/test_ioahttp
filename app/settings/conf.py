import os
from dotenv import load_dotenv


load_dotenv()


HOST = str(os.getenv("HOST"))
PORT = int(os.getenv("PORT"))

PG_URL = str(os.getenv("PG_URL"))

REDIS = str(os.getenv("REDIS"))

AUTH0_SCOPE = str(os.getenv("AUTH0_SCOPE"))
AUTH0_DOMAIN = str(os.getenv("AUTH0_DOMAIN"))
AUTH0_AUDIENCE = str(os.getenv("AUTH0_AUDIENCE"))
AUTH0_CLIENT_ID = str(os.getenv("AUTH0_CLIENT_ID"))
AUTH0_CLIENT_SECRET = str(os.getenv("AUTH0_CLIENT_SECRET"))

# Test mode only
TEST_MODE = True if os.getenv("TEST_MODE") == "true" else False