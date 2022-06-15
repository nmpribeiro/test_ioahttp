import os
from dotenv import load_dotenv

load_dotenv()

PG_URL = str(os.getenv("PG_URL"))

HOST = str(os.getenv("HOST"))
PORT = int(os.getenv("PORT"))
