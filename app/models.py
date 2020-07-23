from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, BigInteger, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base, db, metadata, sqlalchemy

    
custom_images = sqlalchemy.Table(
    "custom_images",
    metadata,
    Column("placeid", String, primary_key=True, unique=True, index=True),
    Column("photoref", String),
    Column("n_requests", BigInteger, index = True),
    Column("update_timestamp", DateTime),
    Column("photo_url", String),
)    

class CustomImages:
    @classmethod
    async def get(cls, placeid):
        query = custom_images.select().where(custom_images.c.placeid == placeid)
        place = await db.fetch_one(query)
        if place:
            place = dict(place)
            query = custom_images.update()
            values = {'n_requests': place['n_requests'] + 1}
            await db.execute(query=query, values=values)    
        return place 
        
    @classmethod
    async def create(cls, **place):
        place['n_requests'] = 1
        place['update_timestamp'] = datetime.now()
        query = custom_images.insert().values(**place)
        try:
            user_id = await db.execute(query)
            return True
        except: 
            return False