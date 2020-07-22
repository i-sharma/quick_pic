from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel


class CustomImageBase(BaseModel):
    placeid : str
    photoref : str

    class Config:
        orm_mode = True


class CustomImageCreate(CustomImageBase):
    
    photo_url : str
    
    class Config:
        orm_mode = True

class CustomImage(CustomImageBase):
    n_requests : int
    update_timestamp : datetime
    photo_url : str
    
    class Config:
        orm_mode = True