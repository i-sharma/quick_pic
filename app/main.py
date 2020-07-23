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
    r = requests.get(url, allow_redirects=False)
    cont_type = r.headers.get('Content-Type',None)
    if cont_type:
        if cont_type.split('/')[0] == 'image':   return True
    return False


def google_api_call(placeid:str, photoref:str):
        maxwidth = 1600
        print("KEY",KEY)
        google_photos_url = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth={maxwidth}&photoreference={photoref}&key={key}'.format(maxwidth=maxwidth, key=KEY, photoref=photoref)
        response = requests.get(google_photos_url, allow_redirects=False)
        return response.headers.get('Location', None) 
           
async def insert_db(placeid:str, photoref:str):
    redirect_url = google_api_call(placeid, photoref)
    if redirect_url:
        new_place = await models.CustomImages.create(placeid=placeid, photoref=photoref,
        photo_url = redirect_url)
        # print("we are here", new_place)
        if new_place:
            return redirect_url
        else:
            print("111111111")
            return False  
    else:
        print("22222222")
        return False

@app.get("/images/custom")
async def get_custom_image_url(placeid:str = '', photoref:str = '', db: Session = Depends(get_db)):
    if placeid == '' and photoref == '':
        return {
            'status': 'INVALID_QUERY',
            'message': 'please check if the fields placeid and photoref are both empty or you may have misspelled the names of query parameters in your request' 
        }
    elif placeid == '':
        return {
            'status': 'INVALID_QUERY',
            'message': 'please check if the field placeid  is empty or you may have misspelled the name of this field in your request' 
        }
    elif photoref == '':
        return {
            'status': 'INVALID_QUERY',
            'message': 'please check if the field photoref field is empty or you may have misspelled the name of this field in your request' 
        }
    db_place = await models.CustomImages.get(placeid=placeid)
    if db_place:
        if validate_url(db_place['photo_url']):
            return {
            'status' : 'FOUND', 
            'placeid' : db_place['placeid'],
            'photoref' : db_place['photoref'],
            'image_url' : db_place['photo_url'],
            'n_requests' : db_place['n_requests']
        }
        else :
            print("in here my lord")
            # redirect_url = google_api_call(placeid, photoref)
            if insert_db():
                return {
                        'status': 'CREATED',
                        'placeid': new_place,
                        'image_url': redirect_url,
                        'n_requests' : 1,
                        'photoref' : photoref
                    }
            return {
                    'status': 'FAILURE',
                    'message' : 'Wrong photoref. Please check.'
                }  
    else:
        # insert_db()
        redirect_url = await insert_db(placeid, photoref)
        if redirect_url:
            return {
                    'status': 'CREATED',
                    'placeid': placeid,
                    'image_url': redirect_url,
                    'n_requests' : 1,
                    'photoref' : photoref
                }
        return {
                'status': 'FAILURE',
                'message' : 'Wrong photoref. Please check.'
            }          
        # if redirect_url:
        #     new_place = await models.CustomImages.create(placeid=placeid, photoref=photoref,
        #     photo_url = redirect_url)
        #     # print("we are here", new_place)
        #     if new_place:
        #         return {
        #             'status': 'CREATED',
        #             'placeid': new_place,
        #             'image_url': redirect_url,
        #             'n_requests' : 1,
        #             'photoref' : photoref
        #         }
        #     else:
        #         return {
        #             'status': 'FAILURE',
        #             'message' : 'Wrong placeid or photoref. Please check.'
        #         }  
        # else:
        #     return {
        #         'status': 'FAILURE',
        #         'message' : 'Wrong photoref. Please check.'
        #     }  
    