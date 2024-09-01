import os
from dotenv import load_dotenv


load_dotenv()

GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', None)
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', None)
FACEBOOK_CLIENT_ID = os.environ.get('FACEBOOK_CLIENT_ID',None)
FACEBOOK_CLIENT_SECRET = os.environ.get('FACEBOOK_CLIENT_SECRET',None)
BACKEND_URL = os.environ.get('BACKEND_URL', None)
PORT= int(os.environ.get('PORT', 5100))