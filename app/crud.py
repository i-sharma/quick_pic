from sqlalchemy.orm import Session
from datetime import datetime
from . import models, schemas


def get_image_url(db: Session, placeid: str):
    return db.query(models.CustomImages).filter(models.CustomImages.placeid == placeid).first()


async def create_place(db: Session, placeid:str, photoref:str, photo_url:str):
    timestamp = datetime.now()
    db_place_data = models.CustomImages(placeid=placeid,update_timestamp=timestamp, 
    photoref=photoref, photo_url=photo_url, n_requests=1)
    await db.add(db_place_data)
    await db.commit()
    await db.refresh(db_place_data)
    return db_place_data