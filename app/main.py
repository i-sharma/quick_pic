from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
# from sqlalchemy import MetaData
from . import crud, models, schemas
from .database import SessionLocal, engine
from .database import SQLALCHEMY_DATABASE_URL,db
import requests
models.Base.metadata.create_all(bind=engine)
import os

app = FastAPI()
KEY = os.environ.get('API_KEY')

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


def validate_url(url : str):
    try:
        r = requests.get(url, allow_redirects=False)
        cont_type = r.headers.get('Content-Type',None)
        if cont_type:
            if cont_type.split('/')[0] == 'image':   return True
        return False
    except: 
        return False
    


def google_api_call(placeid:str, photoref:str):
        maxwidth = 1600
        google_photos_url = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth={maxwidth}&photoreference={photoref}&key={key}'.format(maxwidth=maxwidth, key=KEY, photoref=photoref)
        response = requests.get(google_photos_url, allow_redirects=False)
        return response.headers.get('Location', None) 
           
async def insert_db(placeid:str, photoref:str, city:str = None):
    redirect_url = google_api_call(placeid, photoref)
    if redirect_url:
        new_place = await models.CustomImages.create(placeid=placeid, photoref=photoref,
        photo_url = redirect_url, city=city)
        if new_place:
            return redirect_url
        else:
            return False  
    else:
        return False


async def update_db_photo_url(placeid:str, photoref:str, n_req : int = None):
    redirect_url = google_api_call(placeid, photoref)
    if redirect_url:
        try:
            query = models.custom_images.update().where(models.custom_images.c.placeid == placeid)
            values = {'n_requests': n_req + 1, 'photo_url' : redirect_url}
            await db.execute(query=query, values=values) 
            return redirect_url
        except: 
            return False  
    else:    
        return False

@app.get("/images/custom")
async def get_custom_image_url(placeid:str = '', photoref:str = '', city:str = '',db: Session = Depends(get_db)):
    if placeid == '' and photoref == '':
        return {
            'status': 'INVALID_QUERY',
            'message': 'please check if the fields placeid and photoref are both empty or you may have misspelled the names of query parameters in your request' ,
            'example_correct_request': 'https://easytrips-custom-images.herokuapp.com/images/custom?placeid=<PLACEID>&photoref=<PHOTOREF>'
        }
    elif placeid == '':
        return {
            'status': 'INVALID_QUERY',
            'message': 'please check if the field placeid  is empty or you may have misspelled the name of this field in your request' ,
            'example_correct_request': 'https://easytrips-custom-images.herokuapp.com/images/custom?placeid=<PLACEID>&photoref=<PHOTOREF>'
        }
    elif photoref == '':
        return {
            'status': 'INVALID_QUERY',
            'message': 'please check if the field photoref field is empty or you may have misspelled the name of this field in your request' ,
            'example_correct_request': 'https://easytrips-custom-images.herokuapp.com/images/custom?placeid=<PLACEID>&photoref=<PHOTOREF>'
        }
    db_place = await models.CustomImages.get(placeid=placeid)
    if db_place:
        if validate_url(db_place['photo_url']):
            return {
                'status' : 'SUCCESS', 
                'action_taken': 'FOUND',
                'placeid' : db_place['placeid'],
                'photoref' : db_place['photoref'],
                'image_url' : db_place['photo_url'],
                'n_requests' : db_place['n_requests'] + 1,
                'city': db_place['city']
            }
        else :
            redirect_url = await update_db_photo_url(placeid, photoref, db_place['n_requests'])
            if redirect_url:
                return {
                    'status' : 'SUCCESS', 
                    'action_taken': 'UPDATED',
                    'placeid': placeid,
                    'image_url': redirect_url,
                    'n_requests' : db_place['n_requests'] + 1,
                    'photoref' : photoref,
                    'city': db_place['city']
                }
            return {
                    'status': 'FAILURE',
                    'message' : 'Wrong photoref. Please check.'
                }  
    else:
        # insert_db()
        redirect_url = await insert_db(placeid, photoref, city)
        if redirect_url:
            return {
                    'status': 'SUCCESS', 
                    'action_taken': 'CREATED',
                    'placeid': placeid,
                    'image_url': redirect_url,
                    'n_requests' : 1,
                    'photoref' : photoref,
                    'city': city
                }
        return {
                'status': 'FAILURE',
                'message' : 'Wrong photoref. Please check.'
            }     
    