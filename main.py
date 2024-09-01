import fastapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi import status, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Annotated
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
import uvicorn
from authlib.integrations.starlette_client import OAuth,OAuthError
# import os
import requests


# importation des api-key et secret
from config import GOOGLE_CLIENT_ID,GOOGLE_CLIENT_SECRET,PORT,FACEBOOK_CLIENT_ID,FACEBOOK_CLIENT_SECRET, BACKEND_URL

# lancement
app = fastapi.FastAPI()

#permet au serveur d'afficher des page html creer dans le dossier templates
templates = Jinja2Templates(directory="templates")

#gerer la protection et les secrets de session
app.add_middleware(
    SessionMiddleware,
    secret_key=GOOGLE_CLIENT_SECRET,
    session_cookie="your_session_cookie_name",  # Nom du cookie de session
    max_age=3600,  # Temps de vie des sessions en secondes
    same_site="lax",  # Ou "strict" ou "none" selon vos besoins
    https_only=False  # Mettez à True en production avec HTTPS
)

# point de depart de l'authentification
oauth = OAuth()

# Ajout de l'authentification avec Facebook
oauth.register(
    name="facebook",
    client_id=FACEBOOK_CLIENT_ID,  # Remplacez par votre App ID
    client_secret=FACEBOOK_CLIENT_SECRET,  # Remplacez par votre App Secret
    authorize_url="https://www.facebook.com/dialog/oauth",
    authorize_params=None,
    access_token_url="https://graph.facebook.com/oauth/access_token",
    access_token_params=None,
    client_kwargs={'scope': 'email'},
    redirect_uri=f"{BACKEND_URL}/auth/facebook"
)

#permet de d'initialiser l'authentification ici avec google
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    client_kwargs={
        'scope': 'email openid profile',
        'redirect_url': f"http://127.0.0.1:{PORT}/auth/google"
    }
)


# endpoint de depart et ici affiche une page html d'accueil
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(name="home.html", context={"request":request})

#endpoint sur lequel on lance l'authentification Google 
@app.get("/login/google")
async def login(request : Request):
    redirect_uri = request.url_for('authDefGoogle')
    return await oauth.google.authorize_redirect(request, redirect_uri)

#endpoint sur lequel on lance l'authentification Facebook
@app.get("/login/facebook")
async def login(request : Request):
    redirect_uri_facebook = request.url_for('authDefFacebook')
    return await oauth.facebook.authorize_redirect(request, redirect_uri_facebook)


#endpoint qui gere la connexion avec google malgré qu'on ne la voit pas reellement
@app.get("/auth/google")
async def authDefGoogle(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        print(f"OAuthError: {str(e)}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not valide credentials")
    
    user_info = token.get('userinfo')
    return {'data': user_info}

#endpoint qui gere la connexion avec facebook malgré qu'on ne la voit pas reellement
@app.get("/auth/facebook")
async def authDefFacebook(request: Request):
    try:
        token = await oauth.facebook.authorize_access_token(request)
    except OAuthError as e:
        print(f"OAuthError: {str(e)}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not valide credentials")
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {str(e)}")
    access_token = token['access_token']

        # Faire une requête à l'API Graph de Facebook pour obtenir des informations utilisateur
    user_info_url = 'https://graph.facebook.com/me'
    user_info_params = {
            'access_token': access_token,
            'fields': 'id,name,email,picture'
        }

    user_info_response = requests.get(user_info_url, params=user_info_params)
    user_info_response.raise_for_status()  # Lever une exception si la requête échoue

    user_info = user_info_response.json()  # Décoder la réponse JSON
    return {'data': user_info}
    

# lancement du code (pas forcement necessaire)
HOST = "127.0.0.1"
if __name__ == "__main__":
    uvicorn.run('main:app',host=HOST,port=int(PORT),reload=True)