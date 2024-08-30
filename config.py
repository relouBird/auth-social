import os
from dotenv import load_dotenv


load_dotenv()

CLIENT_ID = os.environ.get('CLIENT_ID', None)
CLIENT_SECRET = os.environ.get('CLIENT_SECRET', None)
FACEBOOK_CLIENT_ID = os.environ.get('FACEBOOK_CLIENT_ID',None)
FACEBOOK_CLIENT_SECRET = os.environ.get('FACEBOOK_CLIENT_SECRET',None)
PORT= int(os.environ.get('PORT', 5100))